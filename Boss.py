from Charecter import Enemy
from links import rn
from Item import Item
from weapon import Weapon
from armor import Armor
from spell import AttackSpell, HealingSpell
from event import BattleEvent

class Boss(Enemy):
    def __init__(self, name, hp, damage, manabank, loot=None):
        super().__init__(name, hp, damage, manabank)
        self.loot = loot if loot else []
        self.phase = 1  
        self.spells = []
        self.minions = []
        self.item_class = Item()  # Передаём player в Item
        self.actions = {
            "attack": self.attack_enemy,
            "special_attack": self.special_attack,
            "summon_minions": self.summon_minions,
            "use_ability": self.use_ability,
        }

    def decide_action(self, player):
        """Определяет действие босса."""
        action_name = rn.choice(list(self.actions.keys()))
        action = self.actions.get(action_name)
        if action:
            action(player)

    def special_attack(self, player):
        """Стандартная особая атака босса."""
        print(f"{self.name} использует мощную атаку!")
        player.take_damage(self.damage * 2)

    def summon_minions(self, player=None):
        """Босс вызывает миньонов, которые участвуют в бою."""
        if self.minions:
            print(f"{self.name} уже вызвал миньонов.")
            return

        print(f"{self.name} вызывает миньонов!")
        self.minions = [
            Enemy(name="Скелет", hp=50, damage=10, manabank=0),
            Enemy(name="Зомби", hp=70, damage=8, manabank=0),
        ]


    def use_ability(self, player):
        """
        Использует уникальную способность босса.
        :param player: Игрок, против которого направлено действие.
        """
        if self.spells:
            ability = rn.choice(self.spells)
            print(f"{self.name} использует {ability['name']}!")
            ability['effect'](self, player)  


    def take_damage(self, amount):
        """Получение урона. Переход в следующую фазу при достижении порога здоровья."""
        self.hp -= amount
        print(f"{self.name} получает {amount} урона. Текущее здоровье: {self.hp}.")
        if self.hp <= 0:
            print(f"{self.name} погиб.")
            self.drop_loot()
        elif self.hp <= self.max_hp * 0.5 and self.phase == 1:
            self.phase += 1
            print(f"{self.name} переходит на вторую фазу!")
            self.phase_two()

    def phase_two(self):
        """Вторая фаза босса."""
        print(f"{self.name} становится сильнее! Урон увеличен.")
        self.damage += 10

    def drop_loot(self):
        """Генерация лута."""
        loot_table = [
            {"type": "item", "class": "item", "args": None},
            {"type": "weapon", "class": Weapon, "args": {"type_weapon": "Меч", "damage": 30, "weapon_count": 100}},
            {"type": "armor", "class": Armor, "args": {"armor_type": "Нагрудник", "durability": 50, "absorption": 10}},
        ]
        loot = rn.choice(loot_table)
        if loot["class"] == "item":
            item = rn.choice(self.item_class.items)
            print(f"{self.name} оставляет после себя {item['name']}!")
            return item
        else:
            loot_item = loot["class"](**loot["args"])
            print(f"{self.name} оставляет после себя {loot_item}.")
            return loot_item

class Lich(Boss):
    def __init__(self, name, hp, damage, manabank, loot=None):
            super().__init__(name, hp, damage, manabank, loot)
            self.deathRay = AttackSpell('Луч смерти', 10, 20)
            self.spells = [
                {"name": "Заморозка", "effect": self.freeze_player},
                {"name": "Ледяная броня", "effect": self.death_ray},
                {'name': 'Магическое слово: Смерть', 'effect': self.deathWord},
                {'name': 'Удар', 'effect': self.punch},
                {'name': 'Костяные Шипы', 'effect': self.special_attack}
            ]
            self.loot_table = [
            {"type": "item", "class": Item, "args": {"name": "Зелье здоровья", "effect": lambda p: p.increase_hp(20), "count": 1}},
            {"type": "weapon", "class": Weapon, "args": {"type_weapon": "Меч", "damage": 30, "weapon_count": 100}},
            {"type": "armor", "class": Armor, "args": {"armor_count": 50, "absorption": 10}},
        ]

    def freeze_player(self, boss, player):
        """Замораживает игрока, снижая его урон."""
        print(f"{boss.name} замораживает {player.name}, снижая его урон!")
        player.damage = max(0, player.damage - 10)

    def special_attack(self, player):
        """Особая атака босса."""
        print(f"{self.name} использует смертельный холод!")
        player.take_damage(self.damage * 1.5)
        self.heal(50)
        print(f"{self.name} восстанавливает 50 HP.")

    def punch(self, boss, player):
        """Наносит удар по игроку."""
        print(f"{boss.name} наносит удар по {player.name}!")
        player.take_damage(30)  

    def death_ray(self, boss, player):
        print(f"{boss.name} стреляет Лучём смерти!")
        boss.cast_spell((self, 'Луч смерти', boss, player))
    
    def deathWord(self, boss, player):
        '''Наносит большой урон по игроку'''
        print(f'{boss.name} выкрикивает {'pullum zedha mo'.upper()}')
        player.hp = rn.randint(min(player.hp), max(player.hp))

    def heal(self, amount):
        """Восстанавливает здоровье."""
        self.hp += amount
        print(f"{self.name} восстанавливает {amount} здоровья. Текущее здоровье: {self.hp}")

    def summon_minions(self, player):
        """Лич вызывает миньонов."""
        print(f"{self.name} вызывает скелетов!")
        self.minions = [
            Enemy("Скелет-Воин", hp=60, damage=15, manabank=0),
            Enemy("Скелет-Маг", hp=40, damage=20, manabank=50),
        ]
    
