@echo off
rem 设置控制台代码页为UTF-8
chcp 65001 > nul
title 豆瓣评分预测系统
color 0F

echo ================================================
echo            豆瓣评分预测系统 - 启动中
echo ================================================
echo.

rem 使用pythonw来避免控制台编码问题
start cmd /k "python -X utf8 -u src/app.py"

exit 