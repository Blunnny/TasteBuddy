import os
import joblib
import sys
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import numpy as np

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    # 创建models目录（如果不存在）
    os.makedirs("models", exist_ok=True)
    
    print("加载数据...")
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
    
    # 确定特征列
    feature_columns = [col for col in encoded_df.columns if col not in ['title', 'watch_time', 'director', 'cast', 'user_score']]
    
    # 创建特征矩阵 X 和标签向量 y
    X = encoded_df[feature_columns]
    y = encoded_df['user_score']
    
    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 处理缺失值
    imputer = SimpleImputer(strategy='mean')
    X_train = imputer.fit_transform(X_train)
    X_test = imputer.transform(X_test)
    
    print("训练模型...")
    # 训练岭回归模型
    best_ridge = Ridge(alpha=10.0)
    best_ridge.fit(X_train, y_train)
    
    # 训练决策树模型
    best_dt = DecisionTreeRegressor(max_depth=5, min_samples_leaf=5, min_samples_split=2, random_state=42)
    best_dt.fit(X_train, y_train)
    
    # 训练随机森林模型
    best_rf = RandomForestRegressor(n_estimators=200, max_depth=5, min_samples_leaf=5, 
                                    min_samples_split=2, random_state=42)
    best_rf.fit(X_train, y_train)
    
    print("保存模型...")
    # 保存模型
    joblib.dump(best_ridge, "models/best_ridge.joblib")
    joblib.dump(best_dt, "models/best_dt.joblib")
    joblib.dump(best_rf, "models/best_rf.joblib")
    
    # 保存特征处理器
    joblib.dump(imputer, "models/imputer.joblib")
    
    print("模型保存完成！")
    print("保存的模型文件:")
    print("- models/best_ridge.joblib")
    print("- models/best_dt.joblib")
    print("- models/best_rf.joblib")
    print("- models/imputer.joblib")

if __name__ == "__main__":
    main() 