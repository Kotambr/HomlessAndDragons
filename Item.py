import random as rn

class Item:
    def __init__(self):
        self.items = [
            {'type': 'Восполняющее здоровье', 'name': 'Зелье здоровья', 'effect': lambda: self.increase_hp(20), 'count': 1},
            {'type': 'Увеличение параметров', 'name': 'Зелье силы', 'effect': self.increase_damage, 'count': 1},
            {'type': 'Рандомизатор', 'name': 'Карта-обманка', 'effect': lambda: self.increase_hp(rn.randint(-50, 20)), 'count': 1},
            {'type': 'Вероятность', 'name': 'Карта подземки', 'effect': lambda: self.event.incrimer_event('chest'), 'count': 1},
            {'type': 'Вероятность', 'name': 'Странный мешок', 'effect': lambda: self.event.incrimer_event('enemy'), 'count': 1},
            {'type': 'Вероятность', 'name': 'Походная книга', 'effect': lambda: self.event.incrimer_event('item'), 'count': 1},
            {'type': 'Вероятность', 'name': 'Тухлое яйцо', 'effect': lambda: self.event.incrimer_event('nothing'), 'count': 1}
        ]
    
    @staticmethod
    def increase_hp(self, amount):
        self.hp += amount
        print(f"{self.name} восстановил {amount} здоровья. Текущее здоровье: {self.hp}")

    @staticmethod
    def increase_damage(self):
        self.player.damage += 20
        print(f"{self.name} увеличил силу атаки на 20. Текущая сила атаки: {self.damage}")

    def find_item(self, player):
        item = rn.choice(self.items)
        choice = input(f'Вы нашли {item["name"]}! Взять? (1)Да (2)Нет :')
        if choice == '1':
            player.inventory.add_item(item)
        else:
            print('Вы продолжили путь')
            return None
        

class InventoryItem:
    def __init__(self, item_dict):
        """
        Инициализация объекта InventoryItem.
        :param item_dict: Словарь с описанием предмета.
        """
        self.item = item_dict  # Словарь с информацией о предмете
        self.quantity = item_dict.get("count", 1)  # Количество предметов
        self.name = item_dict.get("name")  # Название предмета
        self.price = item_dict.get("price")  # Цена предмета

    def use(self):
        """
        Применяет эффект предмета.
        """
        print(f"Используется предмет: {self.item['name']}")
        if callable(self.item["effect"]):
            self.item["effect"]()  # Применяем эффект, если он задан

    def __str__(self):
        """
        Строковое представление предмета для отображения в инвентаре.
        """
        return f"{self.item['name']} (x{self.quantity})"
    
    def __repr__(self):
        return f"InventoryItem(name={self.item['name']}, quantity={self.quantity})"

class Inventory:
    def __init__(self):
        self.items = []  # Список предметов, каждый элемент — это InventoryItem

    def add_item(self, item_dict):
        """
        Добавляет предмет в инвентарь.
        :param item_dict: Словарь с описанием предмета.
        """

        # Проверяем, есть ли уже предмет с таким именем в инвентаре
        for inventory_item in self.items:
            if inventory_item.item["name"] == item_dict["name"]:
                inventory_item.quantity += item_dict.get("count", 1)
                print(f"Обновлено количество {inventory_item.item['name']} до {inventory_item.quantity}")
                return
        # Если предмет не найден, добавляем его как новый
        self.items.append(InventoryItem(item_dict))
        print(f"Добавлен новый предмет: {item_dict['name']}")

    def add_poition_enemy(self, item):
        """
        Добавляет предмет в инвентарь врага.
        :param item: Объект предмета (например, экземпляр Potion).
        """
        item_dict = item.to_dict() if hasattr(item, "to_dict") else item
        for inventory_item in self.items:
            if inventory_item.item["name"] == item_dict["name"]:
                inventory_item.quantity += item_dict.get("count", 1)
                print(f"Обновлено количество {inventory_item.item['name']} до {inventory_item.quantity}")
                return

        self.items.append(Potion(**item_dict))


    def remove_item(self, item_name, quantity=1):
        """Удаляет предмет из инвентаря или уменьшает его количество."""
        for inventory_item in self.items:
            if inventory_item.item["name"] == item_name:
                if inventory_item.quantity > quantity:
                    inventory_item.quantity -= quantity
                else:
                    self.items.remove(inventory_item) 
                return
        print("Такого предмета нет в инвентаре.")

    def use_item(self, item_name):
        """Использует предмет из инвентаря."""
        for inventory_item in self.items:
            if inventory_item.item["name"] == item_name:
                inventory_item.use()  # Применяем эффект предмета
                if inventory_item.quantity > 1:
                    inventory_item.quantity -= 1
                else:
                    self.items.remove(inventory_item)  # Удаляем предмет, если его количество равно нулю
                return
        print("Такого предмета нет в инвентаре.")

    def show_inventory(self):
        """Выводит содержимое инвентаря."""
        print("Инвентарь:")
        if not self.items:
            print("Инвентарь пуст.")
        else:
            for inventory_item in self.items:
                print(inventory_item)
            action = input('ВЫберите предмет: ')
            self.use_item(action)


class Potion:
    def __init__(self, name, effect, effect_type, count=1):
        """
        :param name: Название зелья.
        :param effect: Сила эффекта.
        :param effect_type: Тип эффекта (heal, buff, random).
        :param count: Количество использований.
        """
        self.name = name
        self.effect = effect
        self.effect_type = effect_type
        self.count = count

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
    @staticmethod
    def give_random_potion():
        potion_class = rn.choice([HealPotion, BuffPotion, RandomPotion]) 
        effect = rn.randint(10, 50) 
        name = f"Экспериментальное зелье #{rn.randint(1, 9999)}"
        return potion_class(name=name, effect=effect, count=1)


