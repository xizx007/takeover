"""
船舶总接管时间整合计算模块
核心逻辑：总时间 = 认知准备时间 + 操作执行时间 + 通信延迟
输入：所有前序模块所需参数 + 通信延迟
输出：总接管时间（秒）+ 各部分耗时明细
"""
from .cognitive_time_calculation import calculate_cognitive_time
from .ship_operation_time import calculate_operation_time
# 修正导入路径 - 适配config包
from config import COMM_DELAY_DEFAULT

def calculate_total_takeover_time(
    # 必传参数(放前面)
    nasa_tlx_score,
    is_experienced,
    is_night,
    ship_length,
    delta_rudder,
    delta_speed,
    # 可选参数(放后面)
    hrv_features=None,
    is_thrust_saturated=False,
    comm_delay=COMM_DELAY_DEFAULT
):
    cognitive_time = calculate_cognitive_time(nasa_tlx_score, is_experienced, is_night, hrv_features)
    operation_time = calculate_operation_time(ship_length, delta_rudder, delta_speed, is_thrust_saturated)
    total_time = cognitive_time + operation_time + comm_delay
    
    return {
        "总接管时间（秒）": round(total_time, 2),
        "认知准备时间（秒）": round(cognitive_time, 2),
        "操作执行时间（秒）": round(operation_time, 2),
        "通信延迟（秒）": round(comm_delay, 2)
    }

# 测试代码
if __name__ == "__main__":
    input_params = {
        "nasa_tlx_score":60,"is_experienced":True,"is_night":False,
        "ship_length":20,"delta_rudder":30,"delta_speed":3,
        "hrv_features":{"RMSSD":28,"LF":1.3,"HF":3.0,"LF_HF":0.42}
    }
    result = calculate_total_takeover_time(**input_params)
    for k,v in result.items():print(f"{k}:{v}")
