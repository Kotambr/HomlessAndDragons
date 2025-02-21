import random as rn

class Weapon:
    def __init__(self, name, damage: int, durability: int, price: int):
        self.name = name
        self.damage = damage
        self.durability = durability
        self.max_durability = self.durability
        self.price = price
        self.upgrade_lvl = 1

    def __str__(self):
        return f"{self.name} (Прочность: {self.durability}/{self.max_durability}, Урон: {self.damage})"

    def is_broken(self):
        return self.durability <= 0

    def reduce_durability(self):
        """Снижает прочность оружия на 1 при использовании."""
        if self.durability > 0:
            self.durability -= 1
            print(f"{self.name} теряет прочность, осталось {self.durability}.")
        if self.is_broken():
            print(f"{self.name} сломалось!")

    def use(self, target):
        """Использование оружия против цели."""
        self.reduce_durability()
        return f"Атака {self.name} по {target.name}, наносит {self.damage} урона."

class Sword(Weapon):
    def __init__(self, damage: int, durability: int):
        super().__init__("Меч", damage, durability)

class Dagger(Weapon):
    def __init__(self, damage: int, durability: int):
        super().__init__("Кинжал", damage, durability)

class MagicalStuff(Weapon):
    def __init__(self, damage: int, durability: int, effect=None):
        super().__init__("Магический предмет", damage, durability)
        self.effect = effect or self.random_magic_effect()

    def random_magic_effect(self):
        """Случайно выбирает эффект для магического предмета."""
        effects = [
            ("Оглушение", lambda target: f"{target.name} оглушен!"),
            ("Отравление", lambda target: f"{target.name} отравлен и теряет 5 здоровья."),
            ("Замедление", lambda target: f"{target.name} замедлен на следующий ход."),
            ("Восстановление маны", lambda caster: f"{caster.name} восстанавливает 10 маны.")
        ]
        return rn.choice(effects)

    def use(self, target, caster=None):
        """Применяет магическое оружие с уникальным эффектом на цель."""
        self.reduce_durability()
        effect_name, effect_function = self.effect
        if self.is_broken():
            return f"{self.name} не может быть использован, так как сломан."
        result = f"Атака {self.name} по {target.name}, наносит {self.damage} урона."
        result += f" Эффект: {effect_function(target if target else caster)}."
        return result

class Projectile(Weapon):
    def __init__(self, damage: int, durability: int):
        super().__init__("Метательное оружие", damage, durability)

class WeaponFactory:
    @staticmethod
    def create_random_weapon():
        weapon_types = [Sword, Dagger, MagicalStuff, Projectile]
        weapon_class = rn.choice(weapon_types)
        
        damage = rn.randint(5, 30)
        durability = rn.randint(5, 15)
        
        if weapon_class == MagicalStuff:
            return weapon_class(damage, durability) 
        else:
            return weapon_class(damage, durability)
