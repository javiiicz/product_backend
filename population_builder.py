import random
import json
from config import ATTRIBUTES

# Define the possible levels for each attribute
# ATTRIBUTES = {
#     "Screen Size": ["5.4\"", "6.2\"", "6.5\""],
#     "Color:": ["Silver", "Black", "Red"],
#     "Price": ["$500", "$700", "$1000"],
#     "Build Material": ["Plastic", "Aluminum", "Titanium"],
#     "AI Integration": ["Yes", "No"],
#     # "Processor": ["Snapdragon 888", "Exynos 2100", "Apple A14", "MediaTek Dimensity 1000"],
#     # "RAM": ["4GB", "6GB", "8GB", "12GB"],
#     # "Storage": ["64GB", "128GB", "256GB", "512GB"],
#     # "Camera Quality": ["12MP", "48MP", "64MP", "108MP"],
#     # "Camera Characteristics": ["Night Mode", "Burst Mode", "Optical Zoom", "Smart HDR 4", "Portrait Mode", "Panorama", "Time-lapse"],
#     # "Number of Cameras": ["One", "Two", "Three"],
#     # "Screen Quality": ["OLED", "Ultra HD", "Retina Display", "LCD"],
#     # "Battery Life": ["3000mAh", "4000mAh", "5000mAh", "6000mAh"],
#     # "Operating System": ["Android", "iOS"],
#     # "Color:": ["Silver", "Black", "White", "Yellow", "Red", "Blue", "Green"],
#     # "Price": ["$500", "$700", "$1000", "$1200"],
#     # "Physical Attributes": ["Home button", "Volume Buttons", "Audio Jack", "Physical Keyboard", "Foldable"],
#     # "Charger Port": ["Lightning", "USB-A", "USB-C", "Micro-USB"],
#     # "5G Support": ["Yes", "No"]
# }

# Step 1: Function to generate a random phone profile
def generate_random_phone(attributes):
    phone = {}
    for attribute in attributes:
        phone[attribute] = random.choice(attributes[attribute])  # Randomly pick a level for each attribute
    return phone

# Step 2: Generate the initial population by sampling randomly from all possible combinations
def generate_initial_population(population_size, attributes):
    population = []
    for _ in range(population_size):
        phone = generate_random_phone(attributes)  # Create a random phone
        population.append(phone)
    return population

# Step 3: Save the generated population to a JSON file
def save_population_to_file(population, filename='population.json'):
    with open(filename, 'w') as file:
        json.dump(population, file, indent=4)
    print(f"Population saved to {filename}")

# Example: Generate an initial population of 100 phones and save to a JSON file
if __name__ == "__main__":
    initial_population = generate_initial_population(100, ATTRIBUTES)
    save_population_to_file(initial_population)

    # Output the first few individuals in the population
    print(initial_population[0], initial_population[1])
