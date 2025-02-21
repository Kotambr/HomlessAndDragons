import random as rn
from armor import Armor
from weapon import Weapon

class Item:
    def __init__(self, name, item_type, effect, price, count=1):
        self.name = name
        self.item_type = item_type
        self.effect = effect
        self.price = price
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
    def __init__(self, name, effect, effect_type, price, count=1):
        super().__init__(name, 'potion', effect, price, count)
        self.effect_type = effect_type

        # Карта действий для эффектов
        self.effect_actions = {
            "heal": self.apply_heal,
            "buff":  self.apply_buff,
            "random": self.apply_random
        }

    def apply_heal(self, target):
        """Лечение цели."""
        target.hp += self.effect
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
    def __init__(self, name, effect, count=1, price=None):
        super().__init__(name, effect, "heal", price, count)

class BuffPotion(Potion):
    def __init__(self, name, effect, count=1, price=None):
        super().__init__(name, effect, "buff", price, count)

class RandomPotion(Potion):
    def __init__(self, name, effect, count=1, price=None):
        super().__init__(name, effect, "random", price, count)

class PotionFactory:
    potion_classes = {'heal': HealPotion, 'buff': BuffPotion, 'random': RandomPotion}

    @staticmethod
    def create_potion(name, effect, price, count=1):
        potion_class = PotionFactory.potion_classes[effect[0]]
        if not name:
            name = f"Экспериментальное зелье #{rn.randint(1, 9999)}"
        return potion_class(name=name, effect=effect[1], count=count, price=price)

class ItemFactory:
    item_classes = {
        'potion': lambda **kwargs: PotionFactory.create_potion(**kwargs),
        'weapon': lambda **kwargs: Weapon(**kwargs),
        'armor': lambda **kwargs: Armor(**kwargs),
        'misc': lambda **kwargs: Item(**kwargs)
    }

    @staticmethod
    def create_item(item_type, **kwargs):
        item_class = ItemFactory.item_classes.get(item_type)
        if not item_class:
            raise ValueError(f"Unknown item type: {item_type}")
        return item_class(**kwargs)

class Inventory:
    def __init__(self):
        self.items = []  # Список предметов, каждый элемент — это экземпляр Item, Armor или Weapon

    def add_item(self, item):
        """Добавляет предмет в инвентарь."""
        for inventory_item in self.items:
            if inventory_item.name == item.name and isinstance(inventory_item, type(item)):
                inventory_item.count += item.count
                print(f"Обновлено количество {inventory_item.name} до {inventory_item.count}")
                return
        self.items.append(item)
        print(f"Добавлен новый предмет: {item.name}")

    def remove_item(self, item_name, quantity=1):
        """Удаляет предмет из инвентаря или уменьшает его количество."""
        for inventory_item in self.items:
            if inventory_item.name == item_name:
                if inventory_item.count > quantity:
                    inventory_item.count -= quantity
                else:
                    self.items.remove(inventory_item)
                return
        print("Такого предмета нет в инвентаре.")
    
    def remove_equipment(self, item_name):
        '''Удаляет оружие и броню из инвентаря'''
        for inventory_item in self.items:
            if inventory_item.name == item_name:
                self.items.remove(inventory_item)
            return
        print("Такого предмета нет в инвентаре.")

    def use_item(self, item_name, target):
        """Использует предмет из инвентаря на указанной цели."""
        for inventory_item in self.items:
            if inventory_item.name == item_name:
                inventory_item.use(target)
                if inventory_item.count > 1:
                    inventory_item.count -= 1
                else:
                    self.items.remove(inventory_item)
                return
        print("Такого предмета нет в инвентаре.")

    def show_inventory(self, player):
        """Выводит содержимое инвентаря и позволяет использовать предметы на игроке."""
        inventory = []
        print("Инвентарь:")
        if not self.items:
            print("Инвентарь пуст.")
        else:
            for i, item in enumerate(self.items, 1):
                if item:
                    print(f"({i}) {item.name}")
                    inventory.append(item)
            action = input('Выберите предмет: ')
            if action == "0":
                return
            if action.isdigit() and 1 <= int(action) <= len(inventory):
                item = inventory[int(action) - 1]
                self.use_item(item.name, player)

class MiscItem(Item):
    def __init__(self, name, effect, price, count=1):
        super().__init__(name, 'misc', effect, price, count)

    def to_dict(self):
        """Преобразует объект в словарь для добавления в инвентарь."""
        return {
            "name": self.name,
            "effect": self.effect,
            "effect_type": self.effect_type,
            "count": self.count
        }
    
    def use(self, target):
        """Применяет эффект к указанной цели."""
        if self.count <= 0:
            print(f"{self.name} больше нет в наличии.")
            return
        
        if callable(self.effect):
            self.effect(target)

        self.count -= 1
        if self.count == 0:
            print(f"{self.name} закончилось.")

    def repair_effect(self, item, durability):
        item.durability += durability
        print(f'Прочность на {item.name} восстановлена на {durability}')
    
    def description(self, description):
        print(description)



