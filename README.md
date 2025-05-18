# 豆瓣评分预测系统

这是一个基于机器学习的豆瓣评分预测系统，可以根据影视作品的基本信息（如地区、类型、导演等）预测用户可能给出的评分。

## 功能特点

- 输入影视作品的基本信息，如片名、年份、地区、类型、导演、演员等
- 使用集成学习模型预测用户可能给出的评分（满分 5 分）
- 提供评分解释和观影建议
- 友好的命令行交互界面

## 系统要求

- Python 3.8+
- 依赖库：pandas, numpy, scikit-learn, colorama 等

## 安装方法

1. 克隆或下载本仓库
2. 安装依赖库：
   ```
   pip install -r requirements.txt
   ```
3. 保存特征名称（首次运行前需要执行）：
   ```
   python src/save_feature_names.py
   ```
   或者直接运行：
   ```
   save_feature_names.bat
   ```

## 使用方法

### Windows 用户

有多种方式运行程序：

1. **推荐方式**：双击运行`run_app_windows.bat`文件，这将在新的命令行窗口中以 UTF-8 模式启动 Python。

2. 双击运行`run_app.bat`文件。

3. 使用 Python 运行启动脚本：
   ```
   python run_app.py
   ```

### 其他系统用户

1. 在命令行中运行 Python 启动脚本：

   ```
   python run_app.py
   ```

2. 或者直接运行应用程序：
   ```
   python src/app.py
   ```

## 中文显示问题解决方案

如果你在 Windows 系统上遇到中文乱码问题，请尝试以下解决方案：

1. 使用`run_app_windows.bat`启动程序，它会在 UTF-8 模式下启动新的命令行窗口。

2. 手动设置命令行窗口的代码页为 UTF-8：

   ```
   chcp 65001
   ```

   然后运行：

   ```
   python -X utf8 -u src/app.py
   ```

3. 在 PowerShell 中，可以使用以下命令：
   ```
   [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
   python -X utf8 -u src/app.py
   ```

## 使用流程

1. 启动程序后，选择"1. 预测新影视作品评分"
2. 按照提示输入影视作品信息：
   - 片名
   - 年份
   - 豆瓣评分（可选）
   - 地区（从列表中选择）
   - 类型（从列表中选择）
   - 导演
   - 主要演员（可选）
3. 系统会加载模型并预测评分
4. 显示预测结果，包括预测评分和观影建议

或者直接运行`save_feature_names.bat`。

## 项目结构

- `src/` - 源代码目录
  - `app.py` - 主程序入口
  - `predict_example.py` - 预测示例代码
  - `load_models.py` - 模型加载和预测函数
  - `save_models.py` - 模型保存函数
- `models/` - 保存训练好的模型
- `data/` - 数据文件
  - `raw.xlsx` - 原始数据
  - `cleaned_data.json` - 清洗后的数据
  - `onehot_encoded_data.json` - One-Hot 编码后的数据
- `run_app.bat` - 启动应用程序的批处理文件
- `requirements.txt` - 依赖库列表

## 模型说明

本系统使用了多个机器学习模型进行集成预测：

- Ridge 回归
- 决策树
- 随机森林

这些模型通过平均预测结果来提供最终的评分预测。

## TODO

- 设计 GUI 界面
- 将文件打包为 exe 文件
- 优化模型。
