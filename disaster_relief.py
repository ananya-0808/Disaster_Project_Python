import random
import time
import matplotlib.pyplot as plt

# Simulating disaster-affected areas and resources
areas = ['Area A', 'Area B', 'Area C', 'Area D']
needs = ['food', 'water', 'medical', 'shelter']

# Mock population and demand for resources
area_data = {
    area: {
        'population': random.randint(1000, 10000),  # Simulated population
        'food_need': random.randint(200, 1000),
        'water_need': random.randint(100, 500),
        'medical_need': random.randint(50, 200),
        'shelter_need': random.randint(100, 500)
    }
    for area in areas
}

# Mock resource availability
resources_available = {
    'food': 3000,
    'water': 2000,
    'medical': 500,
    'shelter': 1000
}


# Function to allocate resources to areas based on need and availability
def allocate_resources():
    global resources_available, area_data

    allocations = {}

    for area in area_data:
        # For each resource type, decide the allocation
        for resource in needs:
            required = area_data[area][f'{resource}_need']
            available = resources_available[resource]

            if available >= required:
                allocations[area] = {resource: required}
                resources_available[resource] -= required
            else:
                allocations[area] = {resource: available}
                resources_available[resource] -= available

    return allocations


# Blockchain Simulation
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Initial block that starts the chain
        self.chain.append({'block': 0, 'transactions': 'Genesis Block'})

    def add_block(self, transaction_details):
        block = {
            'block': len(self.chain),
            'transactions': transaction_details
        }
        self.chain.append(block)

    def view_chain(self):
        return self.chain


# Simulate adding transactions (resource allocation) to the blockchain
blockchain = Blockchain()


# Example of adding a transaction
def log_transaction(allocations):
    for area, allocation in allocations.items():
        blockchain.add_block(f"{area} received {allocation}")


# Function to plot the current resource needs
def plot_resources():
    areas = list(area_data.keys())
    food_needs = [area_data[area]['food_need'] for area in areas]
    water_needs = [area_data[area]['water_need'] for area in areas]
    medical_needs = [area_data[area]['medical_need'] for area in areas]
    shelter_needs = [area_data[area]['shelter_need'] for area in areas]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(areas, food_needs, label='Food Needs', color='#38d996', alpha=1)  # Red-orange
    ax.bar(areas, water_needs, label='Water Needs', color='#42aaf5', alpha=1)  # Blue
    ax.bar(areas, medical_needs, label='Medical Needs', color='#38d95b', alpha=1)  # Green
    ax.bar(areas, shelter_needs, label='Shelter Needs', color='#3b38d9', alpha=1)  # Orange

    ax.set_xlabel('Areas')
    ax.set_ylabel('Need Level')
    ax.set_title('Disaster Aid Needs by Area')
    ax.legend()

    plt.show()


# Real-time adjustment simulation
def real_time_monitoring():
    while True:
        # Simulate real-time adjustments
        allocations = allocate_resources()
        log_transaction(allocations)

        print(f"Allocations: {allocations}")
        print(f"Resources available: {resources_available}")

        # Plot updated resource needs
        plot_resources()

        # Simulate waiting for next real-time update (e.g., 5 seconds)
        time.sleep(5)


# Run the simulation
real_time_monitoring()
