import random as rn
from armor import Armor
from weapon import Weapon

class Item:
    def __init__(self, name, item_type, effect, count=1):
        self.name = name
        self.item_type = item_type
        self.effect = effect
        self.count = count

    def use(self, target):
        if callable(self.effect):
            self.effect(target)
        else:
            print(f"Эффект {self.name} не может быть применен.")

    def __str__(self):
        return f"{self.name} (x{self.count})"

    def __repr__(self):
        return f"Item(name={self.name}, item_type={self.item_type}, count={self.count})"

class Potion(Item):
    def __init__(self, name, effect, effect_type, count=1):
        super().__init__(name, 'potion', None, count)
        self.effect = effect
        self.effect_type = effect_type

        # Карта действий для эффектов
        self.effect_actions = {
            "heal": self.apply_heal,
            "buff": self.apply_buff,
            "random": self.apply_random
        }

    def to_dict(self):
        """Преобразует объект в словарь для добавления в инвентарь."""
        return {
            "name": self.name,
            "effect": self.effect,
            "effect_type": self.effect_type,
            "count": self.count
        }

    def apply_heal(self, target):
        """Лечение цели."""
        target.hp = min(target.max_hp, target.hp + self.effect)
        print(f"{target.name} восстановил {self.effect} HP. Текущее здоровье: {target.hp}.")

    def apply_buff(self, target):
        """Увеличение урона цели."""
        target.damage += self.effect
        print(f"{target.name} увеличил урон на {self.effect}. Текущий урон: {target.damage}.")

    def apply_random(self, target):
        """Применение случайного эффекта."""
        action = rn.choice(["heal", "buff"])
        self.effect_actions[action](target)  

    def use(self, target):
        """Применяет эффект зелья к указанной цели."""
        if self.count <= 0:
            print(f"{self.name} больше нет в наличии.")
            return
        
        action = self.effect_actions.get(self.effect_type)
        if action:
            action(target)

        self.count -= 1
        if self.count == 0:
            print(f"{self.name} закончилось.")

class HealPotion(Potion):
    def __init__(self, name, effect, count=1):
        super().__init__(name, effect, "heal", count)

class BuffPotion(Potion):
    def __init__(self, name, effect, count=1):
        super().__init__(name, effect, "buff", count)

class RandomPotion(Potion):
    def __init__(self, name, effect, count=1):
        super().__init__(name, effect, "random", count)

class PotionFactory:
    potion_classes = [HealPotion, BuffPotion, RandomPotion]

    @staticmethod
    def create_potion(name=None, effect=None, count=1):
        potion_class = rn.choice(PotionFactory.potion_classes)
        if not name:
            name = f"Экспериментальное зелье #{rn.randint(1, 9999)}"
        if not effect:
            effect = rn.randint(10, 50)
        return potion_class(name=name, effect=effect, count=count)

class ItemFactory:
    item_classes = {
        'potion': lambda **kwargs: PotionFactory.create_potion(**kwargs),
        'weapon': lambda **kwargs: Weapon(**kwargs),
        'armor': lambda **kwargs: Armor(**kwargs)
    }

    @staticmethod
    def create_item(item_type, **kwargs):
        item_class = ItemFactory.item_classes.get(item_type)
        if not item_class:
            raise ValueError(f"Unknown item type: {item_type}")
        return item_class(**kwargs)


