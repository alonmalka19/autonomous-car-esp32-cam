# Hardware and Wiring

The autonomous car uses the following components. Adjust the parts as necessary for your own build.

| Component | Description |
|---|---|
| **ESP32-CAM** | A microcontroller board with Wi-Fi. In this project the built-in camera is **not used**. The ESP32 handles the motor control via HTTP commands. |
| **Smartphone (IP Webcam)** | A smartphone running the IP Webcam app provides the live video stream. Make sure the phone is on the same Wi-Fi network as the host computer so that the Python script can read the video feed over HTTP. |
| **L298N motor driver** | Dual H-bridge driver for controlling two DC motors. Connect the IN1/IN2 pins to the ESP32's GPIO pins and the motor outputs to the motors. |
| **Four DC motors (two per side) with wheels** | Provide movement for the car. Each side (two motors) connects to one channel of the motor driver. |
| **Battery pack (7 V – 12 V)** | Powers the motors and motor driver. Use a separate 5 V regulator for the ESP32 if necessary. |

## Wiring overview

1. Connect the ESP32‑CAM's **3V3** and **GND** pins to a stable 3.3 V power source (do not power directly from the motor battery). Some boards have a built‑in regulator.
2. Connect the ESP32's **GPIO** pins to the **IN1**, **IN2**, **IN3** and **IN4** pins of the L298N driver. The exact pin numbers should match those used in `esp32.ino`.
3. Connect the motors' leads to the **OUT1/OUT2** and **OUT3/OUT4** terminals on the L298N.
4. Power the L298N with the battery pack. Ensure that the motor driver's ground is connected to the ESP32 ground.
5. The smartphone is **not wired** to the ESP32. It only needs to stream video using the IP Webcam app over the local network.

Refer to the schematic diagrams in this folder for a visual representation of the wiring.
