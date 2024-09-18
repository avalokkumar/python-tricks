import socket  # Import the socket module for network communication
import struct  # Import struct to unpack the packet data

# Function to create a raw socket
def create_socket():
    # Create a raw socket to capture all incoming packets at the network interface
    # AF_INET -> IPv4, SOCK_RAW -> raw packet, IPPROTO_IP -> protocol for IP packets
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

    # Bind the socket to a network interface (replace with your interface IP)
    s.bind(('YOUR_INTERFACE_IP', 0))

    # Set options for the socket: IP_HDRINCL allows custom IP headers to be included
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Enable promiscuous mode to capture all packets (Windows specific: SIO_RCVALL)
    s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    return s

# Function to parse the IP header from the packet
def parse_ip_header(packet):
    # Unpack the first 20 bytes (IP header) of the packet
    # '!BBHHHBBH4s4s' -> struct format string to extract fields from binary data
    iph = struct.unpack('!BBHHHBBH4s4s', packet[:20])

    # Extract source and destination IP addresses from the header
    src_ip = socket.inet_ntoa(iph[8])  # Convert 32-bit binary IP to dotted string format
    dst_ip = socket.inet_ntoa(iph[9])
    return src_ip, dst_ip

# Function to sniff packets continuously
def sniff_packets(socket):
    try:
        # Infinite loop to continuously sniff packets
        while True:
            # Receive packets from the socket (buffer size 65565 bytes)
            packet, _ = socket.recvfrom(65565)

            # Parse the IP header to extract source and destination IPs
            src_ip, dst_ip = parse_ip_header(packet)

            # Print the IP addresses of the packet
            print(f"Source IP: {src_ip} -> Destination IP: {dst_ip}")
    except KeyboardInterrupt:
        # Stop sniffing if interrupted (Ctrl+C), disable promiscuous mode
        socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

# Main function to execute the sniffer
if __name__ == "__main__":
    # Create a socket and start sniffing packets
    s = create_socket()
    sniff_packets(s)