# import requests module to make HTTP requests
import requests
# import tabulate module to create tables in the terminal
from tabulate import tabulate

# ANSI escape sequences for color formatting
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

# Make a GET request to the League of Legends API
response = requests.get("http://ddragon.leagueoflegends.com/cdn/13.10.1/data/en_US/champion.json")

# Extract the champion data from the API response and set it to a variable
champion_data = response.json()
champions = champion_data["data"]

# Extract the champion IDs
champion_ids = [champion["id"] for champion in champions.values()]

# Define the number of columns for the table to be created
num_columns = 10

# Chunk the champion IDs into groups based on the number of columns, this creates the rows for the table
champion_chunks = [champion_ids[i:i + num_columns] for i in range(0, len(champion_ids), num_columns)]

# Create a table using the champion chunks as rows
table = champion_chunks

# Print the table in the terminal with tabulate module and grid format
print(tabulate(table, tablefmt="grid"))

while True:
    # Prompt the user to enter the name of a champion based on the table
    user_input = input("Enter the name of a champion (q to quit): ")

    # Check if user wants to quit
    if user_input.lower() == "q":
        print("Thanks for playing!")
        break

    # Find the champion with the given name
    chosen_champion = None
    for champion in champions.values():
        if champion["id"] == user_input:
            chosen_champion = champion
            break

    # If the champion is found, retrieve and display the desired stats
    if chosen_champion:
        champion_id = chosen_champion["id"]
        champion_stats_url = f"http://ddragon.leagueoflegends.com/cdn/13.10.1/data/en_US/champion/{champion_id}.json"

        # Make a GET request to retrieve the selected champion's stats
        stats_response = requests.get(champion_stats_url)
        stats_data = stats_response.json()

        # Extract and display the desired stats (a little bit of destructuring was used, but probably not necessary at this point)
        info = stats_data["data"][champion_id]["info"]
        stats = stats_data["data"][champion_id]["stats"]

        # Extract and display the desired stats with color formatting
        print(f"\nStats for {GREEN}{chosen_champion['name']}{RESET}")
        print(f"Attack: {BLUE}{info['attack']}{RESET}")
        print(f"Defense: {BLUE}{info['defense']}{RESET}")
        print(f"Magic: {BLUE}{info['magic']}{RESET}")
        print(f"HP: {BLUE}{stats['hp']}{RESET}")
        print(f"MP: {BLUE}{stats['mp']}{RESET}")
        print(f"Armor: {BLUE}{stats['armor']}{RESET}")
    else:
        print(f"{RED}Champion not found.{RESET}")