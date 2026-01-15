"""
human_ship_demand.py - 接管总时间预算计算
核心依据：文档1 (MWL绩效模型) + Tanshi结构 + Nomoto动力学
"""
from config import *

def calc_cognitive_time(mode, nasa_tlx, hrv_stress, is_exp, is_night):
    """
    计算人因认知时间 (T_human)
    区分 岸基(Shore) 与 船端(Onboard) 模式
    """
    # 1. 确定基准时间
    if mode == MODE_SHORE:
        t_base = BASE_SA_SHORE
        night_penalty = PENALTY_NIGHT_SHORE
    else:
        t_base = BASE_SA_ONBOARD
        night_penalty = PENALTY_NIGHT_ONBOARD
    
    # 2. 计算综合工作负荷 (MWL) - 文档1强调主客观融合
    # 综合分 = 60% TLX + 40% HRV (归一化后)
    mwl_score = (nasa_tlx * 0.6) + (hrv_stress * 100 * 0.4)
    t_load = (mwl_score / 10.0) * WEIGHT_MWL
    
    # 3. 经验与环境修正 (文档1结论)
    t_adjust = 0.0
    if is_exp: t_adjust += BONUS_EXPERIENCE
    if is_night: t_adjust += night_penalty
        
    t_cognitive = t_base + t_load + t_adjust
    return max(5.0, round(t_cognitive, 2))

def calc_ship_dynamic_time(current_speed, delta_rudder):
    """
    计算船舶动力学响应时间 (T_ship) - Nomoto模型
    包含：机械延迟 + 惯性滞后
    """
    if current_speed < 1.0: return 999.0
    
    # 机械延迟
    t_mech = RUDDER_DELAY + (abs(delta_rudder) / RUDDER_RATE)
    
    # 动力学惯性滞后 (关键点：速度越快响应越灵敏)
    speed_factor = 10.0 / max(5.0, current_speed)
    t_inertia = NOMOTO_T * speed_factor * 1.5 
    
    return round(t_mech + t_inertia, 2)

def calc_total_budget(mode, nasa_tlx, hrv_stress, is_exp, is_night, speed, rudder):
    """计算总时间预算"""
    # A. 认知
    t_human = calc_cognitive_time(mode, nasa_tlx, hrv_stress, is_exp, is_night)
    # B. 船
    t_ship = calc_ship_dynamic_time(speed, rudder)
    # C. 通信
    t_comm = COMM_DELAY_SHORE if mode == MODE_SHORE else COMM_DELAY_ONBOARD
    
    total = t_human + t_ship + t_comm
    return total, t_human, t_ship, t_comm
