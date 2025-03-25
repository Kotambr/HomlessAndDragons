import curses
import os
from enemy_factory import EnemyFactory, Mage, Warrior, Thief, Jester, Animal, Mimic, EnemyNameGenerator
import random as rn
from spell import SpellFactory
from Item import Item
from animations import animate_attack, animate_magic, animate_run

class Event:
    '''Класс для событий, в нём нужно определить события'''
    def __init__(self, player):
        self.player = player
        self.events_list = [
            {'name': 'enemy', 'chance': 40},
            {'name': 'chest', 'chance': 20},
            {'name': 'item', 'chance': 25},
            {'name': 'nothing', 'chance': 10},
            {'name': 'travel', 'chance': 5}
        ]
        self.fixed_increase = 5
        self.message_count = 0
        self.enemy_factory = EnemyFactory()

    def create_random_enemy(self):
        classes = [Mage, Warrior, Thief, Jester, Animal, Mimic]
        enemy_class = rn.choice(classes)(rn.choice(classes).__name__)
        enemy_class.distribute_attributes()
        name = EnemyNameGenerator.generate_name(enemy_class.__class__.__name__)
        return self.enemy_factory.create_enemy(name, enemy_class.hp, enemy_class.damage, enemy_class.manabank)
    
    def roll_event(self):
        roll = rn.randint(1, 100)
        cumulative_chance = 0 
        for event in self.events_list:
            cumulative_chance += event["chance"]
            if roll <= cumulative_chance:
                return event["name"]
        return "Ничего не произошло."  
    
    def incrimer_event(self, event_name):
        for event in self.events_list:
            if event['name'] == event_name:
                event['chance'] += self.fixed_increase
                break
        else:
            print(f"Событие с именем '{event_name}' не найдено.")
            return
        total_chance = sum(event['chance'] for event in self.events_list)
        if total_chance >= 100:
            for event in self.events_list:
                event['chance'] = 10

    def clear_console(self):
        """Очистка консоли после 20 строк сообщений."""
        self.message_count += 1
        if self.message_count >= 20:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.message_count = 0

    def print_message(self, message):
        """Вывод сообщения с очисткой консоли."""
        print(message)
        self.clear_console()

class ChestEvent(Event):
    def __init__(self, player):
        super().__init__(player)
        self.mimick = [
            self.enemy_factory.create_enemy('Мимик-Сундук', 100, 10, 10),
            self.enemy_factory.create_enemy('Мимик-Бочка', 100, 10, 10),
            self.enemy_factory.create_enemy('Мимик-Комод', 100, 10, 10),
        ]
        self.battle = BattleEvent(player=player)
        self.game_over = False
        self.events_chest = [
            {'name': 'mimick', 'chance': 20, 'funck': lambda: self.battle.action(rn.choice(self.mimick))},
            {'name': 'item', 'chance': 30, 'funck': lambda: self.items.find_item(self.player)},
            {'name': 'nothing', 'chance': 30, 'funck': lambda: self.print_message('Вы ничего не нашли')},
            {'name': 'death', 'chance': 1, 'funck': lambda: self.print_message('помер')},
            {'name': 'magic', 'chance': 5, 'funck': lambda: self.player.learn_spell(SpellFactory.create_random_spell())},
        ]

    def choise(self):
        result = self.event_in_chest()
        if result is None:
            self.print_message('Ничего не произошло.')
            return

        self.event_name, self.is_mimick, self.mimick_obj = result
        if self.is_mimick == "mimick":
            choice = input(f'Вы нашли {self.mimick_obj.name[:6]}! Открыть? \n(1) Да \n(2) Нет! \n')
        else:
            choice = input('Вы нашли сундук! Открыть? \n(1) Да \n(2) Нет! \n')
        
        actions = [
            {'number': '1', 'funck': lambda: self.event_name()},
            {'number': '2', 'funck': lambda: self.print_message('Вы уходите')}
        ]
        for act in actions:
            if act['number'] == choice:
                act['funck']()
                break
        else:
            self.print_message('Неверный выбор')

    def event_in_chest(self):
        roll = rn.randint(1, 100)
        cumulative_chance = 0

        for event in self.events_chest:
            cumulative_chance += event["chance"]
            if roll <= cumulative_chance:
                if event["name"] == "mimick":
                    mimick_obj = rn.choice(self.mimick)
                    return event["funck"], event["name"], mimick_obj
                return event["funck"], event["name"], None
        return None

