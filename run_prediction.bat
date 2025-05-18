@echo off
chcp 65001 > nul
echo ================================================
echo            豆瓣评分预测系统 - 示例运行
echo ================================================
echo.
python src/predict_example.py
echo.
echo 按任意键退出...
pause > nul 