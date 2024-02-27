from apps.properties.models import Property

import random

# Generate test data for properties
test_data = [
    {
        'price': random.randint(100000, 1000000),  # Random price between $100,000 and $1,000,000
        'price_currency': 'USD',
        'area': random.randint(500, 5000),  # Random area between 500 and 5000 square feet
        'total_area': random.randint(500, 5000),  # Random total area between 500 and 5000 square feet
        'measured_area': random.randint(500, 5000),  # Random measured area between 500 and 5000 square feet
        'total_rooms': random.randint(2, 10),  # Random total rooms between 2 and 10
        'toilets': random.randint(1, 5),  # Random number of toilets between 1 and 5
        'construction_year': random.randint(1980, 2020),  # Random construction year between 1980 and 2020
        'renovation_year': random.randint(1980, 2020),  # Random renovation year between 1980 and 2020
        'total_floors': random.randint(1, 5),  # Random total floors between 1 and 5
        'heating': random.choice(['Gas', 'Electric', 'Oil', 'None']),  # Random heating type
        'outer_walls': random.choice(['Brick', 'Wood', 'Stone', 'Stucco']),  # Random outer walls type
        'roof_type': random.choice(['Flat', 'Pitched', 'Gable', 'Hip']),  # Random roof type
        'address': 'Address {}'.format(i)  # Sample address
    }
    for i in range(1, 21)  # Generate 20 records
]

# Create Property objects
for data in test_data:
    try:
        Property.objects.create(**data)
    except Exception as ex:
        pass

print("Test data created successfully!")
