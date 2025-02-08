from Item import Inventory, Potion, PotionFactory
import random as rn
        
class Character():
    '''Основной класс для работы с персонажами'''
    def __init__(self, name: str, hp: int, damage: int, manabank: int, spells: list = []):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.manabank = manabank
        self.max_hp = hp
        self.inventory = Inventory()
        self.gold = 0
        self.spells = spells

    def is_alive(self):
        return self.hp > 0 
    
    def take_damage(self, damage: int):
        self.hp -= damage
        print(f'{self.name} получает {damage}. У {self.name} остаётся {self.hp}')
        if self.hp <= 0:
            print(f"{self.name} помер")

    def attack_enemy(self, enemy):
        enemy.take_damage(self.damage)

    def learn_spell(self, spell):
        list(set(self.spells))
        self.spells.append(spell)
        print(f"{self.name} изучил заклинание: {spell.name}.")

    def cast_spell(self, spell_name, player, target):
        for spell in self.spells:
            if spell.name == spell_name:
                return spell.cast(player, target)
        print(f"{self.name} не знает заклинания {spell_name}.")
        return False

    def info (self):
        print(f'У него: {self.hp} здоровья\n {self.damage} урона')

    def roll_action(self):
        """
        Определяет результат случайного события (например, успешность побега).
        Возвращает True для успеха, False для неудачи.
        """
        roll = rn.randint(1,100)
        roll2 = rn.randint(1,50)
        if roll > roll2:
            return True
        else:
            return False

class Player(Character):
    '''Класс игрока, в нём при необходимости можно реализовать систему инвенторя и магии'''
    def __init__(self, name: str, hp: int, damage: int, manabank: int):
        super().__init__(name, hp, damage, manabank)
        self.quests = []

    def attack_enemy(self, enemy):
        enemy.take_damage(self.damage)

    def info (self):
        print(f'У персонажа: {self.hp} здоровья\n {self.damage} урона')

    def equip_weapon(self, weapon):
        """Экипирует оружие."""
        self.weapon = weapon
        self.damage += weapon.damage
        print(f"{weapon.type_weapon} экипировано. Урон увеличен на {weapon.damage}.")

    def equip_armor(self, armor):
        """Экипирует броню."""
        self.armor = armor
        print(f"Экипирована броня с поглощением урона: {armor.absorption}.")

class Enemy(Character):
    def __init__(self, name, hp, damage, manabank, spells = []):
        super().__init__(name, hp, damage, manabank, spells)
        self.alive = True
        self.inventory.add_poition_enemy(PotionFactory.give_random_potion().to_dict())

    def take_damage(self, amount):
        self.hp -= amount
        print(f"{self.name} получает {amount} урона. Текущее здоровье: {self.hp}.")
        if self.hp <= 0:
            print(f"{self.name} погиб.")
            self.alive = False

    def use_potion(self):
            """Ищет и использует первое подходящее зелье из инвентаря."""
            for item in self.inventory.items:
                if isinstance(item, Potion):
                    print(f"{self.name} использует {item.name}.")
                    item.use(self)
                    return False
                if item.count <= 0:
                    self.inventory.items.remove(item)  
            print(f"{self.name} не нашёл подходящих зелий в инвентаре.")
            return False
   
    def is_alive(self):
        return self.alive and self.hp > 0
    
    def flee(self):
        """Попытка покинуть поле боя."""
        if self.roll_action() == True:
            print(f"{self.name} убегает с поля боя!")
            self.alive = False
            return True
        else:
            print(f"{self.name} попытался сбежать, но не смог!")
            return False

    def decide_action(self, player):
        """
        Определяет действие врага в зависимости от состояния.
        """
        print(f"{self.name} обдумывает свои действия...")
        
        # Критическое здоровье: пытается лечиться или убежать
        if self.hp <= self.max_hp * 0.3:
            if self.use_potion():
                return "heal"
            if self.flee():
                return "flee"

        # Если манапул позволяет, враг может использовать магию
        if self.manabank >= 10 and rn.random() < 0.3:  # 30% шанс на использование магии
            spell = rn.choice(self.spells)  # Случайное заклинание
            print(f"{self.name} использует магию: {spell}!")
            self.cast_spell(spell, player)
            return "magic"

        # Если игрок сильнее (по здоровью или урону)
        if player.hp > self.hp or player.damage > self.damage:
            if rn.random() < 0.5:  # 50% шанс баффнуть себя
                print(f"{self.name} использует бафф для усиления!")
                self.use_potion()  # Пробует использовать бафф
                return "buff"
            else:
                print(f"{self.name} атакует!")
                return "attack"
        print(f"{self.name} атакует!")
        return "attack"
