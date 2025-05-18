#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
豆瓣评分预测系统启动脚本
这个脚本用于启动豆瓣评分预测系统，可以在任何支持Python的平台上运行。
"""

import os
import sys
import subprocess

def main():
    """主函数，启动豆瓣评分预测系统"""
    print("=" * 50)
    print("          豆瓣评分预测系统 - 启动中")
    print("=" * 50)
    print()
    
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建app.py的路径
    app_path = os.path.join(current_dir, "src", "app.py")
    
    # 检查文件是否存在
    if not os.path.exists(app_path):
        print(f"错误：找不到应用程序文件 {app_path}")
        input("按回车键退出...")
        return
    
    try:
        # 使用Python解释器运行app.py
        # -u 参数禁用输出缓冲
        # -X utf8 参数设置UTF-8编码
        subprocess.run([sys.executable, "-u", "-X", "utf8", app_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"错误：程序运行失败，错误代码 {e.returncode}")
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"错误：{str(e)}")
    
    print("\n程序已退出")

if __name__ == "__main__":
    main() 