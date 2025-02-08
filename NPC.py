from Item import Item, Inventory
import random as rn
from event import Event

class NPC:
    def __init__(self, name, description, actions=None):
        """
        :param name: Имя NPC.
        :param description: Краткое описание NPC.
        :param actions: Список доступных действий для взаимодействия.
        """
        self.name = name
        self.description = description
        self.actions = actions if actions else []

    def interact(self, player):
        """
        Интерфейс взаимодействия с NPC.
        """
        print(f"Вы встречаете {self.name}: {self.description}")
        while True:
            print("Доступные действия:")
            for i, action in enumerate(self.actions, 1):
                print(f"({i}) {action['name']}")
            print("(0) Уйти")

            choice = input("Ваш выбор: ")
            if choice == "0":
                print(f"Вы покидаете {self.name}.")
                break

            if choice.isdigit() and 1 <= int(choice) <= len(self.actions):
                action = self.actions[int(choice) - 1]
                action["func"](player)
            else:
                print("Неверный выбор. Попробуйте снова.")
        
class Merchant(NPC):
    def __init__(self, name, inventory, quests=None):
        """
        :param name: Имя торговца.
        :param inventory: Инвентарь торговца (список предметов).
        :param quests: Список квестов, доступных у торговца.
        """
        super().__init__(name, description="Местный торговец", actions=[
            {"name": "Купить предмет", "func": self.show_items_for_sale},
            {"name": "Продать предмет", "func": self.buy_from_player},
            {"name": "Взять квест", "func": self.give_quest},
        ])
        self.inventory = Inventory()
        self.quests = quests if quests else []
        self.populate_inventory()

    def populate_inventory(self):
        """Добавляет предметы в инвентарь торговца."""
        items_for_sale = [
            {'type': 'Восполняющее здоровье', 'name': 'Зелье здоровья', 'effect': lambda: self.increase_hp(20), 'count': 1, 'price': 100},
            {'type': 'Увеличение параметров', 'name': 'Зелье силы', 'effect': Item.increase_damage, 'count': 1, 'price': 100},
            {'type': 'Рандомизатор', 'name': 'Карта-обманка', 'effect': lambda: Item.increase_hp(rn.randint(-50, 20)), 'count': 1, 'price': 100},
            {'type': 'Вероятность', 'name': 'Карта подземки', 'effect': lambda: Event.incrimer_event('chest'), 'count': 1, 'price': 100},
            {'type': 'Вероятность', 'name': 'Странный мешок', 'effect': lambda: Event.incrimer_event('enemy'), 'count': 1, 'price': 100},
            {'type': 'Вероятность', 'name': 'Походная книга', 'effect': lambda: Event.incrimer_event('item'), 'count': 1, 'price': 100},
            {'type': 'Вероятность', 'name': 'Тухлое яйцо', 'effect': lambda: Event.incrimer_event('nothing'), 'count': 1, 'price': 100},
        ]
        for item in items_for_sale:
            self.inventory.add_item(item)

    def show_items_for_sale(self, player):
        """Показывает товары, доступные для покупки."""
        if not self.inventory.items:
            print(f"{self.name}: У меня пока нет товаров на продажу.")
            return

        print(f"{self.name}: Вот, что у меня есть на продажу:")
        for i, item in enumerate(self.inventory.items, 1):
            print(f"({i}) {item[('name')]} - {item[('price')]} монет")

        choice = input("Что хотите купить? (0 для отмены): ")
        if choice == "0":
            return

        if choice.isdigit() and 1 <= int(choice) <= len(self.inventory.items):
            item = self.inventory.items[int(choice) - 1]
            if player.gold >= item.price:
                player.gold -= item.price
                player.inventory.add_item({"name": item.name, "price": item.price, "count": 1})
                print(f"Вы купили {item.name} за {item.price} монет.")
            else:
                print("У вас недостаточно монет.")
        else:
            print("Неверный выбор.")

    def buy_from_player(self, player):
        """Позволяет игроку продать предметы."""
        print("Ваш инвентарь:")
        for i, item in enumerate(player.inventory.items, 1):
            print(f"({i}) {item.item['name']} - Цена: {item.item.get('sell_price', 10)} монет")
        choice = input("Что хотите продать? (0 для отмены): ")
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(player.inventory.items):
            item = player.inventory.items[int(choice) - 1]
            sell_price = item.item.get("sell_price", 10)
            player.gold += sell_price
            player.inventory.remove_item(item.item["name"])
            print(f"Вы продали {item.item['name']} за {sell_price} монет.")
        else:
            print("Неверный выбор.")

    def give_quest(self, player):
        """Выдаёт квест игроку."""
        if not self.quests:
            print(f"{self.name}: У меня для вас нет заданий.")
            return
        quest = self.quests.pop(0)
        player.quests.append(quest)
        print(f"{self.name}: Возьмите это задание: {quest.name}. {quest.description}")

class Quest:
    def __init__(self, name, description, reward, condition):
        """
        :param name: Название квеста.
        :param description: Описание квеста.
        :param reward: Награда за выполнение.
        :param condition: Условие выполнения (функция).
        """
        self.name = name
        self.description = description
        self.reward = reward
        self.condition = condition
        self.completed = False

    def check_completion(self, player):
        """Проверяет выполнение квеста."""
        if self.condition(player):
            self.completed = True
            print(f"Квест '{self.name}' выполнен!")
            player.gold += self.reward
            print(f"Вы получили {self.reward} монет в награду.")
