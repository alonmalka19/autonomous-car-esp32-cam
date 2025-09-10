# Setup Instructions

These instructions describe how to configure and run the autonomous car project.

## Prerequisites

- **ESP32-CAM development board**
- **Host computer** running Python 3 (Linux, macOS or Windows)
- **Wi-Fi network** accessible to both the ESP32 and the host computer

## Firmware setup

1. Install the [Arduino IDE](https://www.arduino.cc/en/software) or [PlatformIO](https://platformio.org/) on your computer.
2. Open `firmware/esp32.ino` in your chosen IDE.
3. Edit the sketch to set your Wi-Fi SSID and password.  You may also need to adjust the IP addresses used for the HTTP API.
4. Connect the ESP32-CAM to your computer via USB and flash the firmware.

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
4. Edit `fixed_leg_tracking.py` to set the correct IP addresses for your ESP32-CAM and streaming server.
5. Run the script:

   ```bash
   python fixed_leg_tracking.py
   ```

The script will open a window showing the camera feed and draw bounding boxes around detected legs.  When the legs move, the script sends commands to the ESP32 to drive the motors accordingly.
