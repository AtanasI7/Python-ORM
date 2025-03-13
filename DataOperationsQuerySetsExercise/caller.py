import os
from decimal import Decimal
import django
from django.db.models import F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character
from main_app.choices import RoomTypeChoice, CharacterClassTypeChoice


def create_pet(name: str, species: str) -> str:
    pet = Pet.objects.create(
        name=name,
        species=species
    )

    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"

def rename_artifact(artifact: Artifact, new_name: str) -> None:
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()

def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')

    return '\n'.join(f"{l.name} has a population of {l.population}!" for l in locations)

def new_capital():
    # Location.objects.first().update(is_capital=True)

    first = Location.objects.first()
    first.is_capital = True
    first.save()

def get_capitals():
    return Location.objects.filter(is_capital=True).values('name')

def delete_first_location():
    Location.objects.first().delete()



def apply_discount() -> None:
    cars = Car.objects.all()

    updated_prices = []

    for car in cars:
        percentage = Decimal(str(sum(int(digit) for digit in str(car.year)) / 100))
        discount = car.price * percentage
        car.price_with_discount = car.price - discount
        updated_prices.append(car)

    cars.bulk_update(updated_prices, ['price_with_discount',])

def get_recent_cars():
    return Car.objects.all().filter(year__gt=2020).values('model', 'price_with_discount')

def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(f"Task - {task.title} needs to be done until {task.due_date}!" for task in unfinished_tasks)


def complete_odd_tasks():
    tasks = Task.objects.all()

    odd_completed_tasks = []

    for t in tasks:
        if t.id % 2 == 1:
            t.is_finished = True
            odd_completed_tasks.append(t)

    Task.objects.bulk_update(odd_completed_tasks, ['is_finished'])

def encode_and_replace(text: str, task_title: str) -> None:
    encoded_text = ''.join(chr(ord(c) - 3) for c in text)

    updated_task = []

    for task in Task.objects.filter(title=task_title):
        task.description = encoded_text
        updated_task.append(task)

    Task.objects.bulk_update(updated_task, ['description'])

    # Task.objects.filter(title=task_title).update(description=encoded_text)


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type=RoomTypeChoice.DELUXE)

    result = []

    for room in deluxe_rooms:
        if room.id % 2 == 0:
            result.append(f"Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!")


    return '\n'.join(result)

def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    previous_room: HotelRoom= None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room:
            room.capacity += previous_room.capacity
        else:
            room.capacity += room.id

        previous_room = room
        room.save()

def reserve_first_room():
    room = HotelRoom.objects.first()
    room.is_reserved = True
    room.save()

def delete_last_room():
    room = HotelRoom.objects.last()

    if not room.is_reserved:
        room.delete()


def update_characters():
    Character.objects.filter(class_name=CharacterClassTypeChoice.MAGE).update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7
    )

    Character.objects.filter(class_name=CharacterClassTypeChoice.WARRIOR).update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4
    )

    Character.objects.filter(class_name__in=[CharacterClassTypeChoice.SCOUT, CharacterClassTypeChoice.ASSASSIN]).update(
        inventory='The inventory is empty'
    )

def fuse_characters(first_character: Character, second_character: Character) -> None:
    fusion_inventory = None

    if first_character.class_name in [CharacterClassTypeChoice.MAGE, CharacterClassTypeChoice.SCOUT]:
        fusion_inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    elif first_character.class_name in [CharacterClassTypeChoice.WARRIOR, CharacterClassTypeChoice.ASSASSIN]:
        fusion_inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name=CharacterClassTypeChoice.FUSION,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=fusion_inventory
    )

    first_character.delete()
    second_character.delete()

def grand_dexterity():
    Character.objects.update(
        dexterity=30
    )

def grand_intelligence():
    Character.objects.update(
        intelligence=40
    )

def grand_strength():
    Character.objects.update(
        strength=50
    )

def delete_characters():
    empty_characters = Character.objects.filter(inventory='The inventory is empty').delete()







