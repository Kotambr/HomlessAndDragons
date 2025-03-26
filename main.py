import os
from Charecter import Player
from event import Event, BattleEvent, ChestEvent
from Item import ItemFactory
from Location import LocationManager
import random as rn
from Quest import Quest, QuestLog

main_quest = Quest(quest_id=1,
                   name='Попал так попал...',
                   description='''Багровый закат догорал за горизонтом, когда ваша видавшая виды «пятёрка», 
                надрывно воя мотором, пробиралась сквозь ухабы и рытвины забытой богом просёлочной дороги. 
                Казалось, ничто не предвещало беды, лишь назойливое жужжание комаров и мерный стук подвески аккомпанировали вашему путешествию. 
                Но внезапно, небо раскололось от оглушительного рёва, и в багряном зареве появился 
                ОН – дракон, древний и могущественный, чья чешуя искрилась в последних лучах солнца.
                Не успели вы и глазом моргнуть, как чудовище обрушилось на ваш автомобиль, словно игрушку. Металл заскрежетал, стекла разлетелись вдребезги, и всё погрузилось в хаос огня и боли. А затем – тьма.
                Когда вы пришли в себя, то обнаружили себя лежащим на незнакомой земле под сенью гигантских деревьев.
                Зловещая тишина окружала вас, нарушаемая лишь странными шорохами и криками невиданных существ. 
                Ваша верная «пятёрка», испепелённая и изувеченная, валялась неподалёку, словно предостережение. 
                Вы – в совершенно чужом, враждебном мире, куда вас забросила ненасытная пасть дракона. 
                И теперь, чтобы выжить и найти дорогу домой, вам предстоит раскрыть тайны этого места, обрести новых союзников и, возможно, отомстить за свою «ласточку».''',
                objectives={
                'Этап первый: Доберитесь до лакуны Город': False,
                'Этап второй: Получив информацию от местных жителей, отправьтесь в лес к своей "пятёрке"': False,
                'Этап третий: Найдите недостающие агрегаты для авто': False, 
                'Этап четвертый: Победите дракона': False},
                rewards=None, giver=None, is_main=True)



class Game:
    def __init__(self):
        self.message_count = 0
        self.game_over = False
        self.player = Player(name='Илюха', hp=1000, damage=100, manabank=100)
        self.chest_event = ChestEvent(player=self.player)
        self.battle = BattleEvent(self.player)
        self.travel = LocationManager(self.player)
        self.event = Event(self.player)
        self.quest_log = QuestLog()
        self.quest_log.add_quest(main_quest)
        self.events = {
            'enemy': lambda: self.battle.action(enemy=self.event.create_random_enemy()),
            'item': lambda: self.player.inventory.add_item(ItemFactory.create_random_item()),
            'nothing': lambda: self.print_message('Ничего не произошло'),
            'chest': lambda: self.chest_event.choise(),
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
        os.system('cls' if os.name == 'nt' else 'clear')
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

