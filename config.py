"""
config.py - 船舶接管辨识系统参数配置
核心策略：基于风险分级的多地协同控制 (Risk-Based Hierarchical Control)
"""

# --- 1. CRI 风险分级阈值 (你的核心需求) ---
THRESHOLD_LOW = 0.3      # [0.0 - 0.3] 低风险：船舶自主规划
THRESHOLD_HIGH = 0.6     # [0.3 - 0.6] 中风险：岸基远程介入
                         # [0.6 - 1.0] 高风险：船端人工接管

# CRI 趋势预测参数
CRI_LIMIT = 0.95         # 物理碰撞临界值 (调高以留出计算余量)
CRI_HISTORY_LEN = 10      # 历史窗口长度
CRI_SAMPLING_RATE = 1.0  # 采样率

# --- 2. 人因参数 (基于文档1校准) ---
MODE_SHORE = "SHORE"      # 岸基模式
MODE_ONBOARD = "ONBOARD"  # 船端模式

# 基础态势感知恢复时间 (Base SA Recovery Time)
# 岸基：文档1指出远程监控存在"回路外(OOTL)"效应，恢复极慢
BASE_SA_SHORE = 45.0      
# 船端：身临其境，物理感知强，恢复快
BASE_SA_ONBOARD = 15.0    

# 调节系数 (秒)
BONUS_EXPERIENCE = -12.0  # 资深人员显著快 (文档1结论)
PENALTY_NIGHT_SHORE = 20.0   # 岸基夜间易疲劳走神
PENALTY_NIGHT_ONBOARD = 8.0  # 船端有物理刺激，稍好
WEIGHT_MWL = 0.4          # 负荷权重

# --- 3. 船舶动力学参数 (Nomoto模型 - 灵便型货船) ---
# 修正了之前的参数，防止船"反应太慢"导致永远算不过来
NOMOTO_K = 0.20      # 旋回性指数 (提高灵活性)
NOMOTO_T = 40.0      # 惯性时间常数 (T值越大越难拐弯)
RUDDER_DELAY = 3.0   # 舵机响应延迟
RUDDER_RATE = 3.0    # 舵速 deg/s

# --- 4. 安全余量 ---
SAFETY_MARGIN_BASE = 10.0
COMM_DELAY_SHORE = 3.0   # 卫星通信延迟
COMM_DELAY_ONBOARD = 0.0 # 无延迟
