"""
船舶接管时间计算 - 常量配置文件
统一管理行业标准、默认值、调节系数（便于后续维护）
"""
# NASA-TLX评分范围
NASA_TLX_MIN = 0
NASA_TLX_MAX = 100

# HRV特征默认值（文档1均值）
HRV_DEFAULT = {
    "RMSSD": 25,
    "LF": 1.2,
    "HF": 2.9,
    "LF_HF": 0.42
}

# 船舶参数默认值（文档2 CyberShip II模型）
SHIP_DEFAULT_LENGTH = 1.255  # 模型船长度（m）
SHIP_MAX_RUDDER = 45         # 最大舵角（度）

# 调节系数（文档1/2实证）
EXPERIENCE_ADJUST = 38.0     # 资深操作员认知时间调节值
NIGHT_ADJUST = -19.89        # 夜间操作认知时间调节值
RUDDER_RESPONSE_COEFF = 0.8  # 舵角响应系数（秒/度）
THRUST_SATURATED_COEFF = 1.5 # 推力饱和调节系数
COMM_DELAY_DEFAULT = 2.0     # 通信延迟默认值（秒）

# 时间范围限制
COGNITIVE_TIME_MIN = 1.0
COGNITIVE_TIME_MAX = 60.0
OPERATION_TIME_MIN = 5.0
OPERATION_TIME_MAX = 30.0
