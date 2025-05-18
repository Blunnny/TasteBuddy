import pandas as pd
import numpy as np
import os
import sys
import datetime
import json
import locale
import io
from colorama import init, Fore, Back, Style

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.load_models import load_models, predict_with_ensemble

# 初始化colorama，设置自动重置和转换ANSI颜色
init(autoreset=True, convert=True)

# 设置控制台编码
if sys.platform == 'win32':
    # 对于Windows系统
    os.system('chcp 65001 > nul')
    # 修复Windows控制台输出
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # 设置区域
    try:
        locale.setlocale(locale.LC_ALL, 'Chinese_China.utf8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'zh_CN.utf8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, '')
            except:
                pass
else:
    # 对于类Unix系统
    try:
        locale.setlocale(locale.LC_ALL, 'zh_CN.utf8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, '')
        except:
            pass

def clear_screen():
    """清除控制台屏幕"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印程序标题"""
    clear_screen()
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{' '*20}豆瓣评分预测系统{' '*20}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print()

def load_region_and_genre_options():
    """加载可用的地区和类型选项"""
    try:
        # 读取第一条数据，获取所有可能的地区和类型选项
        with open("data/onehot_encoded_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if data and len(data) > 0:
                first_item = data[0]
                regions = [col.replace("region_", "") for col in first_item.keys() if col.startswith("region_")]
                genres = [col.replace("genre_", "") for col in first_item.keys() if col.startswith("genre_")]
                return regions, genres
    except Exception as e:
        print(f"{Fore.RED}加载地区和类型选项时出错: {e}{Style.RESET_ALL}")
    
    # 如果无法从数据中加载，则使用默认值
    regions = ["中国大陆", "中国香港", "中国台湾", "美国", "日本", "韩国", "英国", "法国"]
    genres = ["剧情", "喜剧", "动作", "爱情", "科幻", "动画", "悬疑", "惊悚", "恐怖", "犯罪"]
    return regions, genres

def get_user_input():
    """获取用户输入的影视作品信息"""
    print_header()
    print(f"{Fore.YELLOW}请输入影视作品信息：{Style.RESET_ALL}")
    print()
    
    # 获取基本信息
    title = input(f"{Fore.WHITE}片名: {Style.RESET_ALL}")
    
    # 获取年份
    while True:
        try:
            year = int(input(f"{Fore.WHITE}年份: {Style.RESET_ALL}"))
            if 1900 <= year <= 2100:
                break
            else:
                print(f"{Fore.RED}年份应在1900-2100之间，请重新输入{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}请输入有效的年份{Style.RESET_ALL}")
    
    # 获取豆瓣评分（可选）
    douban_score = None
    while True:
        score_input = input(f"{Fore.WHITE}豆瓣评分(0-10，可选): {Style.RESET_ALL}")
        if not score_input:
            break
        try:
            douban_score = float(score_input)
            if 0 <= douban_score <= 10:
                break
            else:
                print(f"{Fore.RED}评分应在0-10之间，请重新输入{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}请输入有效的评分{Style.RESET_ALL}")
    
    # 加载可用的地区和类型选项
    regions, genres = load_region_and_genre_options()
    
    # 选择地区
    print(f"\n{Fore.YELLOW}可选地区:{Style.RESET_ALL}")
    for i, region in enumerate(regions):
        print(f"{i+1}. {region}", end="\t")
        if (i+1) % 5 == 0:
            print()
    print("\n")
    
    selected_regions = []
    while True:
        region_input = input(f"{Fore.WHITE}选择地区(输入序号，多个用逗号分隔，输入0完成): {Style.RESET_ALL}")
        if region_input == "0":
            if not selected_regions:
                print(f"{Fore.RED}请至少选择一个地区{Style.RESET_ALL}")
                continue
            break
        
        try:
            indices = [int(idx.strip()) for idx in region_input.split(",")]
            for idx in indices:
                if 1 <= idx <= len(regions) and regions[idx-1] not in selected_regions:
                    selected_regions.append(regions[idx-1])
            
            print(f"{Fore.GREEN}已选择地区: {', '.join(selected_regions)}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}请输入有效的序号{Style.RESET_ALL}")
    
    # 选择类型
    print(f"\n{Fore.YELLOW}可选类型:{Style.RESET_ALL}")
    for i, genre in enumerate(genres):
        print(f"{i+1}. {genre}", end="\t")
        if (i+1) % 5 == 0:
            print()
    print("\n")
    
    selected_genres = []
    while True:
        genre_input = input(f"{Fore.WHITE}选择类型(输入序号，多个用逗号分隔，输入0完成): {Style.RESET_ALL}")
        if genre_input == "0":
            if not selected_genres:
                print(f"{Fore.RED}请至少选择一个类型{Style.RESET_ALL}")
                continue
            break
        
        try:
            indices = [int(idx.strip()) for idx in genre_input.split(",")]
            for idx in indices:
                if 1 <= idx <= len(genres) and genres[idx-1] not in selected_genres:
                    selected_genres.append(genres[idx-1])
            
            print(f"{Fore.GREEN}已选择类型: {', '.join(selected_genres)}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}请输入有效的序号{Style.RESET_ALL}")
    
    # 输入导演
    directors = []
    print(f"\n{Fore.YELLOW}请输入导演(每行一个，输入空行完成):{Style.RESET_ALL}")
    while True:
        director = input(f"{Fore.WHITE}导演: {Style.RESET_ALL}")
        if not director:
            if not directors:
                print(f"{Fore.RED}请至少输入一位导演{Style.RESET_ALL}")
                continue
            break
        directors.append(director)
    
    # 输入演员（可选）
    casts = []
    print(f"\n{Fore.YELLOW}请输入主要演员(每行一个，输入空行完成，可选):{Style.RESET_ALL}")
    while True:
        cast = input(f"{Fore.WHITE}演员: {Style.RESET_ALL}")
        if not cast:
            break
        casts.append(cast)
    
    # 构建数据
    movie_data = {
        "title": title,
        "douban_score": douban_score,
        "watch_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "year": year,
        "region": selected_regions,
        "genre": selected_genres,
        "director": directors,
        "cast": casts
    }
    
    return movie_data

def prepare_features(movie_data):
    """准备模型所需的特征"""
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
    
    # 处理缺失的豆瓣评分
    if df['douban_score'].iloc[0] is None:
        # 使用默认值7.5（或者从数据中计算平均值）
        df['douban_score'] = 7.5
    
    # 尝试直接加载特征名称
    try:
        print(f"{Fore.CYAN}尝试加载特征名称文件...{Style.RESET_ALL}")
        import joblib
        feature_names = joblib.load("models/feature_names.joblib")
        
        if feature_names and isinstance(feature_names, list):
            print(f"{Fore.GREEN}成功加载特征名称，共{len(feature_names)}个特征{Style.RESET_ALL}")
            
            # 确保基本特征存在
            basic_features = ['douban_score', 'year', 'watch_year', 'watch_quarter', 
                             'title_length', 'director_count', 'cast_count']
            for feature in basic_features:
                if feature not in df.columns:
                    print(f"{Fore.YELLOW}添加缺失的基本特征: {feature}{Style.RESET_ALL}")
                    df[feature] = 0
            
            # 处理地区和类型特征
            for col in feature_names:
                if col.startswith('region_'):
                    region = col.replace('region_', '')
                    # 设置默认值为0
                    df[col] = 0
                    # 如果该地区在用户选择的地区中，设置为1
                    if region in movie_data['region']:
                        df[col] = 1
                        
                elif col.startswith('genre_'):
                    genre = col.replace('genre_', '')
                    # 设置默认值为0
                    df[col] = 0
                    # 如果该类型在用户选择的类型中，设置为1
                    if genre in movie_data['genre']:
                        df[col] = 1
            
            # 确保所有特征都存在，并按照特征名称文件中的顺序排列
            for col in feature_names:
                if col not in df.columns:
                    df[col] = 0
            
            # 打印当前特征列表
            print(f"{Fore.CYAN}当前特征列表: {list(df.columns)[:10]}...等{len(df.columns)}个{Style.RESET_ALL}")
            
            # 返回按照特征名称文件中的顺序排列的特征
            return df[feature_names]
    except Exception as e:
        print(f"{Fore.YELLOW}加载特征名称文件失败: {e}，将使用默认特征处理方式{Style.RESET_ALL}")
    
    # 如果无法加载特征名称文件，则尝试从训练数据中获取特征顺序
    try:
        print(f"{Fore.CYAN}尝试从训练数据获取特征顺序...{Style.RESET_ALL}")
        # 加载训练数据的第一行，只是为了获取特征顺序
        with open("data/onehot_encoded_data.json", "r", encoding="utf-8") as f:
            train_data = json.load(f)
            if train_data and len(train_data) > 0:
                # 获取第一行数据的所有特征名
                first_item = train_data[0]
                # 获取所有可能的特征列名（排除非特征列）
                all_feature_cols = [col for col in first_item.keys() if col not in ['title', 'watch_time', 'director', 'cast', 'user_score']]
                
                print(f"{Fore.GREEN}成功从训练数据获取特征顺序，共{len(all_feature_cols)}个特征{Style.RESET_ALL}")
                
                # 确保基本特征存在
                basic_features = ['douban_score', 'year', 'watch_year', 'watch_quarter', 
                                 'title_length', 'director_count', 'cast_count']
                for feature in basic_features:
                    if feature not in df.columns:
                        print(f"{Fore.YELLOW}添加缺失的基本特征: {feature}{Style.RESET_ALL}")
                        df[feature] = 0
                
                # 处理地区和类型特征
                for col in all_feature_cols:
                    if col.startswith('region_'):
                        region = col.replace('region_', '')
                        # 设置默认值为0
                        df[col] = 0
                        # 如果该地区在用户选择的地区中，设置为1
                        if region in movie_data['region']:
                            df[col] = 1
                            
                    elif col.startswith('genre_'):
                        genre = col.replace('genre_', '')
                        # 设置默认值为0
                        df[col] = 0
                        # 如果该类型在用户选择的类型中，设置为1
                        if genre in movie_data['genre']:
                            df[col] = 1
                
                # 确保所有特征都存在
                for col in all_feature_cols:
                    if col not in df.columns:
                        df[col] = 0
                
                # 返回按照训练数据中相同顺序的特征
                return df[all_feature_cols]
    except Exception as e:
        print(f"{Fore.YELLOW}无法从训练数据获取特征顺序: {e}，将使用默认特征处理方式{Style.RESET_ALL}")
    
    # 如果以上方法都失败，则使用默认的特征处理方式
    print(f"{Fore.YELLOW}使用默认特征处理方式{Style.RESET_ALL}")
    
    # One-hot编码地区和类型
    regions, genres = load_region_and_genre_options()
    
    # 为每个地区和类型创建特征列，并设置默认值为0
    for region in regions:
        df[f'region_{region}'] = 0
    
    for genre in genres:
        df[f'genre_{genre}'] = 0
    
    # 设置选中的地区和类型为1
    for region in movie_data['region']:
        if f'region_{region}' in df.columns:
            df[f'region_{region}'] = 1
    
    for genre in movie_data['genre']:
        if f'genre_{genre}' in df.columns:
            df[f'genre_{genre}'] = 1
    
    # 确定特征列
    feature_columns = [col for col in df.columns if col not in ['title', 'watch_time', 'director', 'cast', 'region', 'genre']]
    
    return df[feature_columns]

def predict_rating(movie_data):
    """预测评分"""
    try:
        # 加载模型
        print(f"{Fore.CYAN}加载模型...{Style.RESET_ALL}")
        models = load_models()
        
        # 检查是否成功加载了模型
        if not models:
            print(f"{Fore.RED}错误：未能加载任何模型{Style.RESET_ALL}")
            return None
        
        # 打印加载的模型信息
        print(f"{Fore.CYAN}已加载的模型:{Style.RESET_ALL}")
        for model_name in models:
            print(f"  - {model_name}")
        
        # 准备特征
        print(f"{Fore.CYAN}准备特征...{Style.RESET_ALL}")
        features = prepare_features(movie_data)
        
        # 打印特征信息
        print(f"{Fore.CYAN}特征数量: {len(features.columns)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}前10个特征: {list(features.columns)[:10]}{Style.RESET_ALL}")
        
        # 如果有feature_names，检查特征是否匹配
        if "feature_names" in models and isinstance(models["feature_names"], list):
            feature_names = models["feature_names"]
            print(f"{Fore.CYAN}模型特征数量: {len(feature_names)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}模型前10个特征: {feature_names[:10]}{Style.RESET_ALL}")
            
            # 检查特征是否一致
            missing_features = [f for f in feature_names if f not in features.columns]
            if missing_features:
                print(f"{Fore.YELLOW}警告: 缺少以下特征: {missing_features}{Style.RESET_ALL}")
                # 添加缺失的特征
                for feature in missing_features:
                    features[feature] = 0
            
            # 重排特征顺序
            features = features[feature_names]
        
        # 预测评分
        print(f"{Fore.CYAN}预测评分中...{Style.RESET_ALL}")
        prediction = predict_with_ensemble(features, models)
        
        # 将numpy数组转换为标量
        if isinstance(prediction, np.ndarray):
            prediction = prediction[0]
        
        return prediction
    
    except Exception as e:
        print(f"{Fore.RED}预测过程中出错: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return None

def display_result(movie_data, predicted_score):
    """显示预测结果"""
    print_header()
    print(f"{Fore.GREEN}【预测结果】{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    
    print(f"{Fore.WHITE}片名: {Style.RESET_ALL}{movie_data['title']}")
    print(f"{Fore.WHITE}年份: {Style.RESET_ALL}{movie_data['year']}")
    
    if movie_data['douban_score'] is not None:
        print(f"{Fore.WHITE}豆瓣评分: {Style.RESET_ALL}{movie_data['douban_score']}")
    
    print(f"{Fore.WHITE}地区: {Style.RESET_ALL}{', '.join(movie_data['region'])}")
    print(f"{Fore.WHITE}类型: {Style.RESET_ALL}{', '.join(movie_data['genre'])}")
    print(f"{Fore.WHITE}导演: {Style.RESET_ALL}{', '.join(movie_data['director'])}")
    
    if movie_data['cast']:
        print(f"{Fore.WHITE}主要演员: {Style.RESET_ALL}{', '.join(movie_data['cast'])}")
    
    print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
    
    if predicted_score is not None:
        # 根据预测分数选择颜色
        if predicted_score >= 4.5:
            color = Fore.GREEN  # 高分
        elif predicted_score >= 3.5:
            color = Fore.YELLOW  # 中等分数
        else:
            color = Fore.RED  # 低分
        
        print(f"{Fore.WHITE}预测评分: {color}{predicted_score:.2f}/5.0{Style.RESET_ALL}")
        
        # 添加评价
        if predicted_score >= 4.5:
            comment = "强烈推荐！这可能是一部非常出色的作品。"
        elif predicted_score >= 4.0:
            comment = "值得一看！这可能是一部很好的作品。"
        elif predicted_score >= 3.5:
            comment = "还不错，可以考虑观看。"
        elif predicted_score >= 3.0:
            comment = "一般，期望不要太高。"
        else:
            comment = "可能不太推荐，除非你对这类作品特别感兴趣。"
        
        print(f"{Fore.WHITE}评价: {Style.RESET_ALL}{comment}")
    else:
        print(f"{Fore.RED}预测失败，请检查输入数据或重试。{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")

def main():
    while True:
        print_header()
        print(f"{Fore.CYAN}欢迎使用豆瓣评分预测系统！{Style.RESET_ALL}")
        print(f"{Fore.CYAN}本系统可以根据影视作品的基本信息，预测您可能给出的评分。{Style.RESET_ALL}")
        print()
        
        print(f"{Fore.YELLOW}请选择操作：{Style.RESET_ALL}")
        print(f"1. 预测新影视作品评分")
        print(f"2. 退出程序")
        
        choice = input(f"\n{Fore.WHITE}请输入选项(1-2): {Style.RESET_ALL}")
        
        if choice == "1":
            # 获取用户输入
            movie_data = get_user_input()
            
            # 预测评分
            predicted_score = predict_rating(movie_data)
            
            # 显示结果
            display_result(movie_data, predicted_score)
            
            input(f"\n{Fore.CYAN}按回车键继续...{Style.RESET_ALL}")
        
        elif choice == "2":
            print(f"\n{Fore.CYAN}感谢使用豆瓣评分预测系统，再见！{Style.RESET_ALL}")
            break
        
        else:
            print(f"\n{Fore.RED}无效选项，请重新选择{Style.RESET_ALL}")
            input(f"{Fore.CYAN}按回车键继续...{Style.RESET_ALL}")

if __name__ == "__main__":
    main() 