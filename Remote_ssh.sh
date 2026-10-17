#!/usr/bin/env bash
# run_detect.sh -- 在 RPi4 上（VS Code 終端機）執行，偵測畫面顯示在 RPi4 接的螢幕上
#
# 用法（在 leslie@L-rpi4B:~/SX$ 底下）：
#
# 停止：在 VS Code 終端機按 Ctrl+C。
# 前置條件：RPi4 已登入桌面（螢幕上看得到桌面）。

cd "$(dirname "$(readlink -f "$0")")" || exit 1

# VS Code 遠端終端機可能帶有自己的 DISPLAY，這裡強制導向 RPi 本機螢幕
export DISPLAY=:0
export QT_QPA_PLATFORM=xcb
[ -f "$HOME/.Xauthority" ] && export XAUTHORITY="$HOME/.Xauthority"

exec python3 Fruit_detect.py "$@"
# exec python3 M01_MIX.py "$@"



# bash Remote_ssh.sh
# source Svenv/bin/activate
# python Serial_feedback.py
# python F01_detect_test.py
# python W01_HX711_dev.py
