from links import rn

class Weapon:
    def __init__(self, type_weapon, damage: int, weapon_count: int):
        self.type_weapon = type_weapon
        self.damage = damage
        self.weapon_count = weapon_count

    def is_broken(self):
        return self.weapon_count <= 0

    def reduce_durability(self):
        """Снижает прочность оружия на 1 при использовании."""
        if self.weapon_count > 0:
            self.weapon_count -= 1
            print(f"{self.type_weapon} теряет прочность, осталось {self.weapon_count}.")
        if self.is_broken():
            print(f"{self.type_weapon} сломалось!")

    def use(self, target):
        """Использование оружия против цели."""
        self.reduce_durability()
        return f"Атака {self.type_weapon} по {target.name}, наносит {self.damage} урона."

class Sword(Weapon):
    def __init__(self, damage: int, weapon_count: int):
        super().__init__("Меч", damage, weapon_count)

class Dagger(Weapon):
    def __init__(self, damage: int, weapon_count: int):
        super().__init__("Кинжал", damage, weapon_count)

class MagicalStuff(Weapon):
    def __init__(self, damage: int, weapon_count: int, effect=None):
        super().__init__("Магический предмет", damage, weapon_count)
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
            return f"{self.type_weapon} не может быть использован, так как сломан."
        result = f"Атака {self.type_weapon} по {target.name}, наносит {self.damage} урона."
        result += f" Эффект: {effect_function(target if target else caster)}."
        return result

class Projectile(Weapon):
    def __init__(self, damage: int, weapon_count: int):
        super().__init__("Метательное оружие", damage, weapon_count)

class WeaponFactory:
    @staticmethod
    def create_random_weapon():
        weapon_types = [Sword, Dagger, MagicalStuff, Projectile]
        weapon_class = rn.choice(weapon_types)
        
        damage = rn.randint(5, 30)
        weapon_count = rn.randint(5, 15)
        
        if weapon_class == MagicalStuff:
            return weapon_class(damage, weapon_count) 
        else:
            return weapon_class(damage, weapon_count)
