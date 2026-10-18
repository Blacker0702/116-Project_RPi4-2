# RPi4-2：水果/食物影像辨識（Fruit Detect）與重量感測 回傳
 
> Diet JARVIS 的「看」：在 Raspberry Pi 4 上以 YOLO（ONNX 模型）即時辨識鏡頭畫面，將辨識到的類別名稱透過 UART 序列埠送出。
 
---

## 功能概覽
 
1. 以 USB 鏡頭擷取即時影像（640 × 480）。
2. 使用 Ultralytics YOLO 載入 ONNX 模型 `see_models/fruit_detect_320.onnx` 進行推論。
3. 將偵測框畫在畫面上，並顯示在 RPi4 所接的螢幕。
4. 有偵測到物件時，取**第一個**偵測結果（通常為信心度最高者）的類別名稱，連同重量欄位（開發中，暫為 `-9999`）透過 UART 輸出。
```text
鏡頭 ▶ YOLO（ONNX）推論 ▶ 標註畫面 ▶ 顯示於螢幕
                    │
                    └▶ 取第一個偵測物件（通常為信心度最高者）的類別 ▶ UART（/dev/serial0, 9600）
```
 
## 檔案說明
 
| 檔案 | 說明 |
|------|------|
| `Fruit_detect.py` | 即時辨識主程式 |
| `Remote_ssh.sh` | 從 VS Code 遠端終端機啟動主程式的腳本，讓畫面顯示在 RPi4 的螢幕上 |
| `see_models/fruit_detect_320.onnx` | YOLO ONNX 模型（需自行放置於此路徑） |
 
## 硬體與環境
 
| 項目 | 說明 |
|------|------|
| 裝置 | Raspberry Pi 4B（已登入桌面，螢幕上看得到桌面） |
| 鏡頭 | 接在 `VideoCapture(0)` 的攝影機 |
| 序列埠 | `/dev/serial0`（GPIO 硬體序列埠），若使用 USB 轉 TTL 模組，通常改為 `/dev/ttyUSB0` |
| 鮑率 | 9600 |
| Python 套件 | `opencv-python`、`pyserial`、`ultralytics`，以及載入 ONNX 所需的 `onnxruntime` |
 
## UART 輸出格式
 
每次有偵測到物件，送出一行文字（以換行 `\n` 結尾）：
 
```text
['類別名稱', -9999]
```
 
| 欄位 | 說明 |
|------|------|
| 類別名稱 | 第一個偵測框（通常為信心度最高者）的類別，例如 `paper` |
| `-9999` | 重量感測的數值欄位。重量感測功能目前還在製作中，因此程式暫時固定送出 `-9999` 作為預設值 |
 
## 執行方式
 
### 直接在 RPi4 上執行
 
```bash
python3 Fruit_detect.py
```
 
### 從 VS Code 遠端終端機執行（建議）
 
```bash
bash Remote_ssh.sh
```
 
`Remote_ssh.sh` 會做三件事：
 
1. 切換到腳本所在資料夾。
2. 強制設定 `DISPLAY=:0`、`QT_QPA_PLATFORM=xcb`（若有 `~/.Xauthority` 也一併設定），讓 SSH 連線的程式把視窗顯示在 RPi4 本機螢幕，而不是遠端終端機。
3. 以 `exec python3 Fruit_detect.py` 啟動辨識，並可帶入額外參數。
> 前置條件：RPi4 已登入桌面。
 
### 停止
 
- 在顯示畫面的視窗按 `q`。
- 或在 VS Code 終端機按 `Ctrl + C`。
結束時程式會自動釋放鏡頭、關閉序列埠與視窗。
 
## 開發進度
 
- [x] 水果／食物影像辨識
- [x] UART 輸出類別名稱
- [ ] 重量感測（製作中）：完成後，將取代目前固定的 `-9999`
