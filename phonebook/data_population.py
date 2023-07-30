import random
import string
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phonebook.settings")

import django

django.setup()

from django.contrib.auth.models import User
from faker import Faker
from api.models import Contact, Profile

fake = Faker()


def generate_phone_number():
    return ''.join(random.choices(string.digits, k=10))


def create_random_user():
    username = fake.user_name()
    while User.objects.filter(username=username).exists():
        username = fake.user_name()

    password = fake.password()
    email = fake.email()

    user = User.objects.create_user(username=username, password=password, email=email)

    number = generate_phone_number()
    profile = Profile.objects.create(user=user, phone_number=number)

    num_contacts = random.randint(0, 10)
    for _ in range(num_contacts):
        name = fake.name()
        number = generate_phone_number()
        spam = random.choice([True, False])
        Contact.objects.create(name=name, phone_number=number, spam=spam, user=user)

    print(f"Created user: {username}, Password: {password}")

def populate_database():
    num_users = 100
    for _ in range(num_users):
        create_random_user()

populate_database()
