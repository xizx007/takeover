"""
结果输出工具模块
支持控制台格式化输出、JSON文件导出、简单可视化
"""
import json
import matplotlib.pyplot as plt

def print_formatted_result(result):
    """
    控制台格式化输出计算结果
    :param result: calculate_total_takeover_time返回的字典
    """
    print("\n===== 船舶接管时间计算结果 =====")
    for key, value in result.items():
        print(f"{key:<15}: {value:>6.2f}")
    print("===============================\n")

def save_result_to_json(result, file_path="takeover_time_result.json"):
    """
    将结果保存为JSON文件
    :param result: 计算结果字典
    :param file_path: 保存路径
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"结果已保存至：{file_path}")

def plot_takeover_time_breakdown(result):
    """
    绘制接管时间构成饼图（可视化）
    :param result: 计算结果字典
    """
    # 提取各部分耗时（排除总时间）
    labels = [k for k in result.keys() if k != "总接管时间（秒）"]
    sizes = [result[k] for k in labels]
    
    # 绘图配置
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 支持中文
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90)
    plt.title("船舶接管时间构成")
    plt.axis('equal')  # 饼图为正圆形
    plt.savefig("takeover_time_breakdown.png", dpi=300, bbox_inches='tight')
    plt.show()

__all__ = ["print_formatted_result", "save_result_to_json", "plot_takeover_time_breakdown"]
