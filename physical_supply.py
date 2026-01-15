"""
physical_supply.py - 物理供给侧计算 (TTCR算法)
核心功能：基于 CRI 变化率预测物理剩余时间
"""
import numpy as np
from config import CRI_LIMIT, CRI_HISTORY_LEN, CRI_SAMPLING_RATE

class CRITrendPredictor:
    def __init__(self):
        self.history = []
    
    def update_and_predict(self, current_cri):
        """输入当前 CRI，输出预测的物理剩余时间 T_rem"""
        # 1. 达到死线
        if current_cri >= CRI_LIMIT: return 0.0
            
        # 2. 维护历史数据
        self.history.append(current_cri)
        if len(self.history) > CRI_HISTORY_LEN:
            self.history.pop(0)
            
        # 3. 冷启动兜底
        if len(self.history) < 3: return 999.0
            
        # 4. 计算斜率 (线性拟合)
        x = np.arange(len(self.history)) * CRI_SAMPLING_RATE
        y = np.array(self.history)
        slope = np.polyfit(x, y, 1)[0]
        
        # 5. 计算 TTCR
        if slope <= 0.001: 
            return 999.0 # 风险未增加
        else:
            t_rem = (CRI_LIMIT - current_cri) / slope
            return max(0.0, round(t_rem, 2))
