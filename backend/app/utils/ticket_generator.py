from datetime import datetime
import random

def generate_ticket_number():

    timestamp = datetime.now().strftime("%Y%m%d")

    random_part = random.randint(
        1000,
        9999
    )

    return f"TDE-{timestamp}-{random_part}"