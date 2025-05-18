@echo off
rem 设置控制台代码页为UTF-8
chcp 65001 > nul
title 豆瓣评分预测系统
color 0F

echo ================================================
echo            豆瓣评分预测系统 - 启动中
echo ================================================
echo.

rem 使用python -u选项禁用输出缓冲
python -u src/app.py

echo.
echo 程序已退出
pause > nul 