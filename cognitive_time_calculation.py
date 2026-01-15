"""
船舶接管时间模型 - 认知准备时间计算模块
核心依据：文档1（MWL-绩效模型）的HPM模型、NASA-TLX评分、经验/时段调节系数
输入：NASA-TLX评分、操作员经验、时段、HRV特征（可选）
输出：认知准备时间（秒）
"""
import numpy as np
# 修正导入路径 - 适配config包
from config import (
    HRV_DEFAULT, EXPERIENCE_ADJUST, NIGHT_ADJUST,
    COGNITIVE_TIME_MIN, COGNITIVE_TIME_MAX,
    NASA_TLX_MIN, NASA_TLX_MAX
)

def normalize_hrv(hrv_features):
    """归一化HRV特征（文档1中HRV处理流程简化）"""
    hrv = hrv_features or HRV_DEFAULT
    rmssd = hrv.get("RMSSD", HRV_DEFAULT["RMSSD"])
    lf = hrv.get("LF", HRV_DEFAULT["LF"])
    hf = hrv.get("HF", HRV_DEFAULT["HF"])
    lf_hf = hrv.get("LF_HF", HRV_DEFAULT["LF_HF"])
    
    norm_rmssd = (rmssd - 10) / (40 - 10) * 100
    norm_lf = (lf - 0.5) / (2.0 - 0.5) * 100
    norm_hf = (hf - 1.0) / (4.0 - 1.0) * 100
    norm_lf_hf = (0.5 - lf_hf) / (0.5 - 0.4) * 100
    
    hrv_norm = (norm_rmssd * 0.3 + norm_lf * 0.2 + norm_hf * 0.3 + norm_lf_hf * 0.2)
    return np.clip(hrv_norm, NASA_TLX_MIN, NASA_TLX_MAX)

def calculate_cognitive_time(nasa_tlx_score, is_experienced, is_night, hrv_features=None):
    """计算认知准备时间（文档1 Eq.1简化版+调节系数）"""
    nasa_tlx_score = np.clip(nasa_tlx_score, NASA_TLX_MIN, NASA_TLX_MAX)
    
    if hrv_features is not None:
        hrv_norm = normalize_hrv(hrv_features)
        mwl_comprehensive = nasa_tlx_score * 0.6 + hrv_norm * 0.4
    else:
        mwl_comprehensive = nasa_tlx_score
    
    performance_scale = -0.0184 * (mwl_comprehensive ** 2) + 0.2154 * mwl_comprehensive + 0.1374
    base_cognitive_time = (1 - performance_scale) * 100
    
    experience_adjust = EXPERIENCE_ADJUST if is_experienced else 0.0
    night_adjust = NIGHT_ADJUST if is_night else 0.0
    
    cognitive_time = base_cognitive_time + experience_adjust + night_adjust
    return np.clip(cognitive_time, COGNITIVE_TIME_MIN, COGNITIVE_TIME_MAX)

# 测试代码
if __name__ == "__main__":
    cognitive_time_1 = calculate_cognitive_time(60, True, False)
    print(f"测试用例1认知时间：{cognitive_time_1:.2f}s")
    hrv_test = {"RMSSD": 30, "LF": 1.5, "HF": 3.2, "LF_HF": 0.45}
    cognitive_time_2 = calculate_cognitive_time(50, False, True, hrv_test)
    print(f"测试用例2认知时间：{cognitive_time_2:.2f}s")
