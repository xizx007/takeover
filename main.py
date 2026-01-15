"""
main.py - 船舶接管辨识系统主程序 (分级协同版)
逻辑：
1. CRI < 0.3: 自主导航 (Autonomous) -> 不计算接管
2. 0.3 < CRI <= 0.6: 岸基接管 (Shore) -> 用岸基参数算
3. CRI > 0.6: 船端接管 (Onboard) -> 用船端参数算 (快)
4. Any Time: T_rem < T_req -> 紧急避险 (MRM)
"""
import time
from config import *
from physical_supply import CRITrendPredictor
from human_ship_demand import calc_total_budget

def run_hierarchical_simulation():
    print(">>> 启动分级协同接管系统 (Hierarchical Control) <<<\n")
    
    # 1. 初始化
    predictor = CRITrendPredictor()
    
    # 2. 设定场景 (固定变量)
    # 假设：资深船长，但在夜间值班，海况较差需要大舵角
    SCENE = {
        "nasa_tlx": 65,       # 中高负荷
        "hrv_stress": 0.6,    # 生理压力中等
        "is_exp": True,       # 资深
        "is_night": True,     # 夜间
        "speed": 12.0,        # 12节
        "delta_rudder": 20.0  # 需打20度舵
    }
    
    # 3. 模拟 CRI 逐渐升高的过程 (模拟真实逼近过程)
    # 数据流设计：从安全 -> 岸基区 -> 船端区 -> 极度危险
    cri_stream = [0.15, 0.25, 0.32, 0.45, 0.55, 0.62, 0.75, 0.88, 0.93]
    
    for step, current_cri in enumerate(cri_stream):
        print(f"--- [T={step}s] 当前 CRI: {current_cri} ---")
        
        # ==========================================
        # 步骤 A: 物理供给计算 (TTCR) - 全局统一
        # ==========================================
        t_rem = predictor.update_and_predict(current_cri)
        
        # ==========================================
        # 步骤 B: 确定控制权与模式 (你的核心需求)
        # ==========================================
        active_mode = None
        control_status = ""
        
        if current_cri <= THRESHOLD_LOW:
            # [0 - 0.3] 自主导航区
            control_status = "🤖 船舶自主规划 (Autonomous)"
            active_mode = "AUTO"
            
        elif current_cri <= THRESHOLD_HIGH:
            # [0.3 - 0.6] 岸基控制区
            control_status = "📡 岸基遥控介入 (Shore Control)"
            active_mode = MODE_SHORE
            
        else:
            # [> 0.6] 船端控制区
            control_status = "🚢 船端人工接管 (Onboard Control)"
            active_mode = MODE_ONBOARD

        print(f"  📝 当前策略: {control_status}")
        
        # ==========================================
        # 步骤 C: 分级博弈判定
        # ==========================================
        
        # 情况 1: 自主导航阶段 (不计算接管，只看物理时间)
        if active_mode == "AUTO":
            if t_rem > 900:
                print(f"  🟢 状态: 安全巡航")
            else:
                print(f"  🟢 状态: 自主避碰规划中 (T_rem: {t_rem:.1f}s)")
        
        # 情况 2: 需要介入 (岸基 或 船端)
        else:
            # 1. 计算需求时间 (使用对应模式的参数!)
            t_budget, t_hum, t_shp, t_comm = calc_total_budget(
                active_mode, 
                SCENE["nasa_tlx"], SCENE["hrv_stress"], 
                SCENE["is_exp"], SCENE["is_night"], 
                SCENE["speed"], SCENE["delta_rudder"]
            )
            
            # 2. 计算动态余量
            delta_t = SAFETY_MARGIN_BASE + (SCENE["speed"] * 0.5)
            
            # 3. 判定阈值
            threshold = t_budget + delta_t
            margin = t_rem - threshold
            
            print(f"  ⏳ 物理剩余: {t_rem:.1f}s | 📊 需求预算: {t_budget:.1f}s (人{t_hum}+船{t_shp})")
            
            # 4. 核心判决逻辑
            if margin > 0:
                # 时间够用 -> 发出接管请求
                if active_mode == MODE_SHORE:
                    print(f"  🟡 [岸基指令] 请岸基驾驶员介入调整航线 (裕度+{margin:.1f}s)")
                    print("     -> 此时岸基人员有足够时间完成态势感知恢复")
                else:
                    print(f"  🟠 [船端指令] 请船长立即掌舵 (裕度+{margin:.1f}s)")
                    print("     -> 岸基已来不及，切换至船端，利用其快反应优势成功匹配")
            else:
                # 时间不够用 -> 熔断 -> MRM
                print(f"  🔴 [紧急熔断] 🚫 接管来不及 (缺口{margin:.1f}s) -> 触发 MRM 自动避险")

        print("-" * 60)
        time.sleep(1)

if __name__ == "__main__":
    run_hierarchical_simulation()
