import cv2
import serial
from ultralytics import YOLO  # 這裡補上了 YOLO 的引用

# 初始化 UART (以樹莓派 GPIO 硬體序列埠 /dev/serial0 為例，鮑率設為 9600)
# 若是透過 USB 轉 TTL 模組，通常為 '/dev/ttyUSB0'
ser = serial.Serial(port="/dev/serial0", baudrate=9600, timeout=1)

# 載入 ONNX 模型
model = YOLO("see_models/fruit_detect_320.onnx")

# 開啟攝影機
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("無法開啟攝影機")
    exit()

print("開始即時串流辨識與 UART 輸出，按下 'q' 鍵離開...")

try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("無法讀取畫面")
            break

        # 進行推論
        results = model(frame, imgsz=480, verbose=False)
        annotated_frame = results[0].plot()

        # 解析辨識結果並透過 UART 輸出
        boxes = results[0].boxes
        if len(boxes) > 0:
            # 取得第一個偵測到的物件類別名稱
            cls_id = int(boxes[0].cls[0])
            class_name = model.names[cls_id]

            # 取得對應數值（範例中指定為整數，若無特別數值可帶入指定的 int，例如 -9999）
            val = -9999

            # 組合格式如 ['paper', -9999]
            output_data = f"['{class_name}', {val}]\n"

            # 寫入 UART (轉成 bytes 發送)
            ser.write(output_data.encode("utf-8"))
            print(f"已發送: {output_data.strip()}")

        # 顯示即時畫面
        cv2.imshow("Raspberry Pi YOLO ONNX + UART", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    ser.close()
    cv2.destroyAllWindows() 
