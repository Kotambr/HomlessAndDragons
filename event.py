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
    
    @staticmethod
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
    def __init__(self, player, items):
        super().__init__(player)
        self.items = items
        self.mimick = [
            self.enemy_factory.create_enemy('Сундук', 100, 10, 10),
            self.enemy_factory.create_enemy('Бочка', 100, 10, 10),
            self.enemy_factory.create_enemy('Комод', 100, 10, 10),
        ]
        self.battle = BattleEvent(player=player)
        self.game_over = False
        self.events_chest = [
            {'name': 'mimick', 'chance': 20, 'funck': lambda : self.battle.action(rn.choice(self.mimick))},
            {'name': 'item', 'chance': 30, 'funck': lambda: self.items.find_item(self.player)},
            {'name': 'nothing', 'chance': 30, 'funck': lambda: self.print_message('Вы ничего не нашли')},
            {'name': 'death', 'chance': 1, 'funck': lambda: self.print_message('помер')},
            {'name': 'magic', 'chance': 5, 'funck': lambda: self.player.learn_spell(SpellFactory.create_random_spell())},
        ]

    def choise(self):
        choice = input('Вы нашли сундук! Открыть? \n(1) Да \n(2) Нет! \n')
        actions = [
            {'number': '1', 'funck': lambda: self.open_chest()},
            {'number': '2', 'funck': lambda: self.print_message('Вы уходите')}
        ]
        for act in actions:
            if act['number'] == choice:
                act['funck']()
            else:
                self.print_message('Неверный выбор')

    def open_chest(self):
        roll = rn.randint(1, 100)
        cumulative_chance = 0

        for event in self.events_chest:
            cumulative_chance += event["chance"]
            if roll <= cumulative_chance:
                event["funck"]() 
                return
        self.print_message("Ничего не произошло.")

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
<<<<<<< HEAD
        self.enemies = [
            self.create_random_enemy(),
            self.create_random_enemy(),
            self.create_random_enemy()
        ]
        self.enemy_action = [
            {'action': 'attack', 'func': lambda player: self.enemies[0].attack_enemy(player), 'player': True},
            {'action': 'flee', 'func': lambda: self.enemies[0].flee(), 'player': False},
            {'action': 'buff', 'func': lambda: self.enemies[0].use_potion(), 'player': False}
        ]
=======
        self.enemies = []
        self.enemy_action = [
            {'action': 'attack', 'func': lambda player: self.enemies.attack_enemy(player), 'player': True},
            {'action': 'flee', 'func': lambda: self.enemies.flee(), 'player': False},
            {'action': 'buff', 'func': lambda: self.enemies.use_potion(), 'player': False}
]       
    def create_enemies(self):
        if not self.enemies:
            self.enemies = [self.create_random_enemy() for _ in range(3)]

>>>>>>> 6068af9 (Изменение боёвки)

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

<<<<<<< HEAD
=======

>>>>>>> 6068af9 (Изменение боёвки)
    def run(self, enemy):
        """
        Попытка сбежать от врага. Если сбежать удалось, возвращается True.
        """
        self.print_message(f'{self.player.name} пытается сбежать!')
        curses.wrapper(animate_run)
        if self.player.roll_action: 
            self.print_message('Вы успешно сбежали!')
<<<<<<< HEAD
=======

>>>>>>> 6068af9 (Изменение боёвки)
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
<<<<<<< HEAD
=======
        if not enemy.is_alive():
            self.enemies.remove(enemy)
            self.print_message(f'{enemy.name} побежден и удален из списка врагов.')
>>>>>>> 6068af9 (Изменение боёвки)

    def open_inventory(self):
        """
        Открытие инвентаря игрока.
        """
        self.print_message('Открытие инвентаря...')
        # curses.wrapper(animate_inventory)
        self.player.inventory.show_inventory()

    def action(self, enemy):
        """
        Выводит доступные действия игрока в бою.
        :param enemy: Объект врага, с которым идёт бой.
        """
<<<<<<< HEAD
=======
        enemy = self.create_random_enemy()
>>>>>>> 6068af9 (Изменение боёвки)
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

class MimicEvent(Event):
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
        action = input("Введите 'взаимодействовать' чтобы взаимодействовать или 'пройти' чтобы пройти мимо: ")
        if action.lower() == 'взаимодействовать':
            print(f"Мимик атакует! Начинается битва с {self.mimic.name}.")
            # Логика битвы с мимиком
        else:
            print("Вы прошли мимо мимика.")

<<<<<<< HEAD
# Пример использования
if __name__ == '__main__':
    player = None  # Здесь должен быть объект игрока
    event = MimicEvent(player)
    event.encounter_mimic()
=======
>>>>>>> 6068af9 (Изменение боёвки)
