# Autonomous Car with ESP32-CAM & Python

This project implements a small autonomous car controlled by an ESP32-CAM microcontroller and a Python script running on a host computer.  The Python script communicates with the ESP32 over HTTP commands and uses a custom YOLO model to detect and track a pair of legs in the camera feed.  When the legs move, the car follows them by sending motion commands to the motors via the ESP32.

## Features

- **Real-time video streaming** from the ESP32-CAM.
- **Object detection** using a custom YOLO model trained to recognize legs.
- **Autonomous motion control** over HTTP: the Python script sends commands such as `forward`, `left`, `right`, and `stop` to the ESP32.
- **Optical-flow fallback**: if YOLO temporarily loses the target, the script uses optical flow to continue tracking.
- **Planned search behaviour** when the target is lost: the car rotates slowly until the legs are detected again.

## Directory layout

The repository is organised as follows:

```
.
├── firmware/                # Arduino/ESP32 firmware code
│   └── esp32.ino           # Main sketch for the ESP32-CAM
├── python/                  # Host-side Python code
│   ├── fixed_leg_tracking.py  # Main script for object detection and motion control
│   ├── requirements.txt    # Python dependencies
│   └── models/
│       └── best_mylegs_v5.pt  # Trained YOLO weights file
├── docs/                    # Project documentation
│   ├── setup.md            # Instructions to set up and run the project
│   └── hardware.md         # Hardware connections and bill of materials
├── .gitignore              # Files and folders to exclude from version control
├── LICENSE                 # MIT open-source licence
└── README.md               # This file
```

## Getting started

1. **Clone this repository** (or download the files).  Make sure you have Python 3 installed on your machine.

2. **Install Python dependencies**:

   ```bash
   cd python
   pip install -r requirements.txt
   ```

3. **Flash the ESP32 firmware**:  open the `firmware/esp32.ino` sketch in the Arduino IDE or PlatformIO, configure your Wi-Fi credentials and IP addresses, and upload it to your ESP32-CAM.

4. **Run the Python script**:  modify the IP addresses in `python/fixed_leg_tracking.py` to match your ESP32-CAM and computer network, then execute:

   ```bash
   python fixed_leg_tracking.py
   ```

You should see the camera feed with a bounding box drawn around the detected legs, and the car will move to follow the target.

## Hardware

See `docs/hardware.md` for a list of components and wiring instructions.  In general, you will need an ESP32-CAM, an L298N or similar motor driver, two DC motors with wheels, a battery pack, and optionally an ultrasonic sensor for obstacle avoidance.

## License

This project is licensed under the MIT License – see the `LICENSE` file for details.
