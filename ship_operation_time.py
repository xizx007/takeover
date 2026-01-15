"""
船舶接管时间模型 - 船舶操作耗时计算模块
核心依据：文档2（船舶动力学模型）的3DOF动力学、舵角/速度响应规律、推力约束
输入：船舶参数、操作目标（舵角变化、速度变化）、是否推力饱和
输出：操作执行时间（秒）
"""
import numpy as np
# 修正导入路径 - 适配config包
from config import (
    SHIP_DEFAULT_LENGTH, SHIP_MAX_RUDDER,
    RUDDER_RESPONSE_COEFF, THRUST_SATURATED_COEFF,
    OPERATION_TIME_MIN, OPERATION_TIME_MAX
)

class ShipParameter:
    """船舶参数类（文档2 CyberShip II模型参数+实船缩放逻辑）"""
    def __init__(self, ship_length=SHIP_DEFAULT_LENGTH):
        self.model_mass = 23.8
        self.model_max_thrust = 2.0
        self.model_length = SHIP_DEFAULT_LENGTH
        scale_ratio = ship_length / self.model_length
        self.actual_mass = self.model_mass * (scale_ratio ** 3)
        self.actual_max_thrust = self.model_max_thrust * (scale_ratio ** 2)

def calculate_rudder_response_time(delta_rudder):
    delta_rudder = np.clip(delta_rudder, 0, SHIP_MAX_RUDDER)
    return RUDDER_RESPONSE_COEFF * delta_rudder

def calculate_speed_adjust_time(ship_param, delta_speed, is_thrust_saturated):
    delta_speed_mps = delta_speed * 0.5144
    base_time = abs(delta_speed_mps) * ship_param.actual_mass / ship_param.actual_max_thrust
    saturated_adjust = THRUST_SATURATED_COEFF if is_thrust_saturated else 1.0
    return base_time * saturated_adjust

def calculate_operation_time(ship_length, delta_rudder, delta_speed, is_thrust_saturated=False):
    ship_param = ShipParameter(ship_length=ship_length)
    rudder_time = calculate_rudder_response_time(delta_rudder)
    speed_time = calculate_speed_adjust_time(ship_param, delta_speed, is_thrust_saturated)
    operation_time = max(rudder_time, speed_time)
    return np.clip(operation_time, OPERATION_TIME_MIN, OPERATION_TIME_MAX)

# 测试代码
if __name__ == "__main__":
    operation_time = calculate_operation_time(20, 30, 3, False)
    print(f"操作执行时间：{operation_time:.2f}s")
