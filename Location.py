import random as rn
from event import BattleEvent
from NPC import Merchant, Quest
from Charecter import Enemy
from Boss import Lich, BossBattleEvent


class Location():
    def __init__(self, player, name: str, description: str):
        self.player = player
        self.name = name
        self.description = description
        self.events = []

    def enter_location(self):
        """Метод, вызываемый при входе в локацию"""
        print(f'{self.player.name} входит в локацию {self.name}')
        self.location_loop()

    def solve_riddle(self, player):
        """Игрок решает загадку и получает награду."""
        riddles = [
            {"question": "Что всегда поднимается, но никогда не опускается?", "answer": "Возраст"},
            {"question": "Что можно держать в правой руке, но никогда в левой?", "answer": "Левую руку"},
            {"question": "Что у всех на виду, но его никто не видит?", "answer": "Воздух"},
        ]
        riddle = rn.choice(riddles)
        print(f"Загадка: {riddle['question']}")
        answer = input("Ваш ответ: ")
        if answer.lower() == riddle["answer"].lower():
            print("Правильно! Вы получаете 50 монет.")
            player.gold += 50
        else:
            print("Неверно! Никакой награды.")

    def find_rare_item(self, player):
        """Игрок может найти редкий предмет."""
        rare_items = [
            {'type': 'Увеличение параметров', 'name': 'Осколок Древнего Бога', 'effect': lambda: self.item, 'count': 1},
            {"name": "Меч Титана", "effect": "Дополнительный урон +20", "rarity": "Epic"},
            {"name": "Кольцо Защитника", "effect": "Уменьшение урона на 10%", "rarity": "Rare"},
        ]
        item = rn.choice(rare_items)
        print(f"Вы нашли редкий предмет: {item['name']}! ({item['rarity']})")
        player.inventory.add_item(item)

    def gather_resources(self, player):
        """Игрок собирает ресурсы."""
        resources = [
            {"name": "Осколки Древности", "count": rn.randint(1, 10)},
            {"name": "Камень", "count": rn.randint(1, 8)},
            {"name": "Палка", "count": rn.randint(1, 5)},
        ]
        resource = rn.choice(resources)
        print(f"Вы нашли {resource['count']} единиц ресурса: {resource['name']}.")
        player.inventory.add_item({"name": resource["name"], "count": resource["count"]})

    def location_loop(self):
        flag_player = False
        event_counter = 0
        while not flag_player:
            print(f'Вы оказались в {self.name}. Первым делом вы решаетесь...\n')
            for i, event in enumerate(self.events, start=1):
                print(f"{i}. {event['name']}")
            try:
                player_choice = int(input("Выберите действие: "))
            except ValueError:
                print("Ошибка: введите число!")
                continue
            for act in self.events:
                if act.get('number') == player_choice:
                    act['func']()
                    event_counter +=1
                    break
            else:
                print("Неверный выбор. Попробуйте снова.")
            if event_counter == 5:
                print("Вы нашли выход из лакуны. Вы решили покинуть локацию.")
                flag_player = True

class AbandonedTemple(Location):
    '''Локация Храм'''
    def __init__(self, player, name: str, description: str):
        super().__init__(player, name, description)
        self.events = [{'number': 1, 'name': 'Загадка на полу', 'func': lambda: self.solve_riddle},
                      {'number': 2, 'name': 'Разграбить храм', 'func': lambda: self.hidden_treasure}]

    def hidden_treasure(self):
        """Скрытое сокровище в храме."""
        print("Вы находите древний сундук, покрытый пылью...")
        loot = [0
        ]
        item = rn.choice(loot)
        print(f"Вы находите: {item['name']} ({item['rarity']})!")
        self.player.inventory.add_item(item)

