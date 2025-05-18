#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试预测功能
这个脚本用于直接测试预测功能，便于调试
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import datetime
from colorama import init, Fore, Style

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.load_models import load_models, predict_with_ensemble

# 初始化colorama
init(autoreset=True)

def create_test_movie():
    """创建一个测试电影数据"""
    movie_data = {
        "title": "测试电影",
        "douban_score": 7.5,
        "watch_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "year": 2020,
        "region": ["中国大陆", "美国"],
        "genre": ["剧情", "科幻"],
        "director": ["测试导演"],
        "cast": ["测试演员1", "测试演员2"]
    }
    return movie_data

def prepare_features(movie_data):
    """准备模型所需的特征"""
    print(f"{Fore.CYAN}准备特征...{Style.RESET_ALL}")
    
    # 创建一行数据
    df = pd.DataFrame([movie_data])
    
    # 处理时间特征
    df['watch_time'] = pd.to_datetime(df['watch_time'])
    df['watch_year'] = df['watch_time'].dt.year
    df['watch_quarter'] = df['watch_time'].dt.quarter
    
    # 处理标题长度
    df['title_length'] = df['title'].str.split().str.len()
    
    # 处理导演和演员数量
    df['director_count'] = df['director'].apply(len)
    df['cast_count'] = df['cast'].apply(len)
    
    # 加载特征名称
    try:
        print(f"{Fore.CYAN}加载特征名称...{Style.RESET_ALL}")
        import joblib
        feature_names = joblib.load("models/feature_names.joblib")
        
        if feature_names and isinstance(feature_names, list):
            print(f"{Fore.GREEN}成功加载特征名称，共{len(feature_names)}个特征{Style.RESET_ALL}")
            
            # 获取所有地区和类型特征
            region_features = [f for f in feature_names if f.startswith('region_')]
            genre_features = [f for f in feature_names if f.startswith('genre_')]
            
            print(f"{Fore.CYAN}地区特征数量: {len(region_features)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}类型特征数量: {len(genre_features)}{Style.RESET_ALL}")
            
            # 确保基本特征存在
            basic_features = ['douban_score', 'year', 'watch_year', 'watch_quarter', 
                             'title_length', 'director_count', 'cast_count']
            for feature in basic_features:
                if feature not in df.columns:
                    print(f"{Fore.YELLOW}添加缺失的基本特征: {feature}{Style.RESET_ALL}")
                    df[feature] = 0
            
            # 初始化所有地区和类型特征为0
            for feature in region_features + genre_features:
                df[feature] = 0
            
            # 设置选中的地区和类型为1
            for region in movie_data['region']:
                feature = f'region_{region}'
                if feature in region_features:
                    df[feature] = 1
                    print(f"{Fore.GREEN}设置地区特征: {feature} = 1{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}地区特征不存在: {feature}{Style.RESET_ALL}")
            
            for genre in movie_data['genre']:
                feature = f'genre_{genre}'
                if feature in genre_features:
                    df[feature] = 1
                    print(f"{Fore.GREEN}设置类型特征: {feature} = 1{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}类型特征不存在: {feature}{Style.RESET_ALL}")
            
            # 确保所有特征都存在
            for feature in feature_names:
                if feature not in df.columns:
                    print(f"{Fore.YELLOW}添加缺失特征: {feature}{Style.RESET_ALL}")
                    df[feature] = 0
            
            # 打印当前特征列表
            print(f"{Fore.CYAN}当前特征列表: {list(df.columns)}{Style.RESET_ALL}")
            
            # 按照特征名称顺序排列
            print(f"{Fore.CYAN}按照特征名称顺序排列...{Style.RESET_ALL}")
            df = df[feature_names]
            
            # 打印特征信息
            print(f"{Fore.CYAN}特征形状: {df.shape}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}前10个特征: {list(df.columns)[:10]}{Style.RESET_ALL}")
            
            return df
    except Exception as e:
        print(f"{Fore.RED}加载特征名称失败: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
    
    print(f"{Fore.RED}无法准备特征，返回None{Style.RESET_ALL}")
    return None

def test_prediction():
    """测试预测功能"""
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'测试预测功能':^60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    # 创建测试电影数据
    movie_data = create_test_movie()
    print(f"{Fore.GREEN}测试电影数据:{Style.RESET_ALL}")
    for key, value in movie_data.items():
        print(f"  {key}: {value}")
    
    # 加载模型
    print(f"\n{Fore.CYAN}加载模型...{Style.RESET_ALL}")
    models = load_models()
    
    if not models:
        print(f"{Fore.RED}错误：未能加载任何模型{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}已加载的模型:{Style.RESET_ALL}")
    for model_name in models:
        print(f"  - {model_name}")
    
    # 准备特征
    features = prepare_features(movie_data)
    
    if features is None:
        print(f"{Fore.RED}错误：无法准备特征{Style.RESET_ALL}")
        return
    
    # 预测评分
    print(f"\n{Fore.CYAN}预测评分...{Style.RESET_ALL}")
    try:
        prediction = predict_with_ensemble(features, models)
        
        if prediction is None:
            print(f"{Fore.RED}预测失败，返回None{Style.RESET_ALL}")
            return
        
        # 将numpy数组转换为标量
        if isinstance(prediction, np.ndarray):
            prediction = prediction[0]
        
        print(f"\n{Fore.GREEN}预测结果: {prediction:.2f}/5.0{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}预测过程中出错: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prediction() 