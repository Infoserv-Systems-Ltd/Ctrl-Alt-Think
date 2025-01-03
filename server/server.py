import sqlite3
import socket
import threading
import subprocess
import sqlite3
from random import choice
from time import sleep
import json

# Create a socket server
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 12345  # Port to listen on


def execute_solution(solution_code, challenge_name):
    """Executes the submitted code and checks for correctness."""
    try:
        # Ideally, use a sandboxed environment for execution to avoid security risks
        # Here we're using subprocess to run the code in a separate process
        result = subprocess.run(
            ["python3", "-c", solution_code],
            capture_output=True,
            text=True,
            timeout=5,  # Set a timeout for the execution
        )
        output = result.stdout.strip()
        # Check against correct output (we'll simulate with a static challenge output)
        correct_output = get_correct_output(challenge_name)

        if output == correct_output:
            return True, output
        else:
            return False, output
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def get_correct_output(challenge_name):
    """Get the correct output for a challenge (this could be dynamically generated)."""
    # For simplicity, we're just using static outputs here
    challenge_outputs = {
        "challenge_1": "42",
        "challenge_2": "Hello, world!",
    }
    return challenge_outputs.get(challenge_name, "")


def handle_client(client_socket, client_address):
    """Handles communication with a connected client."""
    print(f"Client connected from {client_address}")

    # Simulating a game loop (you can replace this with real challenges)
    challenges = ["challenge_1", "challenge_2"]
    challenge_name = choice(challenges)
    client_socket.send(f"Your challenge: {challenge_name}".encode())

    # Wait for player solution
    solution_code = client_socket.recv(1024).decode()
    print(f"Received solution from {client_address}: {solution_code}")

    # Execute the solution
    is_correct, output = execute_solution(solution_code, challenge_name)

    # Update score in the database
    score = 1 if is_correct else 0
    player_name = "Player1"  # You would get this from the client
    insert_score(player_name, score, challenge_name, solution_code, output, "correct" if is_correct else "incorrect")

    # Send feedback to client
    client_socket.send(f"Your solution: {output}\nScore: {score}".encode())
    client_socket.close()


def start_server():
    """Start the server to accept client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


def connect_db():
    return sqlite3.connect("game_results.db")


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS player_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER DEFAULT 0,
            challenge_name TEXT NOT NULL,
            player_solution TEXT,
            correct_output TEXT,
            result TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def insert_score(player_name, score, challenge_name, player_solution, correct_output, result):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO player_scores (player_name, score, challenge_name, player_solution, correct_output, result)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (player_name, score, challenge_name, player_solution, correct_output, result),
    )
    conn.commit()
    conn.close()


def update_score(player_name, score):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE player_scores
        SET score = ?
        WHERE player_name = ?
    """,
        (score, player_name),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    start_server()
