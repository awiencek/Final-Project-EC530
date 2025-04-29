import pytest
from virtual_pet import VirtualPet

@pytest.fixture
def default_pet():
    return VirtualPet()

def test_pet_starts_with_default_stats(default_pet):
    assert default_pet.happiness == 50
    assert default_pet.level == 1
    assert default_pet.energy == 50

def test_feed_increases_hunger_and_happiness(default_pet):
    hunger_before = default_pet.hunger
    happiness_before = default_pet.happiness
    default_pet.feed()
    assert default_pet.hunger > hunger_before
    assert default_pet.happiness > happiness_before

def test_gain_experience_levels_up(monkeypatch):
    pet = VirtualPet()

    # Override print to suppress console output
    monkeypatch.setattr("builtins.print", lambda x: None)

    pet.gain_experience(100)
    assert pet.level == 2
    assert pet.experience == 0
