# Hanumanoid UDP test

import socket
import time
import numpy as np

# Configuration
JETSON_IP = "192.168.1.XXX" # <--- CHANGE THIS
PORT = 5005
TEST_DURATION = 10 # Seconds
FREQUENCY = 100    # 100Hz = 10ms loop
TIMEOUT = 0.05     # 50ms timeout for lost packets

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

latencies = []
lost_packets = 0
late_packets = 0 # Packets taking > 10ms (the loop interval)

print(f"Starting 100Hz Locomotion Test to {JETSON_IP}...")

start_time = time.time()
while time.time() - start_time < TEST_DURATION:
    loop_start = time.perf_counter()
    
    # send simulated motor command (128 bytes)
    msg = b'x' * 128 
    send_ts = time.perf_counter()
    sock.sendto(msg, (JETSON_IP, PORT))
    
    try:
        # wait for reflection
        data, addr = sock.recvfrom(1024)
        recv_ts = time.perf_counter()
        
        # calculate Round Trip Time (RTT)
        rtt_ms = (recv_ts - send_ts) * 1000
        latencies.append(rtt_ms)
        
        if rtt_ms > (1000 / FREQUENCY):
            late_packets += 1

    except socket.timeout:
        lost_packets += 1

    # precise sleep to maintain 100Hz
    elapsed = time.perf_counter() - loop_start
    sleep_time = max(0, (1/FREQUENCY) - elapsed)
    time.sleep(sleep_time)

# ------- Analysis -------
if latencies:
    avg_lat = np.mean(latencies)
    jitter = np.std(latencies)
    print("\n--- RESULTS ---")
    print(f"Average Latency: {avg_lat:.3f} ms")
    print(f"Jitter (StdDev): {jitter:.3f} ms") # CRITICAL: Should be < 0.1ms
    print(f"Packet Loss:     {lost_packets} packets")
    print(f"Late Packets:    {late_packets} (Arrived after the next loop started)")
else:
    print("Error: No data received. Check IP and Port settings.")

sock.close()