class CampfireLocation(Location):
    '''Локация Костёр. Можно отдохнуть и встретить NPC Торговца'''
    def __init__(self, player, name: str, description: str):
        super().__init__(player, name, description)
        self.battle = BattleEvent(player)
        self.trader = Merchant(
            name="Торгаш",
            inventory=self.create_trader_inventory(),
            quests=[
                Quest(
                    name="Принести 10 грибов",
                    description="Соберите 10 грибов в лесу и принесите мне.",
                    reward=50,
                    condition=lambda p: p.inventory.has_item("Гриб", 10)
                )
            ]
        )
        self.events = [{'number': 1, 'name': 'Отдохнуть', 'func': self.rest},
                       {'number': 2, 'name': 'Прогуляться', 'func': self.encounter_enemy},
                       {'number': 3, 'name': 'Поторговать', 'func': self.visit_trader}
        ]

    def rest(self):
        """Восстановление здоровья у костра."""
        print("Вы отдыхаете у костра и восстанавливаете 20 HP.")
        self.player.hp = min(self.player.max_hp, self.player.hp + 20)

    def encounter_enemy(self):
        """Случайная встреча с врагом."""
        enemy = Enemy(
            name=rn.choice(["Гоблин убийца из Подворотни", "Орк грабитель Костров", "Разбойник Мафиози"]),
            hp=rn.randint(50, 100),
            damage=rn.randint(10, 20),
            manabank=0
        )
        print(f"На вас нападает {enemy.name}!")
        self.battle.fight(enemy)

    def visit_trader(self):
        """Встреча с торговцем."""
        print(f"Вы встречаете торговца {self.trader.name}.")
        self.trader.interact(self.player)

    def travel_to_forest(self):
        """Событие перехода в другую локацию."""
        print("Вы замечаете тропу, ведущую в лес.")
        choice = input("Хотите отправиться в лес? (да/нет): ")
        if choice.lower() in ["да", "yes"]:
            self.location_manager.travel('Лес')
            
class ForestLocation(Location):
    '''Локация Лес. (Что она делает в подземелье?). Можно собрать ингридиеты и сразится'''
    def __init__(self, player, name: str, description: str):
        super().__init__(player, name, description)
        self.events = [self.find_herbs, self.encounter_enemy]
        self.events = [{'number': 1,'name': 'Собрать травы', 'func': lambda: self.find_herbs},
                       {'number': 2,'name': 'Прогуляться', 'func': lambda: self.encounter_enemy}
        ]

    def find_herbs(self):
        """Поиск трав в лесу."""
        herbs_found = rn.randint(1, 5)
        print(f"Вы находите {herbs_found} лечебных трав.")
        self.player.inventory.add_item({"name": "Гриб", "count": herbs_found})
        return

    def encounter_enemy(self):
        """Встреча с врагом в лесу."""
        enemy = Enemy(
            name=rn.choice(["Волчара Цитатник", "Разбойник-Кинйобзра", "Кабан Решала"]),
            hp=rn.randint(40, 80),
            damage=rn.randint(8, 15),
            manabank=0
        )
        print(f"На вас нападает {enemy.name}!")
        battle = BattleEvent(self.player)
        battle.fight(enemy)

class MountainRegion(Location):
    '''Горы. Охота и битвы'''
    def __init__(self, player, name: str, description: str):
        super().__init__(player, name, description)
        self.events = [self.gather_resources, self.wild_animal_attack]

    def wild_animal_attack(self):
        """На игрока нападает дикое животное."""
        enemy = Enemy(
            name=rn.choice(["Горный медведь", "Снежный волк", "Разбойник"]),
            hp=rn.randint(70, 120),
            damage=rn.randint(15, 25),
            manabank=0
        )
        print(f"На вас нападает {enemy.name}!")
        battle = BattleEvent(self.player)
        battle.fight(enemy)

