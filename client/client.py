import socket

SERVER_IP = '192.168.x.x'  # Replace with Raspberry Pi IP address
PORT = 12345

def send_solution_to_server(solution_code):
    """Send the player's solution to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))
    
    # Receive the challenge
    challenge = client_socket.recv(1024).decode()
    print(f"Challenge: {challenge}")
    
    # Send the solution
    client_socket.send(solution_code.encode())
    
    # Receive the result and score
    result = client_socket.recv(1024).decode()
    print(f"Result: {result}")
    
    client_socket.close()

# Example usage: sending a solution
player_solution = "print(21 + 21)"  # The player's solution (you can change this dynamically)
send_solution_to_server(player_solution)
