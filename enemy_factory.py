from Charecter import Enemy
import random
from spell import SpellFactory

class EnemyFactory:
    def create_enemy(self, name, hp, damage, manabank, spells=None):
        return Enemy(name, hp, damage, manabank, spells)

class EnemyClass:
    def __init__(self, name):
        self.name = name
        self.hp = 0
        self.damage = 0
        self.manabank = 0
        self.spells = []

    def distribute_attributes(self):
        raise NotImplementedError("Этот метод должен быть переопределен в подклассе")

    def assign_spells(self):
        spell_factory = SpellFactory()
        self.spells = [spell_factory.create_random_spell() for _ in range(random.randint(1, 3))]

class Mage(EnemyClass):
    def distribute_attributes(self):
        self.hp = random.randint(50, 100)
        self.damage = random.randint(20, 40)
        self.manabank = random.randint(100, 200)
        self.assign_spells()

class Warrior(EnemyClass):
    def distribute_attributes(self):
        self.hp = random.randint(100, 200)
        self.damage = random.randint(30, 50)
        self.manabank = random.randint(20, 50)
        self.assign_spells()

class Thief(EnemyClass):
    def distribute_attributes(self):
        self.hp = random.randint(70, 120)
        self.damage = random.randint(25, 45)
        self.manabank = random.randint(30, 60)
        self.assign_spells()

class Jester(EnemyClass):
    def distribute_attributes(self):
        self.hp = random.randint(60, 110)
        self.damage = random.randint(15, 35)
        self.manabank = random.randint(50, 100)
        self.assign_spells()

class Animal(EnemyClass):
    def distribute_attributes(self):
        self.hp = random.randint(30, 80)
        self.damage = random.randint(10, 30)
        self.manabank = 0  # Животные не используют ману

class Mimic(EnemyClass):
    def distribute_attributes(self):
        self.hp = random.randint(80, 150)
        self.damage = random.randint(30, 60)
        self.manabank = random.randint(20, 50)
        self.assign_spells()

class EnemyNameGenerator:
    @staticmethod
    def generate_name(enemy_class):
        names = {
            'Mage': ['Магистр Шарлатан', 'Колдун Пузырь', 'Волшебник Пых'],
            'Warrior': ['Воин Топор', 'Боец Кулак', 'Рыцарь Лом'],
            'Thief': ['Воришка Крадун', 'Разбойник Тень', 'Грабитель Шмыг'],
            'Jester': ['Шут Балабол', 'Клоун Хохотун', 'Юморист Прыг'],
            'Animal': ['Зверь Коготь', 'Зверь Клык', 'Зверь Рык'],
            'Mimic': ['Мимик Сундук', 'Мимик Рюкзак', 'Мимик Бочка']
        }
        return random.choice(names[enemy_class])
