import random as rn

class Armor:
    '''Первичный класс для брони'''
    def __init__(self, armor_type, durability, absorption):
        """
        :param armor_type: Тип брони (например, "Шлем", "Нагрудник").
        :param durability: Прочность брони.
        :param absorption: Поглощение урона.
        """
        self.armor_type = armor_type
        self.durability = durability
        self.absorption = absorption

    def absorb_damage(self, damage: int):
        absorbed = damage * self.absorption
        self.durability -= absorbed
        return max(0, damage - absorbed)  # Оставшийся урон, если броня не поглотила полностью

    def is_broken(self):
        return self.durability <= 0

    def __str__(self):
        return f"{self.armor_type} (Прочность: {self.durability}, Поглощение: {self.absorption})"


class Helmet(Armor):
    def __init__(self, armor_type, durability, absorption):
        super().__init__(armor_type, durability, absorption)

class Chestplate(Armor):
    def __init__(self, armor_type, durability, absorption):
        super().__init__(armor_type, durability, absorption)
        
class Leggings(Armor):
    def __init__(self, armor_type, durability, absorption):
        super().__init__(armor_type, durability, absorption)

class Boots(Armor):
    def __init__(self, armor_type, durability, absorption):
        super().__init__(armor_type, durability, absorption)

class ArmorSet:
    '''Класс для управления комплектом брони'''
    def __init__(self, helmet: Helmet, chestplate: Chestplate, leggings: Leggings, boots: Boots):
        self.armor_pieces = [helmet, chestplate, leggings, boots]

    def check_armor(self):
        for armor in self.armor_pieces:
            if armor.is_broken():
                print(f"{armor.armor_type} сломался!")
            else:
                print(f"{armor.armor_type} в порядке, прочность: {armor.durability}")

    def absorb_damage(self, damage):
        for armor in self.armor_pieces:
            if not armor.is_broken():
                damage = armor.absorb_damage(damage)
                if damage <= 0:
                    break  # Все урон поглощен
        return damage  # Остаточный урон, если броня не поглотила все

class ArmorFactory:
    '''Класс для генерации случайной брони'''
    @staticmethod
    def create_random_armor():
        armor_types = [Helmet, Chestplate, Leggings, Boots]
        armor_type = rn.choice(armor_types)  # Случайно выбираем тип брони
        armor_count = rn.randint(50, 150)    # Случайная прочность от 50 до 150
        absorption = round(rn.uniform(0.1, 0.4), 2)  # Случайное поглощение от 0.1 до 0.4
        return armor_type(armor_count, absorption)