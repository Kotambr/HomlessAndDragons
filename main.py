import os
from Charecter import Player
from event import Event, BattleEvent, ChestEvent
from Item import ItemFactory
from Location import LocationManager
import random as rn

class Game:
    def __init__(self):
        self.message_count = 0
        self.game_over = False
        self.player = Player(name='Илюха', hp=1000, damage=100, manabank=100)
        self.chest_event = ChestEvent(player=self.player)
        self.battle = BattleEvent(self.player)
        self.travel = LocationManager(self.player)
        self.event = Event(self.player)
        self.events = {
            'enemy': lambda: self.battle.action(enemy=self.event.create_random_enemy()),
            'item': lambda: ItemFactory.create_random_item().use(target=self.player),
            'nothing': lambda: self.print_message('Ничего не произошло'),
            'chest': self.chest_event.choise,
            'travel': lambda: self.travel.travel()
        }

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

    def play(self):
        """Основной игровой цикл."""
        print("Игра началась, выживет сильнейший")
        while not self.game_over:
            event_name = self.event.roll_event()
            if event_name in self.events:
                self.events[event_name]()
            else:
                self.print_message('Событие не определено.')
            if not self.player.is_alive():
                self.game_over = True
                self.print_message('Game over')

if __name__ == '__main__':
    game = Game()
    game.play()

