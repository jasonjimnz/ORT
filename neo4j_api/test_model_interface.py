import random

from faker import Faker

fake = Faker()
class PersonGenerator:
    faker_instance = fake

    def __init__(self):
        print("Initialized")

    @classmethod
    def get_person(cls):
        return {
            "name": cls.faker_instance.name(),
            "last_name": cls.faker_instance.last_name()
        }

    @classmethod
    def get_city(cls):
        return {
            "city": cls.faker_instance.city(),
        }

    @classmethod
    def get_single_travel(cls):
        return {
            "city": cls.faker_instance.city(),
            "date": cls.faker_instance.date_time_this_decade().strftime('%Y-%m-%d')
        }

    @classmethod
    def get_preson_travels(cls):
        person_travels = {
            "person": cls.get_person(),
            "home": cls.get_city(),
            "travels": [cls.get_single_travel() for x in range(0,10)]
        }

        return person_travels

    @classmethod
    def get_activity(cls):
        activities = [
            "Goes to a museum",
            "Goes to a restaurant",
            "Goes to a church",
            "Goes to a football match",
            "Goes to a basketball match",
            "Goes to a meeting",
            "Explore new places",
            "Find new job",
            "Buy a property",
            "Rent a property",
            "Buy a car",
            "Visit someone",
            "Political event",
            "Hobby event",
            "Visit a doctor",
            "Other"
        ]

        return activities[random.randint(0, len(activities)-1)]

    @classmethod
    def get_purpose(cls):
        purposes = [
            "Business",
            "Holidays",
            "Personal",
            "Medical",
            "Honeymoon",
            "Event",
            "Other"
        ]

        return purposes[random.randint(0, len(purposes)-1)]