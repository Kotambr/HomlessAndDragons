from Item import ItemFactory
from Charecter import Player
import random as rn
Player1 = Player('ff', 19, 10, 100)

class Craft:
    def __init__(self, name: str, craftItem: list, typeCraft: str, finish_item):
        self.name = name
        self.craftItem = craftItem
        self.typeCraft = typeCraft
        self.finish_item = finish_item
        self.itemFact = ItemFactory()

    def move_in_craft(self, player):
        print(f"Выберите предмет для добавления: ")
        for i, item in enumerate(player.inventory.items, 1):
            print(f"({i}) {item.name} - {item.count}")

        choice = input("Предмет(0 для отмены): ")
        if choice == "0":
            return
        
        if choice.isdigit() and 1 <= int(choice) <= len(player.inventory.items):
            item = player.inventory.items[int(choice) - 1]
            self.isCraft(player)

        else:
            print("Неверный выбор.")

    def isCraft(self, player):
        for component in self.craftItem:
            item_name = component['name']
            item_count = component['count']
            found = False
            for item in player.inventory.items:
                if item.name == item_name and item.count >= item_count:
                    found = True
                    break
            if not found:
                print(f"Недостаточно {item_name} для крафта.")
                return False
        
        for component in self.craftItem:
            item_name = component['name']
            item_count = component['count']
            for item in player.inventory.items:
                if item.name == item_name:
                    item.count -= item_count
                    if item.count == 0:
                        player.inventory.items.remove(item)
                    break
        
        print(f"Предмет {self.name} успешно создан!")
        return True

    def craft(self, player):
        if self.isCraft(player):
            created_item = self.itemFact.create_item(self.typeCraft, name=self.name)
            player.inventory.add_item(created_item)

    
arrow = ItemFactory.create_item(item_type='misc', name='Стрела', effect=None, price=1, count=4)
wood = ItemFactory.create_item(item_type='misc', name='Дерево', effect=None, price=1, count=4)
Player1.inventory.add_item(arrow)
Player1.inventory.add_item(wood)
craftt = Craft('Лук', [{'name': 'Дерево', 'count': 2}, {'name': 'Стрела', 'count': 2}], 'weapon')
craftt.move_in_craft(Player1)
craftt.move_in_craft(Player1)
