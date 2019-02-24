from apps.parkSpot.models import parkingSpot

DUMMY_SPOT_DATA = [
    {
        'lat': 1,
        'longi': 35,
        'spot_addr': 'Park Street Avenue, San Jose',
        'cost_per_hr': 100,
    },
    {
        'lat': 3,
        'longi': 35,
        'spot_addr': 'Park Street Avenue, San Jose',
        'cost_per_hr': 10,
    },
    {
        'lat': 8,
        'longi': 25,
        'spot_addr': 'Park Street Avenue, San Jose',
        'cost_per_hr': 16,
    },
    {
        'lat': 4,
        'longi': 35,
        'spot_addr': 'Park Street Avenue, San Jose',
        'cost_per_hr': 23,
    },
    {
        'lat': 9,
        'longi': 25,
        'spot_addr': 'Park Street Avenue, San Jose',
        'cost_per_hr': 15,
    }
]

def insert_street_spots_data():
    """
    Inserts dummy data of street spots for reservation usage of users
    """
    if parkingSpot.objects.count() == 0:
        for spot_data in DUMMY_SPOT_DATA:
            parkingSpot.objects.create(**spot_data)
        print("Spots data insertion completed")