## Network Packet Sniffer

### Overview

A packet sniffer captures network traffic and helps in analyzing the data transmitted across the network. This project is implemented in Python using `socket` and can capture and display raw packets.

### Requirements

- Python 3.x
- Root or Administrator privileges
- `socket` module (included in Python)

### How It Works

This packet sniffer captures raw packets (including headers) from the network interface and decodes them to display useful information like source IP, destination IP, protocol, and more.

### Steps to Build

#### 1. Set Up Raw Socket

Python's `socket` module is used to create a raw socket that listens to all incoming packets on the specified network interface.

```python
import socket

def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        s.bind(('YOUR_INTERFACE_IP', 0))
        s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        return s
    except socket.error as err:
        print(f"Socket creation failed: {err}")
        exit()
```

#### 2. Packet Sniffing Logic

The raw socket captures the data, and the received data is processed to extract useful information such as IP addresses and protocols.

```python
def sniff_packets(s):
    while True:
        packet = s.recvfrom(65565)[0]

        # Parse IP header
        ip_header = packet[0:20]
        ip_info = parse_ip_header(ip_header)
        print(f"Source IP: {ip_info['src_ip']}, Destination IP: {ip_info['dst_ip']}, Protocol: {ip_info['protocol']}")
```

#### 3. Parsing the IP Header

The IP header contains crucial information like the source and destination IP addresses, protocol, etc. A function is created to parse this header.

```python
import struct

def parse_ip_header(packet):
    iph = struct.unpack('!BBHHHBBH4s4s', packet)
    
    src_ip = socket.inet_ntoa(iph[8])
    dst_ip = socket.inet_ntoa(iph[9])
    protocol = iph[6]

    return {
        'src_ip': src_ip,
        'dst_ip': dst_ip,
        'protocol': protocol
    }
```

#### 4. Stop Sniffing

Use a signal handler or manual input to stop packet sniffing.

```python
def stop_sniffing(s):
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
```

### Usage

1. Replace `'YOUR_INTERFACE_IP'` with your machine's IP address in the `create_socket` function.
2. Run the script with elevated privileges:

   ```bash
   sudo python packet_sniffer.py
   ```

3. The terminal will display the captured packet information in real-time.