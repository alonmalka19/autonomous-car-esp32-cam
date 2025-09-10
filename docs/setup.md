# Setup Instructions

These instructions describe how to configure and run the autonomous car project.

## Prerequisites

- **ESP32‑CAM development board** – used as the microcontroller to control the motors. The built‑in camera on the board is **not** used.
- **Smartphone running IP Webcam** – provides the video stream to the Python script. Make sure the phone and host computer are on the same Wi‑Fi network.
- **Host computer** running Python 3 (Linux, macOS or Windows)
- **Wi‑Fi network** accessible to both the ESP32 and the host computer

## Firmware setup

1. Install the Arduino IDE or PlatformIO on your computer.
2. Open `firmware/esp32.ino` in your chosen IDE.
3. Edit the sketch to set your Wi‑Fi SSID and password. You may also need to adjust the IP addresses used for the HTTP API.
4. Connect the ESP32‑CAM to your computer via USB and flash the firmware.

## Python script

1. Navigate to the `python` directory in this repository:

```bash
cd python
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Copy the trained YOLO weights file (`best_mylegs_v5.pt`) into `python/models/`.

4. Edit `fixed_leg_tracking.py` to set the correct IP addresses for your ESP32 and the smartphone streaming server (IP Webcam).

5. Run the script:

```bash
python fixed_leg_tracking.py
```

The script will open a window showing the video feed from your smartphone and draw bounding boxes around detected legs. When the legs move, the script sends commands to the ESP32 to drive the motors accordingly.
