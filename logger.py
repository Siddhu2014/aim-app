import time
import math
import pandas as pd
from pynput import mouse

# Initialize data storage arrays
timestamps, player_x_coords, player_y_coords, target_x_coords, target_y_coords = [], [], [], [], []
start_time = time.time()

print("🎯 Aim Telemetry Logger Initialized!")
print("👉 Move your mouse to track the imaginary moving target... Recording for 5 seconds.")
print("--- Starting in 3... 2... 1... ---")
time.sleep(3)

# Establish a standard sampling rate (50Hz / every 0.02 seconds)
sample_interval = 0.02 
last_sample_time = time.time()

# Define an algorithmic moving target pathway (simulating a smooth cross-screen vector)
def get_target_position(elapsed):
    # Target moves smoothly across the screen over a 5-second window
    t_x = 100 + (elapsed * 150)  
    t_y = 200 + (math.sin(elapsed * 3) * 100)
    return t_x, t_y

def on_move(x, y):
    global last_sample_time
    current_time = time.time()
    elapsed = current_time - start_time
    
    # Cap recording session at 5 seconds
    if elapsed > 5.0:
        return False # Stops the mouse listener loop
        
    # Only capture data points at our specified hardware sample interval
    if current_time - last_sample_time >= sample_interval:
        timestamps.append(round(elapsed, 3))
        player_x_coords.append(x)
        player_y_coords.append(y)
        
        # Calculate where the moving target was supposed to be at this exact millisecond
        t_x, t_y = get_target_position(elapsed)
        target_x_coords.append(round(t_x, 2))
        target_y_coords.append(round(t_y, 2))
        
        last_sample_time = current_time

# Activate the low-level background hardware listener hooking into system inputs
with mouse.Listener(on_move=on_move) as listener:
    listener.join()

# Package captured arrays into a clean pandas dataframe structure
log_df = pd.DataFrame({
    "Timestamp_Sec": timestamps,
    "Target_X": target_x_coords,
    "Target_Y": target_y_coords,
    "Player_X": player_x_coords,
    "Player_Y": player_y_coords
})

# Compile and export directly to a user-friendly CSV structure
output_filename = "target_tracking.csv"
log_df.to_csv(output_filename, index=False)

print("\n🚀 Tracking session complete!")
print(f"📁 File saved successfully as: '{output_filename}'")
print("📥 Upload this file directly to your web dashboard!")
