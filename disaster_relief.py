import random
import time
import matplotlib.pyplot as plt

areas = ['Area A', 'Area B', 'Area C', 'Area D']
needs = ['food', 'water', 'medical', 'shelter']

area_data = {
    area: {
        'population': random.randint(1000, 10000), 
        'food_need': random.randint(200, 1000),
        'water_need': random.randint(100, 500),
        'medical_need': random.randint(50, 200),
        'shelter_need': random.randint(100, 500)
    }
    for area in areas
}

resources_available = {
    'food': 3000,
    'water': 2000,
    'medical': 500,
    'shelter': 1000
}

def allocate_resources():
    global resources_available, area_data

    allocations = {}

    for area in area_data:
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

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        self.chain.append({'block': 0, 'transactions': 'Genesis Block'})

    def add_block(self, transaction_details):
        block = {
            'block': len(self.chain),
            'transactions': transaction_details
        }
        self.chain.append(block)

    def view_chain(self):
        return self.chain

blockchain = Blockchain()

def log_transaction(allocations):
    for area, allocation in allocations.items():
        blockchain.add_block(f"{area} received {allocation}")

def plot_resources():
    areas = list(area_data.keys())
    food_needs = [area_data[area]['food_need'] for area in areas]
    water_needs = [area_data[area]['water_need'] for area in areas]
    medical_needs = [area_data[area]['medical_need'] for area in areas]
    shelter_needs = [area_data[area]['shelter_need'] for area in areas]

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(areas, food_needs, label='Food Needs', color='#38d996', alpha=1) 
    ax.bar(areas, water_needs, label='Water Needs', color='#42aaf5', alpha=1) 
    ax.bar(areas, medical_needs, label='Medical Needs', color='#38d95b', alpha=1) 
    ax.bar(areas, shelter_needs, label='Shelter Needs', color='#3b38d9', alpha=1) 

    ax.set_xlabel('Areas')
    ax.set_ylabel('Need Level')
    ax.set_title('Disaster Aid Needs by Area')
    ax.legend()

    plt.show()


def real_time_monitoring():
    while True:
        allocations = allocate_resources()
        log_transaction(allocations)

        print(f"Allocations: {allocations}")
        print(f"Resources available: {resources_available}")
        plot_resources()
        time.sleep(5)


# Run the simulation
real_time_monitoring()
