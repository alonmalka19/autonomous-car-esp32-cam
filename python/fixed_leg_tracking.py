print("🚀 Fixed Leg Tracking - Working baseline with minimal optimizations")
import cv2
import numpy as np
import requests
import time
import torch
from ultralytics import YOLO
import threading
import queue

# Configuration - using working IP addresses
ESP32_IP = "http://192.168.1.177"
CAMERA_URL = "http://192.168.1.116:8080/shot.jpg"
MODEL_PATH = "best_mylegs_v5.pt"

# Performance optimization settings
CAMERA_QUALITY = 60        # איכות מצלמה מופחתת לביצועים
MAX_FRAME_WIDTH = 640      # רזולוציה מקסימלית
INFERENCE_SIZE = 320       # גודל מהיר יותר ל-YOLO

# Display optimization settings
DISPLAY_WIDTH = 480        # חלון תצוגה קטן יותר לביצועים
DISPLAY_HEIGHT = 360       # יחס 4:3 סטנדרטי

# Load model - keep it simple like original
model = YOLO(MODEL_PATH)

# GPU status check (don't force device to avoid camera freezing)
if torch.cuda.is_available():
    print(f"🚀 GPU Available: {torch.cuda.get_device_name(0)}")
    print(f"📊 CUDA Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    print("📝 Model will use YOLO's default device handling")
else:
    print("⚠️ CUDA not available - running on CPU")

# Find MY_LEGS class ID from the model (same as original)
names = model.names
MY_LEGS_ID = None
for k, v in names.items():
    if 'my_legs' in v.lower():
        MY_LEGS_ID = k
        break

if MY_LEGS_ID is None:
    MY_LEGS_ID = 0  # fallback to first class

print(f"🎯 Using MY_LEGS_ID = {MY_LEGS_ID} ('{names[MY_LEGS_ID]}')")

# Tracking variables (exact same as original working code)
selected_class = MY_LEGS_ID  # Always track my_legs instead of auto-selecting
last_position = None
prev_gray = None
tracking_mode = None
last_seen_direction = "left"
consecutive_yolo_misses = 0
YOLO_MISS_LIMIT = 3
AREA_STOP_THRESHOLD = 70000

# Non-blocking search timing
search_start_time = None
search_delay = 0.8  # seconds to wait between search rotations (slower search)

# Original functions (unchanged)
def is_leg_shape(x1, y1, x2, y2):
    width = x2 - x1
    height = y2 - y1
    return height > 1.8 * width

def safe_sleep(duration):
    start = time.time()
    while time.time() - start < duration:
        key = cv2.waitKey(1)
        if key == ord('q'):
            exit()

# ESP32 command queue to prevent thread flooding
esp32_command_queue = queue.Queue(maxsize=10)
esp32_worker_running = True

def stop_esp32_worker():
    """Function to stop the ESP32 worker thread"""
    global esp32_worker_running
    esp32_worker_running = False

def _esp32_worker_thread():
    """Single worker thread for all ESP32 commands"""
    while esp32_worker_running:
        try:
            command, duration = esp32_command_queue.get(timeout=0.5)
            if command is None:  # Shutdown signal
                break
                
            try:
                response = requests.get(f"{ESP32_IP}/{command}", timeout=0.8)
                print(f"🎮 {command} -> {response.status_code}")
                if duration > 0:
                    time.sleep(duration)
                    requests.get(f"{ESP32_IP}/stop", timeout=0.8)
            except requests.exceptions.Timeout:
                print(f"🎮 Timeout: {command}")
            except requests.exceptions.ConnectionError:
                print(f"🎮 Connection failed: {ESP32_IP}/{command}")
            except Exception as e:
                print(f"🎮 ESP32 error: {e}")
                
        except queue.Empty:
            continue

def send_esp32_command(command, duration=0):
    """Non-blocking ESP32 command using queue - prevents thread flooding"""
    try:
        esp32_command_queue.put_nowait((command, duration))
    except queue.Full:
        print(f"🎮 Command queue full, dropping: {command}")

# Start single ESP32 worker thread
esp32_worker = threading.Thread(target=_esp32_worker_thread, daemon=True)
esp32_worker.start()

# Test ESP32 connection at startup
print("🔌 Testing ESP32 connection...")
send_esp32_command("stop")

lost_tracking = False
cv2.namedWindow("Fixed Leg Tracking")
cv2.resizeWindow("Fixed Leg Tracking", DISPLAY_WIDTH, DISPLAY_HEIGHT)  # חלון בגודל קבוע

print("🎯 Starting fixed tracking loop...")

try:
    while True:
        loop_start = time.time()
        
        try:
            # Optimized camera capture with quality control
            camera_url_optimized = f"{CAMERA_URL}?quality={CAMERA_QUALITY}"
            resp = requests.get(camera_url_optimized, timeout=0.4)
            img_arr = np.array(bytearray(resp.content), dtype=np.uint8)
            frame = cv2.imdecode(img_arr, -1)
            
            # Resize frame if too large for better performance
            if frame.shape[1] > MAX_FRAME_WIDTH:
                height, width = frame.shape[:2]
                scale = MAX_FRAME_WIDTH / width
                new_width = MAX_FRAME_WIDTH
                new_height = int(height * scale)
                frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # YOLO inference with optimized size for better performance
            # Using conf=0.3, imgsz for consistent performance, verbose=False to reduce warnings
            results = model(frame, conf=0.3, imgsz=INFERENCE_SIZE, verbose=False)[0]
            boxes = results.boxes

            selected_box = None
            min_dist = float('inf')
            found_by_yolo = False

            # Original detection logic (UNCHANGED)
            if selected_class is not None and boxes is not None:
                for box in boxes:
                    cls = int(box.cls[0])
                    if cls == selected_class:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2

                        if cx < frame.shape[1] // 2:
                            last_seen_direction = "right"
                        else:
                            last_seen_direction = "left"

                        if last_position is not None:
                            dist = np.linalg.norm(last_position[0] - [cx, cy])
                            if dist < min_dist:
                                min_dist = dist
                                selected_box = (x1, y1, x2, y2)
                                last_position = np.array([[cx, cy]], dtype=np.float32)
                                tracking_mode = "yolo"
                                found_by_yolo = True
                                lost_tracking = False
                        else:
                            # First detection
                            last_position = np.array([[cx, cy]], dtype=np.float32)
                            selected_box = (x1, y1, x2, y2)
                            tracking_mode = "yolo"
                            found_by_yolo = True
                            lost_tracking = False

                if found_by_yolo:
                    consecutive_yolo_misses = 0
                    search_start_time = None  # Reset search timer when target found
                else:
                    consecutive_yolo_misses += 1

            # Original optical flow fallback (UNCHANGED)
            if not found_by_yolo and consecutive_yolo_misses < YOLO_MISS_LIMIT and last_position is not None and prev_gray is not None:
                new_pos, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, last_position, None,
                                                               winSize=(15, 15), maxLevel=2,
                                                               criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
                if status[0][0] == 1:
                    last_position = new_pos
                    cx, cy = int(last_position[0][0]), int(last_position[0][1])
                    w, h = 100, 160
                    x1, y1, x2, y2 = cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2

                    if is_leg_shape(x1, y1, x2, y2):
                        selected_box = (x1, y1, x2, y2)
                        tracking_mode = "flow"
                        lost_tracking = False
                    else:
                        selected_box = None
                        lost_tracking = True

            # Original control logic with enhanced ESP32 communication
            if selected_box:
                x1, y1, x2, y2 = selected_box
                cx = (x1 + x2) // 2
                frame_center = frame.shape[1] // 2
                error = cx - frame_center
                max_error = frame.shape[1] // 2
                normalized_error = min(abs(error) / max_error, 1.0)
                pulse_duration = 0.02  # אורך קצר מאוד כדי לא לחלוף על המטרה

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                
                # FPS calculation for display
                loop_time = time.time() - loop_start
                current_fps = 1.0 / loop_time if loop_time > 0 else 0
                cv2.putText(frame, f"MY_LEGS ({tracking_mode}) - {current_fps:.1f}FPS", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if cx < frame.shape[1] * 0.25:
                    send_esp32_command("left", pulse_duration)
                elif cx > frame.shape[1] * 0.75:
                    send_esp32_command("right", pulse_duration)
                else:
                    send_esp32_command("forward")

                if (x2 - x1) * (y2 - y1) > AREA_STOP_THRESHOLD:
                    send_esp32_command("stop")

            elif selected_class is not None and consecutive_yolo_misses >= YOLO_MISS_LIMIT:
                lost_tracking = True
                loop_time = time.time() - loop_start
                current_fps = 1.0 / loop_time if loop_time > 0 else 0
                cv2.putText(frame, f"MY_LEGS lost - searching... {current_fps:.1f}FPS", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                
                # Non-blocking search timing - slower and shorter rotations
                current_time = time.time()
                if search_start_time is None:
                    # Start search sequence with shorter rotation duration
                    search_start_time = current_time
                    if last_seen_direction == "left":
                        send_esp32_command("right", 0.08)  # קצר יותר - סיבוב קל
                    else:
                        send_esp32_command("left", 0.08)   # קצר יותר - סיבוב קל
                elif current_time - search_start_time >= search_delay:
                    # Reset for next search cycle
                    search_start_time = None
                    lost_tracking = False

            prev_gray = gray.copy()
            
            # Create optimized display frame (smaller for better performance)
            display_frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT), interpolation=cv2.INTER_LINEAR)
            cv2.imshow("Fixed Leg Tracking", display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        except requests.exceptions.RequestException as e:
            print(f"📷 Camera error: {e}")
            time.sleep(0.1)
        except Exception as e:
            print(f"❌ Processing error: {e}")

except KeyboardInterrupt:
    print("\n🛑 Shutting down...")

finally:
    # Cleanup
    try:
        stop_esp32_worker()  # Use function to avoid global syntax issues
        
        send_esp32_command("stop")
        print("🛑 Final stop command sent")
        # Signal worker thread to stop
        esp32_command_queue.put((None, 0))
    except:
        pass
    
    # Wait for worker thread to finish
    esp32_worker.join(timeout=2.0)
    cv2.destroyAllWindows()
    print("🏁 Fixed tracking stopped")