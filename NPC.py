from Item import Item, Inventory
import random as rn
from event import Event
from armor import Chestplate, Helmet, Leggings, Boots, ArmorFactory
from weapon import Sword, Dagger, MagicalStuff, Projectile, WeaponFactory

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

class Citizen(NPC):
    def __init__(self, name, description, actions=None):
        super().__init__(name, description, actions)
        self.questions = [
            {'ask': 'Как погода?', 'answer': 'Погода как погода. Что за глупый вопрос!?'},
            {'ask': 'Что нового в городе?', 'answer': 'Ничего особенного, всё как обычно.'},
            {'ask': 'Где можно найти торговца?', 'answer': 'Торговец обычно находится на центральной площади.'}
        ]
        self.phrases = [
            "Прекрасная погода сегодня, не правда ли?",
            "Вы слышали последние новости?",
            "Будьте осторожны, в городе полно разбойников."
        ]
        self.quests = [
            Quest(name="Помощь горожанину", description="Помогите горожанину с его проблемой.", reward=20, condition=lambda p: True)
        ]
        self.actions = [
            {"name": "Задать вопрос", "func": self.ask_of_citizen},
            {"name": "Поговорить", "func": self.talk_to_citizen},
            {"name": "Взять квест", "func": self.give_quest}
        ]

    def ask_of_citizen(self, player):
        print("Выберите вопрос:")
        for i, question in enumerate(self.questions, 1):
            print(f"({i}) {question['ask']}")
        choice = input("Ваш выбор: ")
        if choice.isdigit() and 1 <= int(choice) <= len(self.questions):
            question = self.questions[int(choice) - 1]
            print(f"Вопрос: {question['ask']}")
            print(f"Ответ: {question['answer']}")
        else:
            print("Неверный выбор. Попробуйте снова.")

    def talk_to_citizen(self, player):
        print("Выберите фразу:")
        for i, phrase in enumerate(self.phrases, 1):
            print(f"({i}) {phrase}")
        choice = input("Ваш выбор: ")
        if choice.isdigit() and 1 <= int(choice) <= len(self.phrases):
            phrase = self.phrases[int(choice) - 1]
            print(f"{self.name} говорит: {phrase}")
        else:
            print("Неверный выбор. Попробуйте снова.")

    def give_quest(self, player):
        if not self.quests:
            print(f"{self.name}: У меня для вас нет заданий.")
            return
        quest = self.quests.pop(0)
        player.quests.append(quest)
        print(f"{self.name}: Возьмите это задание: {quest.name}. {quest.description}")

class Blacksmith(NPC):
    def __init__(self, name, description, actions=None):
        """
        :param name: Имя кузнеца.
        :param description: Описание кузнеца.
        :param actions: Список доступных действий для взаимодействия.
        """
        super().__init__(name, description, actions=[
            {"name": "Купить предмет", "func": self.show_items_for_sale},
            {"name": "Продать предмет", "func": self.buy_from_player},
            {"name": "Взять квест", "func": self.give_quest},
            {"name": "Починить предмет", "func": self.repair},
            {"name": "Улучшить предмет", "func": self.upgrade},
            {"name": "Создать предмет", "func": self.craft}
        ])
        self.inventory = Inventory()
        self.populate_inventory()

    def populate_inventory(self):
        """Добавляет предметы в инвентарь кузнеца."""
        items_for_sale = [
            Helmet('Шлем', 100, 0.1),
            Chestplate('Нагрудник', 150, 0.2),
            Leggings('Поножи', 120, 1.5 ),
            Boots('Сапоги', 80, 0.5),
            Sword(200, 2.5),
            Dagger(150, 20),
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
            print(f"({i}) {item.name} - {item.price} монет")

        choice = input("Что хотите купить? (0 для отмены): ")
        if choice == "0":
            return

        if choice.isdigit() and 1 <= int(choice) <= len(self.inventory.items):
            item = self.inventory.items[int(choice) - 1]
            if player.gold >= item.price:
                player.gold -= item.price
                player.inventory.add_item(item)
                print(f"Вы купили {item.name} за {item.price} монет.")
            else:
                print("У вас недостаточно монет.")
        else:
            print("Неверный выбор.")

    def buy_from_player(self, player):
        """Позволяет игроку продать предметы."""
        print("Ваш инвентарь:")
        for i, item in enumerate(player.inventory.items, 1):
            print(f"({i}) {item.name} - Цена: {item.get('sell_price', 10)} монет")
        choice = input("Что хотите продать? (0 для отмены): ")
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(player.inventory.items):
            item = player.inventory.items[int(choice) - 1]
            sell_price = item.get("sell_price", 10)
            player.gold += sell_price
            player.inventory.remove_item(item.name)
            print(f"Вы продали {item.name} за {sell_price} монет.")
        else:
            print("Неверный выбор.")

    def repair(self, player):
        """Ремонтирует предметы игрока."""
        repairable_items = []
        print("Ваши предметы:")
        for i, armor in enumerate(player.armor_set.values(), 1):
            if armor:
                print(f"({i}) {armor.name} - Прочность: {armor.durability}/{armor.max_durability}")
                repairable_items.append(armor)
        if player.weapon:
            print(f"({len(repairable_items) + 1}) {player.weapon.name} - Прочность: {player.weapon.durability}/{player.weapon.max_durability}")
            repairable_items.append(player.weapon)
        choice = input("Что хотите починить? (0 для отмены): ")
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(repairable_items):
            item = repairable_items[int(choice) - 1]
            repair_cost = item.price // 2
            if player.gold >= repair_cost:
                player.gold -= repair_cost
                item.durability = item.max_durability
                print(f"Вы починили {item.name} за {repair_cost} монет.")
            else:
                print("У вас недостаточно монет.")
        else:
            print("Неверный выбор.")

    def upgrade(self, player):
        """Улучшает предметы игрока."""
        while True:
            upgradable_items = []
            print("Ваши предметы:")
            for armor in player.armor_set.values():
                if armor:
                    print(f"({len(upgradable_items) + 1}) {armor.name} - Уровень: {armor.upgrade_lvl}")
                    upgradable_items.append(armor)
            if player.weapon:
                print(f"({len(upgradable_items) + 1}) {player.weapon.name} - Уровень: {player.weapon.upgrade_lvl}")
                upgradable_items.append(player.weapon)

            if not upgradable_items:
                print("У вас нет предметов для улучшения.")
                return

            choice = input("Что хотите улучшить? (0 для отмены): ")
            if choice == "0":
                return

            if choice.isdigit() and 1 <= int(choice) <= len(upgradable_items):
                item = upgradable_items[int(choice) - 1]
                upgrade_cost = item.upgrade_lvl * 10
                if player.gold >= upgrade_cost:
                    player.gold -= upgrade_cost
                    item.upgrade_lvl += 1
                    print(f"Вы улучшили {item.name} за {upgrade_cost} монет.")
                else:
                    print("У вас недостаточно монет.")
            else:
                print("Неверный выбор.")

    def craft(self, player):
        """Создаёт предметы для игрока."""
        print("Создание предметов пока не реализовано.")

    def give_quest(self, player):
        """Выдаёт квест игроку."""
        print("Квесты пока не реализованы.")

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

from Charecter import Player

player = Player('Игрок', 100, 20, 50)
citizen = Blacksmith('Прохожий', 'Обычный чел')
player.equip_armor(Helmet('Шлем', 100, 0.1))
player.equip_weapon(Sword(10,10))
player.gold = 40
print(player.armor_set, player.weapon)
citizen.interact(player)
