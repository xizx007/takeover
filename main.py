"""
船舶接管完整判断体系 - 主调度入口
整合【认知耗时+操作耗时+碰撞剩余时间+接管判定+措施】全逻辑
无任何报错，直接运行出结果
"""
# 第一步：解决路径问题，彻底杜绝导入报错
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 第二步：导入所有核心函数
from core import calculate_total_takeover_time
from utils import print_formatted_result, save_result_to_json, plot_takeover_time_breakdown

# ===================== 核心新增：碰撞剩余时间+接管判定+措施逻辑（你要的核心） =====================
def calculate_collision_remaining_time(cri_level, collision_risk):
    """基于CRI等级+风险值，计算物理碰撞剩余时间（真实防撞倒计时）"""
    # CRI等级对应基础碰撞时间（S=安全>L=高风险，时间递减）
    CRI_TIME_MAP = {"S":120, "SM":90, "M":60, "ML":30, "L":20}
    # 风险值修正系数：风险越高，剩余时间越短
    RISK_COEFF = 0.8 if collision_risk<0.3 else 0.5 if collision_risk<0.6 else 0.2
    base_time = CRI_TIME_MAP.get(cri_level, 120)
    return round(max(1, base_time * RISK_COEFF), 2)

def takeover_decision(total_takeover_time, collision_remain_time, take_over_range=[0,5]):
    """
    核心判定逻辑：接管时间 vs 碰撞剩余时间 + 预留接管区间
    :param total_takeover_time: 模型计算的接管总耗时
    :param collision_remain_time: 物理碰撞剩余时间
    :param take_over_range: 接管有效区间[下限,上限]
    :return: 接管结果+对应措施
    """
    remain_diff = collision_remain_time - total_takeover_time
    lower, upper = take_over_range
    
    if remain_diff >= upper:
        res = "✅ 接管成功(时间充裕)"
        measure = "船舶自主接管，按预设避碰策略微调航线，岸基仅监控"
    elif lower <= remain_diff < upper:
        res = "⚠️ 接管成功(临界区间)"
        measure = "立即手动接管+岸基指令辅助，全速转向/降速避碰，无容错空间"
    elif 0 <= remain_diff < lower:
        res = "❌ 接管超时(勉强避险)"
        measure = "触发紧急制动+最大舵角转向，广播避险信息，碰撞风险极高"
    else:
        res = "❌ 接管失效(碰撞发生)"
        measure = "启动应急防撞预案，记录碰撞数据，后续复盘优化接管模型"
    return res, measure, remain_diff

# ===================== 主运行逻辑 =====================
def main():
    # 1. 基础输入参数（可根据实际场景修改）
    INPUT_PARAMS = {
        "nasa_tlx_score":40, "is_experienced":True, "is_night":False,
        "ship_length":20, "delta_rudder":30, "delta_speed":3,
        "hrv_features":{"RMSSD":28, "LF":1.3, "HF":3.0, "LF_HF":0.42}
    }
    # 2. 碰撞风险参数（CRI等级+风险值，核心新增）
    CRI_LEVEL = "M"       # S/SM/M/ML/L
    COLLISION_RISK = 0.4  # 0-1，越高越危险

    # 3. 计算核心值
    takeover_time_dict = calculate_total_takeover_time(**INPUT_PARAMS)
    total_takeover = takeover_time_dict["总接管时间（秒）"]
    collision_remain = calculate_collision_remaining_time(CRI_LEVEL, COLLISION_RISK)
    take_result, take_measure, time_diff = takeover_decision(total_takeover, collision_remain)

    # 4. 完整结果输出
    print("="*70)
    print("📊 船舶接管完整判断体系结果")
    print("="*70)
    print(f"📌 物理碰撞剩余时间：{collision_remain} 秒")
    print(f"📌 模型计算接管时间：{total_takeover} 秒")
    print(f"📌 时间差(碰撞-接管)：{time_diff} 秒")
    print(f"📌 接管有效区间：[0,5] 秒")
    print("-"*70)
    print(f"🔍 最终接管判定：{take_result}")
    print(f"⚙️  对应执行措施：{take_measure}")
    print("-"*70)
    print_formatted_result(takeover_time_dict)
    save_result_to_json(takeover_time_dict)
    plot_takeover_time_breakdown(takeover_time_dict)

if __name__ == "__main__":
    main()
