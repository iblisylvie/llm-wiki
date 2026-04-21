#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
获取当前时间脚本
用于 Agent 在解析用户时间意图时调用，返回标准化的当前时间信息。
"""

import json
from datetime import datetime

def get_current_time_info():
    """
    获取当前时间详细信息
    返回格式为 JSON，包含时间戳、标准时间字符串、日期、时间等
    """
    now = datetime.now()
    
    # 构建时间信息字典
    time_info = {
        "timestamp": now.timestamp(),             # 时间戳 (浮点数)
        "datetime_str": now.strftime("%Y-%m-%d %H:%M:%S"), # 标准时间字符串
        "date_str": now.strftime("%Y-%m-%d"),     # 仅日期
        "time_str": now.strftime("%H:%M:%S"),     # 仅时间
        "year": now.year,                         # 年份
        "month": now.month,                       # 月份
        "day": now.day,                           # 日期
        "hour": now.hour,                         # 小时
        "minute": now.minute,                     # 分钟
        "second": now.second,                     # 秒数
        "weekday": now.strftime("%A"),            # 星期几 (英文全称)
        "weekday_cn": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()] # 星期几 (中文)
    }
    
    return time_info

def main():
    """
    主函数：打印 JSON 格式的时间信息
    """
    try:
        time_info = get_current_time_info()
        # 确保输出是纯净的 JSON，方便 Agent 解析
        print(json.dumps(time_info, ensure_ascii=False, indent=2))
    except Exception as e:
        # 错误处理：如果出错，输出错误信息
        error_info = {"error": str(e)}
        print(json.dumps(error_info, ensure_ascii=False))

if __name__ == "__main__":
    main()