import pandas as pd
import numpy as np
import os
import sys
import io
import locale
from colorama import init, Fore, Back, Style

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.load_models import load_models, predict_with_ensemble

# 初始化colorama
init()

# 设置控制台编码
if sys.platform == 'win32':
    # 对于Windows系统
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    # 尝试设置控制台代码页
    os.system('chcp 65001 > nul')

def main():
    print(f"{Fore.CYAN}加载模型...{Style.RESET_ALL}")
    models = load_models()
    
    print(f"{Fore.CYAN}加载测试数据...{Style.RESET_ALL}")
    try:
        # 加载 One-Hot 编码后的数据
        encoded_df = pd.read_json("data/onehot_encoded_data.json", orient="records", encoding="utf-8")
        
        # 创建特征
        encoded_df['director_count'] = encoded_df['director'].apply(lambda x: len(eval(x)) if isinstance(x, str) else len(x) if isinstance(x, list) else 0)
        encoded_df['cast_count'] = encoded_df['cast'].apply(lambda x: len(eval(x)) if isinstance(x, str) else len(x) if isinstance(x, list) else 0)
        encoded_df['douban_score'] = encoded_df['douban_score'].fillna(encoded_df['douban_score'].mean())
        encoded_df['watch_time'] = pd.to_datetime(encoded_df['watch_time'])
        encoded_df['watch_year'] = encoded_df['watch_time'].dt.year
        encoded_df['watch_quarter'] = encoded_df['watch_time'].dt.quarter
        encoded_df['title_length'] = encoded_df['title'].str.split().str.len()
        
        # 选择前5个样本作为示例
        sample_df = encoded_df.head(10)
        
        # 确定特征列
        feature_columns = [col for col in encoded_df.columns if col not in ['title', 'watch_time', 'director', 'cast', 'user_score']]
        
        # 提取特征和真实评分
        X_sample = sample_df[feature_columns]
        y_true = sample_df['user_score']
        
        print(f"\n{Fore.GREEN}【预测结果】{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
        header = f"{Fore.WHITE}{Back.BLUE}{'电影名称':<30} {'豆瓣评分':<10} {'真实评分':<10} {'预测评分':<10} {'差异':<10}{Style.RESET_ALL}"
        print(header)
        print(f"{Fore.YELLOW}{'-'*60}{Style.RESET_ALL}")
        
        # 进行预测
        y_pred = predict_with_ensemble(X_sample, models)
        
        # 显示预测结果
        for i, (title, douban, true_score, pred_score) in enumerate(zip(sample_df['title'], sample_df['douban_score'], y_true, y_pred)):
            diff = true_score - pred_score
            # 根据差异大小选择颜色
            if abs(diff) < 0.2:
                color = Fore.GREEN  # 预测非常准确
            elif abs(diff) < 0.5:
                color = Fore.YELLOW  # 预测较为准确
            else:
                color = Fore.RED  # 预测差异较大
                
            print(f"{color}{title:<30} {douban:<10.1f} {true_score:<10.1f} {pred_score:<10.2f} {diff:<10.2f}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
        
        # 计算平均绝对误差
        mae = np.mean(np.abs(y_true - y_pred))
        print(f"\n{Fore.CYAN}平均绝对误差 (MAE): {Fore.WHITE}{mae:.2f}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}发生错误: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        
if __name__ == "__main__":
    main() 