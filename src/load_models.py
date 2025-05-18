import joblib
import os
import numpy as np
import pandas as pd

def load_models(models_dir="models"):
    """
    加载保存的模型和预处理器
    
    参数:
    models_dir: 保存模型的目录路径
    
    返回:
    模型和预处理器的字典
    """
    models = {}
    
    # 检查模型文件是否存在
    model_files = {
        "ridge": "best_ridge.joblib",
        "dt": "best_dt.joblib",
        "rf": "best_rf.joblib",
        "imputer": "imputer.joblib",
        "feature_names": "feature_names.joblib"  # 添加特征名称文件
    }
    
    for model_name, file_name in model_files.items():
        file_path = os.path.join(models_dir, file_name)
        if os.path.exists(file_path):
            models[model_name] = joblib.load(file_path)
        else:
            print(f"警告: 模型文件 {file_path} 不存在")
    
    return models

def predict_with_ensemble(X, models):
    """
    使用集成模型进行预测
    
    参数:
    X: 特征数据
    models: 从load_models()加载的模型字典
    
    返回:
    预测评分
    """
    try:
        # 如果模型中有特征名称列表，确保特征顺序一致
        if "feature_names" in models and isinstance(models["feature_names"], list):
            print(f"确保特征顺序一致...")
            feature_names = models["feature_names"]
            
            # 检查是否所有特征都存在
            missing_features = [f for f in feature_names if f not in X.columns]
            if missing_features:
                print(f"警告: 缺少以下特征: {missing_features[:5]}...")
                # 添加缺失的特征，填充为0
                for feature in missing_features:
                    X[feature] = 0
            
            # 检查是否有多余的特征
            extra_features = [f for f in X.columns if f not in feature_names]
            if extra_features:
                print(f"警告: 存在额外特征: {extra_features[:5]}...")
            
            # 按照训练时的特征顺序重排特征
            print(f"重排特征顺序...")
            X = X[feature_names]
        
        # 确保数据已经过预处理
        if "imputer" in models:
            print(f"应用特征填充...")
            X = models["imputer"].transform(X)
        
        # 获取各个模型的预测结果
        predictions = []
        
        if "ridge" in models:
            print(f"使用Ridge模型预测...")
            ridge_pred = models["ridge"].predict(X)
            predictions.append(ridge_pred)
        
        if "dt" in models:
            print(f"使用决策树模型预测...")
            dt_pred = models["dt"].predict(X)
            predictions.append(dt_pred)
        
        if "rf" in models:
            print(f"使用随机森林模型预测...")
            rf_pred = models["rf"].predict(X)
            predictions.append(rf_pred)
        
        # 如果没有模型可用，返回None
        if not predictions:
            print(f"错误: 没有可用的预测模型")
            return None
        
        # 计算集成预测结果（平均值）
        print(f"计算集成预测结果...")
        ensemble_pred = np.mean(predictions, axis=0)
        print(f"预测完成，结果: {ensemble_pred}")
        return ensemble_pred
    
    except Exception as e:
        print(f"预测过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # 测试加载模型
    models = load_models()
    print("成功加载的模型:")
    for model_name, model in models.items():
        print(f"- {model_name}: {type(model).__name__}") 