class HiddenSanctuary(Location):
    '''Святилище. Можно найти интересные предметы и получить бафф'''
    def __init__(self, player, name: str, description: str):
        super().__init__(player, name, description)
        self.events = [self.find_rare_item, self.mystic_event]

    def mystic_event(self):
        """Событие в святилище."""
        print("Вы чувствуете странную магическую ауру...")
        outcomes = [
            "Ваше здоровье полностью восстановлено.",
            "Вы находите редкий артефакт."
        ]
        outcome = rn.choice(outcomes)
        print(outcome)
        if "здоровье" in outcome:
            self.player.hp = self.player.max_hp
        elif "артефакт" in outcome:
            self.player.inventory.add_item({"name": "Мистический амулет", "rarity": "Legendary"})

class FishingVillage(Location):
    '''Рыбацкая деревня. Рыбалка. NPC Рыбак.'''
    def __init__(self, player, name: str, description: str):
        super().__init__(player, name, description)
        self.events = [self.fishing_event, self.visit_fisherman]

    def fishing_event(self):
        """Рыбалка."""
        catch = [
            {"name": "Маленькая рыба", "price": 5},
            {"name": "Большая рыба", "price": 15},
            {"name": "Редкая жемчужина", "price": 50},
        ]
        fish = rn.choice(catch)
        print(f"Вы поймали: {fish['name']}. Стоимость: {fish['price']} монет.")
        self.player.inventory.add_item(fish)

    def visit_fisherman(self):
        """Встреча с рыбаком."""
        print("Вы встречаете старого рыбака. Он предлагает вам обменять рыбу на уникальные предметы.")
        # Пример диалога с NPC (торговля, квесты)

class Graveyard(Location):
    '''Кладбище. Локация с боссом и возможностью лута'''
    def __init__(self, player, name, description):
        super().__init__(player, name, description)
        self.event = [self.bossBattle]
        self.Lich = Lich("Лич", hp=400, damage=20, manabank=100,
            loot=None)
        self.battle = BossBattleEvent(player, self.Lich)

    def bossBattle(self, player):
        '''Инициализатор, битвы с боссом локации'''
        self.battle.fight()

    def loot_a_grave(self):
        '''Разгробление могилы'''
        pass

    def fight_at_mortal(self):
        '''Битва с врагами'''
        pass

class City(Location):
    '''Город. Локация с большим количеством NPC'''
    pass

class TheFort(Location):
    '''Форт. Встречаются задания на мобов, так же есть торговцы'''
    pass

class AncientAltar(Location):
    '''Древний алтарь. Можно выучить заклинание или найти осколок Чар'''
    pass

class LocationManager:
    def __init__(self, player):
        self.player = player
        self.current_location = None  # Текущая локация игрока
        self.location_list = [
            AbandonedTemple(player, "Заброшенный Храм", "Древнее место, полное загадок и сокровищ."),
            MountainRegion(player, "Горы", "Опасный регион с дикими животными."),
            FishingVillage(player, "Рыбацкая Деревня", "Тихое место для отдыха и рыбалки."),
            HiddenSanctuary(player, "Святилище", "Мистическое место, скрытое от глаз."),
            Graveyard(player, 'Кладбище', 'Тишина и мрак окутывают захоронения')
        ]

    def enter_location(self, location_name: str):
        """Переход в указанную локацию."""
        for location in self.location_list:
            if location.name == location_name:
                self.current_location = location
                self.current_location.enter_location()
                return
        print(f"Локация '{location_name}' не найдена.")

    def list_locations(self):
        """Выводит список доступных локаций."""
        print("Доступные локации:")
        for location in self.location_list:
            print(f"- {location.name}: {location.description}")

    def travel(self):
        """Метод для выбора новой локации."""
        if not self.location_list:
            print("Нет доступных локаций для путешествия.")
            return
        self.list_locations()
        choice = input("Введите название локации, куда хотите отправиться: ")
        self.enter_location(choice)

from Charecter import Player
Playere = Player('1',10,10,10)
forest = ForestLocation(Player,None,None)
forest.location_loop()