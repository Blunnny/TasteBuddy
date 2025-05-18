#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
保存特征名称顺序
这个脚本从训练数据和模型中提取特征名称顺序，并保存到feature_names.joblib文件中
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)

def main():
    """主函数，保存特征名称顺序"""
    print(f"{Fore.CYAN}正在从模型和训练数据中提取特征名称顺序...{Style.RESET_ALL}")
    
    try:
        # 首先尝试从imputer模型中获取特征名称
        print(f"{Fore.CYAN}尝试从imputer模型中获取特征名称...{Style.RESET_ALL}")
        imputer_path = os.path.join("models", "imputer.joblib")
        if os.path.exists(imputer_path):
            imputer = joblib.load(imputer_path)
            if hasattr(imputer, 'feature_names_in_'):
                feature_names = list(imputer.feature_names_in_)
                print(f"{Fore.GREEN}成功从imputer模型中获取特征名称，共{len(feature_names)}个特征{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}imputer模型中没有feature_names_in_属性{Style.RESET_ALL}")
                feature_names = None
        else:
            print(f"{Fore.YELLOW}找不到imputer模型文件{Style.RESET_ALL}")
            feature_names = None
        
        # 如果无法从imputer模型中获取特征名称，则从训练数据中获取
        if feature_names is None:
            print(f"{Fore.CYAN}尝试从训练数据中获取特征名称...{Style.RESET_ALL}")
            # 加载训练数据
            with open("data/onehot_encoded_data.json", "r", encoding="utf-8") as f:
                train_data = json.load(f)
                if not train_data or len(train_data) == 0:
                    print(f"{Fore.RED}错误：训练数据为空{Style.RESET_ALL}")
                    return
                
                # 获取第一行数据的所有特征名
                first_item = train_data[0]
                
                # 获取所有可能的特征列名（排除非特征列）
                feature_names = [col for col in first_item.keys() if col not in ['title', 'watch_time', 'director', 'cast', 'user_score']]
                print(f"{Fore.GREEN}成功从训练数据中获取特征名称，共{len(feature_names)}个特征{Style.RESET_ALL}")
        
        # 确保包含必要的特征
        essential_features = ['douban_score', 'year', 'watch_year', 'watch_quarter', 
                            'title_length', 'director_count', 'cast_count']
        
        # 检查是否缺少必要的特征
        missing_features = [f for f in essential_features if f not in feature_names]
        if missing_features:
            print(f"{Fore.YELLOW}警告：缺少以下必要特征，将添加它们：{missing_features}{Style.RESET_ALL}")
            # 将缺失的特征添加到特征列表中
            feature_names.extend(missing_features)
        
        # 创建models目录（如果不存在）
        os.makedirs("models", exist_ok=True)
        
        # 保存特征名称顺序
        joblib.dump(feature_names, "models/feature_names.joblib")
        
        print(f"{Fore.GREEN}成功保存特征名称顺序到models/feature_names.joblib{Style.RESET_ALL}")
        print(f"{Fore.CYAN}特征数量: {len(feature_names)}{Style.RESET_ALL}")
        
        # 显示前10个特征名称
        print(f"{Fore.CYAN}前10个特征名称:{Style.RESET_ALL}")
        for i, name in enumerate(feature_names[:10]):
            print(f"  {i+1}. {name}")
        
        # 显示必要的特征
        print(f"{Fore.CYAN}必要的特征:{Style.RESET_ALL}")
        for i, name in enumerate(essential_features):
            print(f"  {i+1}. {name} - {'✓' if name in feature_names else '✗'}")
        
    except Exception as e:
        print(f"{Fore.RED}保存特征名称顺序时出错: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 