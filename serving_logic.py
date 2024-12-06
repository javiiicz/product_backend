import os
import json
import random
from datetime import datetime

# Path to the population JSON file
POPULATION_PATH = 'population.json'
SESSIONS_DIR = 'sessions'

# Load the population from the JSON file
def load_population():
    try:
        with open(POPULATION_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Population file {POPULATION_PATH} not found.")
        return []

# Create a new session for a survey respondent
def create_new_session():
    population = load_population()
    
    if not population:
        print("Error: Population is empty or could not be loaded.")
        return None

    # Randomly sample 15 individuals from the population without replacement
    session_individuals = random.sample(population, 15)

    # Create a unique session ID
    session_id = generate_session_id()

    # Initialize session data
    session_data = {
        'session_id': session_id,
        'start_time': str(datetime.now()),
        'individuals': session_individuals,  # The 15 phones
        'scores': {},  # Dictionary to hold the scores for each phone
        'completed': False  # Indicates if the session is completed
    }

    # Save the session to a JSON file
    save_session_data(session_id, session_data)

    print(f"Session {session_id} created.")
    return session_id

def json_serve_new_session():
    population = load_population()
    
    if not population:
        print("Error: Population is empty or could not be loaded.")
        return None

    # Randomly sample 15 individuals from the population without replacement
    session_individuals = random.sample(population, 15)

    # Create a unique session ID
    session_id = generate_session_id()

    # Initialize session data
    session_data = {
        'session_id': session_id,
        'start_time': str(datetime.now()),
        'individuals': session_individuals,  # The 15 phones
        'scores': {},  # Dictionary to hold the scores for each phone
        'completed': False  # Indicates if the session is completed
    }

    return session_data

# Generate a unique session ID based on the current timestamp
def generate_session_id():
    return int(datetime.timestamp(datetime.now()))

# Save session data to a file
def save_session_data(session_id, session_data):
    session_path = os.path.join(SESSIONS_DIR, f"session_{session_id}.json")
    os.makedirs(SESSIONS_DIR, exist_ok=True)  # Ensure the directory exists
    with open(session_path, 'w') as session_file:
        json.dump(session_data, session_file, indent=4)

# Load session data from a file
def load_session_data(session_id):
    session_path = os.path.join(SESSIONS_DIR, f"session_{session_id}.json")
    try:
        with open(session_path, 'r') as session_file:
            return json.load(session_file)
    except FileNotFoundError:
        print(f"Error: Session {session_id} not found.")
        return None

# Serve the next individual (phone) to the respondent
def serve_next_individual(session_id):
    session_data = load_session_data(session_id)
    if session_data is None:
        return None

    # Check if the session is already completed
    if session_data['completed']:
        print(f"Session {session_id} is already completed.")
        return None

    # Serve the next phone that hasn't been rated yet
    for individual in session_data['individuals']:
        individual_id = str(session_data['individuals'].index(individual))
        if individual_id not in session_data['scores']:
            return individual

    # If all phones have been rated, mark the session as completed
    session_data['completed'] = True
    save_session_data(session_id, session_data)
    print(f"Session {session_id} completed.")
    return None

# Record a score for a phone in a session
def record_score(session_id, individual, score):
    session_data = load_session_data(session_id)
    if session_data is None:
        return

    # Record the score for the phone
    individual_id = str(session_data['individuals'].index(individual))
    session_data['scores'][individual_id] = score

    # Save the updated session data
    save_session_data(session_id, session_data)
    print(f"Score recorded for individual {individual_id} in session {session_id}.")

# Example usage
if __name__ == "__main__":
    # Create a new session for a survey respondent
    session_id = create_new_session()

    if session_id:
        # Serve individuals one by one
        for _ in range(15):
            individual = serve_next_individual(session_id)
            if individual:
                print(f"Serving individual: {individual}")
                # Simulate receiving a score from the respondent
                score = random.randint(1, 10)  # Random score for demonstration
                record_score(session_id, individual, score)
            else:
                break