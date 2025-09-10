# Autonomous Car with ESP32-CAM & Python

This project implements a small autonomous car controlled by an ESP32‑CAM board (used as a microcontroller) and a Python script running on a host computer.  A smartphone running the **IP Webcam** app provides the video feed, streaming to the host computer over the local network.  The Python script communicates with the ESP32 over HTTP commands and uses a custom YOLO model to detect and track a pair of legs in the camera feed.  When the legs move, the car follows them by sending motion commands to the motors via the ESP32.

## Features

- **Real‑time video streaming** from a smartphone via **IP Webcam** (the ESP32’s on‑board camera is not used).
- **Object detection** using a custom YOLO model trained to recognise legs.
- **Autonomous motion control** over HTTP: the Python script sends commands such as `forward`, `left`, `right` and `stop` to the ESP32.
- **Optical‑flow fallback**: if YOLO temporarily loses the target, the script uses optical flow to continue tracking.
- **Planned search behaviour** when the target is lost: the car rotates slowly until the legs are detected again.

## Directory layout

The repository is organised as follows:

```
├── firmware/                 # Arduino/ESP32 firmware code
│   └── esp32.ino            # Main sketch for the ESP32‑CAM
├── python/                   # Host‑side Python code
│   ├── fixed_leg_tracking.py # Main script for object detection and motion control
│   ├── requirements.txt     # Python dependencies
│   └── models/              # Model files
│       └── best_mylegs_v5.pt  # Trained YOLO weights file
├── docs/                     # Project documentation
│   ├── setup.md             # Instructions to set up and run the project
│   └── hardware.md          # Hardware connections and bill of materials
├── .gitignore                # Files and folders to exclude from version control
├── LICENSE                   # MIT open‑source licence
└── README.md                 # This file
```

## Getting started

1. **Clone this repository** (or download the files).  Make sure you have Python 3 installed on your machine.

2. **Install Python dependencies**:

```bash
cd python
pip install -r requirements.txt
```

3. **Flash the ESP32 firmware**: open the `firmware/esp32.ino` sketch in the Arduino IDE or PlatformIO, configure your Wi‑Fi credentials and IP addresses, and upload it to your ESP32 board.

4. **Run the Python script**: modify the IP addresses in `python/fixed_leg_tracking.py` to match your ESP32 and streaming server (smartphone) and your computer network, then execute:

```bash
python fixed_leg_tracking.py
```

You should see the camera feed with a bounding box drawn around the detected legs, and the car will move to follow the target.

## Hardware

See `docs/hardware.md` for a list of components and wiring instructions.  In general, you will need:

- An **ESP32‑CAM** board (used only as a microcontroller; its built‑in camera is not used)
- A smartphone with the **IP Webcam** app installed to provide the video stream
- An **L298N** or similar motor driver
- **Four DC motors (two per side)** with wheels
- A **battery pack**

## License

This project is licensed under the MIT License – see the `LICENSE` file for details.