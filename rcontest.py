import socket
import struct

# A quick and dirty rcon function
def send_rcon_command(ip, port, password, command, message):
    # Packet IDs
    auth_id = 1
    command_id = 2

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))

        # Authenticate
        auth_packet = struct.pack('<iii', 10 + len(password), auth_id, 3) + password.encode('utf-8') + b'\x00\x00'
        s.send(auth_packet)

        # Check auth response
        auth_response = s.recv(4096)
        _, response_id, _ = struct.unpack('<iii', auth_response[:12])

        if response_id == -1:
            raise ValueError("Authentication failed")

        # Construct our awesome workaround command with hex A0 for spaces in the message
        command_bytes = command.encode('utf-8') + b' '  # Initial command followed by a normal space
        message_bytes = message.replace(' ', '\xa0').encode('latin-1')  # Replace message spaces with hex A0 and encode
        final_command = command_bytes + message_bytes + b'\x00\x00'  # Final command with null termination

        # Send command
        command_packet_length = 10 + len(final_command) - 2  # Remove two null bytes
        command_packet = struct.pack('<iii', command_packet_length, command_id, 2) + final_command
        s.send(command_packet)

        # Receive command response
        response_packet = s.recv(4096)

        # Extract the response body (ignoring the packet length, id, and type)
        _, _, _, response_body = struct.unpack('<iii', response_packet[:12]) + (response_packet[12:],)

        return response_body.rstrip(b'\x00').decode('utf-8')

# Configuration
ip = '127.0.0.1'
port = 25575
password = 'password'
command = 'broadcast'
message = 'Hello world! This is rcon broadcast with spaces!'

# Execute and output result
try:
    result = send_rcon_command(ip, port, password, command, message)
    print("Command output:", result)
except Exception as e:
    print("Error:", e)
