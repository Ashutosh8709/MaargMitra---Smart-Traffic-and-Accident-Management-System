import os
os.environ["STREAMLIT_DISABLE_WATCHDOG_WARNINGS"] = "true"
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import cv2
import streamlit as st
import numpy as np
import time
from ultralytics import YOLO
def show_speed_monitor_page():
# Load YOLOv8 Model
    model =YOLO("https://github.com/Ashutosh8709/Traffic-and-Accident-Management-System/releases/download/v1.0/yolov8nMytrained.pt")

# Streamlit UI
    st.title("🚦 Real-Time Traffic & Speed Monitoring 🚗")
    # Example of adding a unique key to the file_uploader
    video_file = st.file_uploader("📂 Upload a Video", type=["mp4", "avi", "mov"])


    if video_file:
        tfile = open("temp_video.mp4", "wb")
        tfile.write(video_file.read())
        tfile.close()

        cap = cv2.VideoCapture("temp_video.mp4")
        frame_placeholder = st.empty()
    
    # Sidebar placeholders
        vehicle_count_placeholder = st.sidebar.empty()
        avg_speed_placeholder = st.sidebar.empty()
        congestion_placeholder = st.sidebar.empty()
        overspeeding_placeholder = st.sidebar.empty()

    # Speed tracking variables
        object_positions = {}  # Store previous positions
        object_speeds = {}  # Store speeds
        overspeeding_vehicles = set()
        speed_limit = 50  # Speed limit in km/h

        pixels_to_meters = 0.001  # Adjust based on real-world scenario
        min_movement_threshold = 0  # Ignore small movements
        prev_time = time.time()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            current_time = time.time()
            time_elapsed = current_time - prev_time
            prev_time = current_time

            vehicle_count = 0
            total_speed = 0
            overspeeding_vehicles.clear()

            results = model(frame)

            new_positions = {}  # Store latest positions

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

                # Assign ID based on center position
                    object_id = None
                    min_dist = float('inf')

                # Find closest previous position to track object
                    for prev_id, (prev_x, prev_y) in object_positions.items():
                        dist = np.sqrt((center_x - prev_x) ** 2 + (center_y - prev_y) ** 2)
                        if dist < min_dist and dist < 50:  # Threshold for object tracking
                            min_dist = dist
                            object_id = prev_id

                    if object_id is None:
                        object_id = len(object_positions) + 1  # Assign new ID

                    new_positions[object_id] = (center_x, center_y)

                # Speed Calculation
                    if object_id in object_positions:
                        prev_x, prev_y = object_positions[object_id]
                        distance_px = np.sqrt((center_x - prev_x) ** 2 + (center_y - prev_y) ** 2)
                        distance_m = distance_px * pixels_to_meters

                        if time_elapsed > 0 and distance_px > min_movement_threshold:
                            speed = (distance_m / time_elapsed) * 3.6  # Convert m/s to km/h
                        
                        # Smooth speed to avoid extreme jumps
                            object_speeds[object_id] = 0.8 * object_speeds.get(object_id, speed) + 0.2 * speed
                        else:
                            object_speeds[object_id] = 0  # Stopped vehicle

                    else:
                        object_speeds[object_id] = 0  # Default speed for new vehicles

                    total_speed += object_speeds[object_id]
                    vehicle_count += 1

                # Check for overspeeding
                    if object_speeds[object_id] > speed_limit:
                        overspeeding_vehicles.add(f"Vehicle {object_id}: {object_speeds[object_id]:.1f} km/h")

                # Draw bounding box and speed
                    label = f"{object_speeds[object_id]:.1f} km/h"
                    color = (0, 255, 0) if object_speeds[object_id] <= speed_limit else (0, 0, 255)  # Red if overspeeding
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            object_positions = new_positions  # Update stored positions

        # Compute average speed
            avg_speed = total_speed / max(1, vehicle_count)

        # Display updated values in the sidebar
            vehicle_count_placeholder.markdown(f"### 🚗 Total Vehicles: **{vehicle_count}**")
            avg_speed_placeholder.markdown(f"### 🏎️ Avg Speed: **{avg_speed:.1f} km/h**")
            congestion_placeholder.markdown(f"### 🚦 Congestion Level: {'Low 🟢' if vehicle_count < 10 else 'Moderate 🟡' if vehicle_count < 30 else 'High 🔴'}")

        # Display overspeeding vehicles
            if overspeeding_vehicles:
                overspeeding_placeholder.markdown("### 🚨 Overspeeding Vehicles:\n" + "\n".join(overspeeding_vehicles))
            else:
                overspeeding_placeholder.markdown("### ✅ No Overspeeding Vehicles")

        # Display video
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame, channels="RGB", use_container_width=True)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        st.success("✅ Video Processing Complete")

    cv2.destroyAllWindows()
# show_speed_monitor_page()
