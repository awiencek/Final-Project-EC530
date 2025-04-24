import sqlite3
import pytest
from pet_database import PetDatabase
from virtual_pet import VirtualPet

@pytest.fixture
def db():
    test_db = PetDatabase(db_name=":memory:")
    yield test_db
    test_db.close()

def test_save_and_load_pet_state(db):
    pet = VirtualPet()
    pet.happiness = 77
    pet.achievements = ["Fast Learner"]
    db.save_pet_state(pet)

    loaded = db.load_pet_state()
    assert loaded.happiness == 77
    assert "Fast Learner" in loaded.achievements