class BattleEvent(Event):
    def __init__(self, player):
        super().__init__(player)
        self.player = player
        self.action_list = [
            {'number': '1', 'func': lambda enemy: self.attack(enemy), 'enemy': True},
            {'number': '2', 'func': lambda enemy: self.run(enemy), 'enemy': True},
            {'number': '3', 'func': lambda enemy: self.mage_attack(self.player, enemy),'enemy': True},
            {'number': '4', 'func': lambda: self.open_inventory(), 'enemy': False}
        ]
        self.enemies = []
        self.enemy_action = [
            {'action': 'attack', 'func': lambda player: self.enemies.attack_enemy(player), 'player': True},
            {'action': 'flee', 'func': lambda: self.enemies.flee(), 'player': False},
            {'action': 'buff', 'func': lambda: self.enemies.use_potion(), 'player': False}
]       

    def attack(self, enemy):
        """
        Игрок атакует врага, а если враг жив, он отвечает атакой.
        """
        self.print_message(f'{self.player.name} атакует {enemy.name}!')
        curses.wrapper(animate_attack, self.player, enemy, self.player, enemy)
        self.player.attack_enemy(enemy)
        if enemy.is_alive():
            self.print_message(f'{enemy.name} атакует {self.player.name}!')
            curses.wrapper(animate_attack, enemy, self.player, self.player, enemy)
            enemy.attack_enemy(self.player)

    def run(self, enemy):
        """
        Попытка сбежать от врага. Если сбежать удалось, возвращается True.
        """
        self.print_message(f'{self.player.name} пытается сбежать!')
        curses.wrapper(animate_run)
        if self.player.roll_action: 
            self.print_message('Вы успешно сбежали!')
            return True
        else:
            self.print_message('Вы не смогли сбежать! Враг атакует!')
            curses.wrapper(animate_attack, enemy, self.player, self.player, enemy)
            enemy.attack_enemy(self.player)
            return False

    def mage_attack(self, player, enemy):
        """
        Игрок использует магическое заклинание против врага.
        """
        available_spells = [spell.name for spell in player.spells]
        if not available_spells:
            self.print_message('У вас нет доступных заклинаний!')
            return
        spell_name = input(f'Выберите заклинание ({", ".join(available_spells)}): ')
        self.print_message('')
        curses.wrapper(animate_magic, player, enemy)
        player.cast_spell(spell_name, player, enemy)
        if not enemy.is_alive():
            self.enemies.remove(enemy)
            self.print_message(f'{enemy.name} побежден и удален из списка врагов.')

    def open_inventory(self):
        """
        Открытие инвентаря игрока.
        """
        self.print_message('Открытие инвентаря...')
        self.player.inventory.show_inventory()

    def action(self, enemy):
        """
        Выводит доступные действия игрока в бою.
        :param enemy: Объект врага, с которым идёт бой.
        """
        self.print_message(f"Вы вступили в бой с {enemy.name}!")

        self.enemy_action = [
            {'action': 'attack', 'func': lambda player: enemy.attack_enemy(player), 'player': True},
            {'action': 'flee', 'func': lambda: enemy.flee(), 'player': False},
            {'action': 'buff', 'func': lambda: enemy.use_potion(), 'player': False}
        ]

        while enemy.is_alive() and self.player.is_alive():
            # Действия игрока
            action = input(
                f'{self.player.name}, ваши действия: \n'
                '(1) Атака\n'
                '(2) Бег\n'
                '(3) Магия\n'
                '(4) Открыть инвентарь\n'
                'Ваш выбор: '
            )
            self.clear_console()
            for act in self.action_list:
                if act['number'] == action:
                    # Выполнение действия игрока
                    result_player = (
                        act['func'](enemy)
                        if act.get('enemy', False)
                        else act['func']()
                    )
                    if result_player is True:  # Например, успешный побег
                        self.print_message("Бой завершён.")
                        return
                    break
            else:
                self.print_message("Неверный выбор. Попробуйте снова.")
                continue

            # Проверка состояния после действия игрока
            if not enemy.is_alive():
                self.print_message(f"Вы победили {enemy.name}!")
                return

            # Действия врага
            enemy_decide = enemy.decide_action(self.player)
            for act_enemy in self.enemy_action:
                if act_enemy['action'] == enemy_decide:
                    if act_enemy.get('player', False):
                        result_enemy = act_enemy['func'](self.player)
                    else:
                        result_enemy = act_enemy['func']()
                    if result_enemy is True:  # Например, успешный побег врага
                        self.print_message(f"{enemy.name} сбежал. Бой завершён.")
                        return
                    break

            # Проверка состояния после действия врага
            if not self.player.is_alive():
                self.game_over = True
                self.print_message("Игра окончена. Вы проиграли.")
                return

class MimicEvent(BattleEvent):
    def __init__(self, player):
        super().__init__(player)
        self.player = player
        self.mimic = self.create_mimic()

    def create_mimic(self):
        mimic_class = Mimic("Mimic")
        mimic_class.distribute_attributes()
        name = EnemyNameGenerator.generate_name("Mimic")
        return self.enemy_factory.create_enemy(name, mimic_class.hp, mimic_class.damage, mimic_class.manabank)

    def encounter_mimic(self):
        print(f"Вы нашли {self.mimic.name}. Вы можете пройти мимо или взаимодействовать с ним.")
        action = input(" '1' чтобы взаимодействовать или '2' чтобы пройти мимо: ")
        if action.lower() == '1':
            print(f"Мимик атакует! Начинается битва с {self.mimic.name}.")
        else:
            print("Вы прошли мимо мимика.")

