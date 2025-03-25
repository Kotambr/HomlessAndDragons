from Item import ItemFactory
import random as rn

class Craft:
    def __init__(self):
        self.itemFact = ItemFactory()
        self.craftList = []

    def add_recipe(self, name: str, craftItem: list, typeCraft: str, **kwargs):
        ''' Добавление рецепта крафта '''
        self.craftList.append({
            'name': name,
            'craftItem': craftItem,
            'typeCraft': typeCraft,
            'kwargs': kwargs
        })

    def display_recipes(self):
        print("Доступные рецепты крафта:")
        for i, recipe in enumerate(self.craftList, 1):
            print(f"{i}. {recipe['name']} - Требуемые предметы: {', '.join([f'{item['name']} x{item['count']}' for item in recipe['craftItem']])}")

    def move_in_craft(self, player):
        ''' Переход в меню крафта '''
        self.display_recipes()
        choice = input("Выберите рецепт для крафта (0 для отмены): ")
        if choice == "0":
            return
        
        if choice.isdigit() and 1 <= int(choice) <= len(self.craftList):
            recipe = self.craftList[int(choice) - 1]
            if self.isCraft(player, recipe['craftItem']):
                self.craft(player, recipe)
                print(f"Предмет {recipe['name']} успешно создан!")
            else:
                print("Недостаточно ресурсов для крафта.")
        else:
            print("Неверный выбор.")

    def isCraft(self, player, craftItem):
        ''' Проверка наличия ресурсов для крафта '''
        for component in craftItem:
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
        
        for component in craftItem:
            item_name = component['name']
            item_count = component['count']
            for item in player.inventory.items:
                if item.name == item_name:
                    item.count -= item_count
                    if item.count == 0:
                        player.inventory.items.remove(item)
                    break
        return True

    def craft(self, player, recipe):
        created_item = self.itemFact.create_item(recipe['typeCraft'], name=recipe['name'], **recipe['kwargs'])
        player.inventory.add_item(created_item)
