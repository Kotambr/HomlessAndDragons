from Item import Inventory, ItemFactory
import random as rn
from event import Event
from armor import Chestplate, Helmet, Leggings, Boots, ArmorFactory
from weapon import Sword, Dagger, MagicalStuff, Projectile, WeaponFactory
from Craft import Craft
from Quest import Quest, QuestLog

side_quest = Quest(
    quest_id=1,
    name="Крафт поршня Лады Веста с правильной геометрией",
    description="Соберите поршень Лады Веста с правильной геометрией.",
    objectives={"Доставть чёрт знает где поршень от Лады Веста": False},
    rewards=None,
    is_main=False
)

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
        lambda: self.populate_inventory()

    def populate_inventory(self):
        """Добавляет предметы в инвентарь торговца."""
        items_for_sale = [
            ItemFactory.create_item('potion', name='Зелье здоровья', effect=('heal', 20), count=1, price=100),
            ItemFactory.create_item('potion', name='Зелье силы', effect=('buff', 20), count=1, price=100),
            ItemFactory.create_item('misc', name='Карта-обманка', effect=lambda target: target.increase_hp(rn.randint(-50, 20)), count=1, price=100),
            ItemFactory.create_item('misc', name='Карта подземки', effect=lambda target: self.event.incrimer_event('chest'), count=1, price=100),
            ItemFactory.create_item('misc', name='Странный мешок', effect=lambda target: self.event.incrimer_event('enemy'), count=1, price=100),
            ItemFactory.create_item('misc', name='Походная книга', effect=lambda target: self.event.incrimer_event('item'), count=1, price=100),
            ItemFactory.create_item('misc', name='Тухлое яйцо', effect=lambda target: self.event.incrimer_event('nothing'), count=1, price=100),
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
            print(f"({i}) {item.name} - Цена: {item.name} {item.price} монет")
        choice = input("Что хотите продать? (0 для отмены): ")
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(player.inventory.items):
            item = player.inventory.items[int(choice) - 1]
            sell_price = item.price
            player.gold += sell_price
            player.inventory.remove_equipment(item.name)
            print(f"Вы продали {item.name} за {sell_price} монет.")
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
        self.actions = [
            {"name": "Задать вопрос", "func": self.ask_of_citizen},
            {"name": "Поговорить", "func": self.talk_to_citizen},
            # {"name": "Взять квест", "func": self.give_quest}
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

    # def give_quest(self, player):
    #     if not self.quests:
    #         print(f"{self.name}: У меня для вас нет заданий.")
    #         return
    #     quest = self.quests.pop(0)
    #     player.quests.append(quest)
    #     print(f"{self.name}: Возьмите это задание: {quest.name}. {quest.description}")

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
        self.item_factory = ItemFactory()
        self.inventory = Inventory()
        self.populate_inventory()
        self.craft_system = Craft()
        self.craft_inventory()

    def populate_inventory(self):
        """Добавляет предметы в инвентарь кузнеца."""
        items_for_sale = [
            self.item_factory.create_item('weapon', name='Меч', damage=10, durability=10, price=20),
            self.item_factory.create_item('weapon', name='Кинжал', damage=5, durability=5, price=10),
            self.item_factory.create_item('armor', name='Шлем', durability=20, absorption=0.1, price=20),
            self.item_factory.create_item('armor', name='Нагрудник', durability=30, absorption=0.2, price=30),
            self.item_factory.create_item('armor', name='Поножи', durability=25, absorption=0.15, price=25),
            self.item_factory.create_item('armor', name='Ботинки', durability=15, absorption=0.05, price=15), 
        ]
        for item in items_for_sale:
            self.inventory.add_item(item)

    def craft_inventory(self):
            self.craft_system.add_recipe('Лук', [{'name': 'Дерево', 'count': 2}, {'name': 'Стрела', 'count': 2}], 'weapon', damage=10, durability=100, price=50),
            self.craft_system.add_recipe('Зелье лечения', [{'name': 'Травы', 'count': 3}, {'name': 'Вода', 'count': 1}], 'potion', effect=('heal', 50), price=100),
            self.craft_system.add_recipe('Кольчуга', [{'name': 'Металл', 'count': 5}], 'armor', durability=50, absorption=0.3, price=100),
            self.craft_system.add_recipe('Кольцо', [{'name': 'Металл', 'count': 1}], 'misc', effect=('increase_hp', 50), price=100),

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
            print(f"({i}) {item.name} - Цена: {item.name} {item.price} монет")
        choice = input("Что хотите продать? (0 для отмены): ")
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(player.inventory.items):
            item = player.inventory.items[int(choice) - 1]
            sell_price = item.price
            player.gold += sell_price
            player.inventory.remove_equipment(item.name)
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
        self.craft_system.move_in_craft(player)

    def give_quest(self, player):
        """Выдаёт квест игроку."""
        pass
        

        

# from Charecter import Player
# quest_log = QuestLog()

# player = Player('Игрок', 100, 20, 50)
# ecet = Event(player)
# cytyzen = Blacksmith('Кузнец', 'Мастер по ковке оружия и брони.')
# cytyzen.interact(player)
# quest_log.show_log()
# quest_log.active_quests[1].update_objective('Доставть чёрт знает где поршень от Лады Веста')
# cytyzen.interact(player) 


