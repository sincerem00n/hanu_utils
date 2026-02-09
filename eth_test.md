### 1. Check Bandwidth (The "Quantity" Test)

Use iperf3 to ensure the cable and switch can handle the heavy stream of RGB/Depth data you'll be sending alongside motor commands.

**On the External PC (Server):**
```Bash

iperf3 -s
```

**On the Jetson AGX Orin (Client):**
```Bash

iperf3 -c <PC_IP_ADDRESS> -t 30
```

- Success Criteria: For a 10GbE link, you should see ~9.4 Gbits/sec. For a 1GbE link, look for ~940 Mbits/sec.
- Why it matters: If this is low, your video stream will "choke" the motor commands.

### 2. Check Latency & Jitter (The "Timing" Test)

This is the most important test for your locomotion model. You need a consistent "heartbeat" between the PC and the Jetson.

Run a high-frequency ping from the PC to the Jetson:
```Bash

ping -i 0.01 -c 1000 <JETSON_IP_ADDRESS>
```

(The `-i 0.01` flag sends a ping every 10ms, simulating a 100Hz control loop.)

Look at the "rtt" summary at the bottom:

avg (Latency): Should be < 1.0ms.

mdev (Jitter): This is the "Mean Deviation." For stable locomotion, this must be < 0.1ms (100 microseconds).

If mdev is high, your motor commands are arriving at irregular intervals, which will make the humanoid's walk look "jittery" or vibrate.