class BossBattleEvent(BattleEvent):
    def __init__(self, player, boss):
        super().__init__(player)
        self.boss = boss

    def display_status(self):
        """Выводит текущее состояние боя."""
        print("\n===================== Битва =====================")
        print(f"Босс: {self.boss.name} - HP: {self.boss.hp}/{self.boss.max_hp}")
        if self.boss.minions:
            print("Миньоны:")
            for i, minion in enumerate(self.boss.minions, 1):
                print(f"  ({i}) {minion.name} - HP: {minion.hp}/{minion.max_hp}")
        print(f"Игрок: {self.player.name} - HP: {self.player.hp}/{self.player.max_hp}")
        print("================================================")

    def fight(self):
        """Процесс боя."""
        print(f"Вы вступаете в битву с {self.boss.name}!")
        actions = {
            "1": lambda: self.player.attack_enemy(self.boss),
            "2": self.attack_minion,
            "3": self.mage_attack,
            "4": lambda: self.run(self.boss),
            '5': lambda: self.player.inventory.show_inventory(),
        }

        while self.boss.is_alive() and self.player.is_alive():
            self.display_status()

            # Действия игрока
            act = input(
                f'{self.player.name}, ваши действия: \n'
                '(1) Атака\n'
                '(2) Атака поддержки\n'
                '(3) Магия\n'
                '(4) Побег\n'
                '(5) Инвентарь\n'
                'Ваш выбор: '
            )

            action = actions.get(act)
            if action:
                action()
            else:
                print("Неверный выбор!")

            # Проверка состояния после действий игрока
            if not self.boss.is_alive():
                print(f"Вы победили босса {self.boss.name}!")
                return
            if not self.player.is_alive():
                print("Вы погибли...")
                return

            # Действия босса
            self.boss.decide_action(self.player)

            # Действия миньонов
            self.minions_turn()

    def attack_minion(self):
        """Игрок атакует одного из миньонов."""
        if not self.boss.minions:
            print("Нет миньонов для атаки.")
            return

        print("Выберите миньона для атаки:")
        for i, minion in enumerate(self.boss.minions, 1):
            print(f"({i}) {minion.name} - HP: {minion.hp}/{minion.max_hp}")
        choice = input("Ваш выбор: ")
        if choice.isdigit() and 1 <= int(choice) <= len(self.boss.minions):
            minion = self.boss.minions[int(choice) - 1]
            self.player.attack_enemy(minion)
            if not minion.is_alive():
                print(f"{minion.name} побеждён!")
                self.boss.minions.remove(minion)
        else:
            print("Неверный выбор.")

    def mage_attack(self):
        """Использует магию игрока."""
        available_spells = [spell.name for spell in self.player.spells]
        if not available_spells:
            print('Нет доступных заклинаний!')
            return
        spell_name = input(f'Выберите заклинание ({", ".join(available_spells)}): ')
        self.player.cast_spell(spell_name, self.boss)

    def minions_turn(self):
        """Миньоны атакуют игрока."""
        for minion in self.boss.minions:
            if minion.is_alive():
                print(f"{minion.name} атакует {self.player.name}!")
                minion.attack_enemy(self.player)


    def handle_loot(self, loot):
        """Обрабатывает лут, выпавший с босса."""
        if isinstance(loot, dict):  # Лут из Item.items
            self.player.inventory.add_item(loot)
            print(f"Предмет добавлен в инвентарь: {loot['name']}.")
        elif isinstance(loot, Weapon):
            if not self.player.weapon or loot.damage > self.player.weapon.damage:
                self.player.equip_weapon(loot)
                print(f"{loot.type_weapon} экипировано!")
            else:
                print(f"{loot.type_weapon} хуже вашего текущего оружия и не экипировано.")
        elif isinstance(loot, Armor):
            if not self.player.armor or loot.absorption > self.player.armor.absorption:
                self.player.equip_armor(loot)
                print(f"Броня экипирована: {loot.absorption} поглощение урона.")
            else:
                print("Броня хуже текущей и не экипирована.")