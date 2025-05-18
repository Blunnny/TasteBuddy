@echo off
rem 设置控制台代码页为UTF-8
chcp 65001 > nul
title 测试预测功能
color 0F

echo ================================================
echo                测试预测功能
echo ================================================
echo.

rem 运行Python脚本
python -u src/test_prediction.py

echo.
echo 按任意键退出...
pause > nul 