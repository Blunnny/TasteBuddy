@echo off
rem 设置控制台代码页为UTF-8
chcp 65001 > nul
title 保存特征名称顺序
color 0F

echo ================================================
echo            正在保存特征名称顺序
echo ================================================
echo.

rem 运行Python脚本
python -u src/save_feature_names.py

echo.
echo 按任意键退出...
pause > nul 