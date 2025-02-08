import random as rn


class Spell:
    def __init__(self, name: str, mana_cost: int, effect):
        self.name = name
        self.mana_cost = mana_cost
        self.effect = effect

    def cast(self, caster, target):
        if caster.manabank < self.mana_cost:
            print(f"{caster.name} недостаточно маны для использования {self.name}.")
            return False
        caster.manabank -= self.mana_cost
        print(f"{caster.name} использует {self.name}. {self.effect(caster, target)}")
        return True

class AttackSpell(Spell):
    def __init__(self, name, mana_cost, damage):
        super().__init__(name, mana_cost, effect=self.attack_effect)
        self.damage = damage

    def attack_effect(self, caster, target):
        if target:
            target.hp -= self.damage
            return f"{target.name} получает {self.damage} урона от {self.name}!"
        return f"{self.name} не имеет цели."

class HealingSpell(Spell):
    def __init__(self, name, mana_cost, heal_amount):
        super().__init__(name, mana_cost, effect=self.healing_effect)
        self.heal_amount = heal_amount

    def healing_effect(self, caster, target=None):
        caster.hp = min(caster.max_hp, caster.hp + self.heal_amount)
        return f"{caster.name} восстанавливает {self.heal_amount} здоровья от {self.name}."

class BuffSpell(Spell):
    def __init__(self, name, mana_cost, buff_stat, buff_amount, duration):
        super().__init__(name, mana_cost, effect=self.buff_effect)
        self.buff_stat = buff_stat
        self.buff_amount = buff_amount
        self.duration = duration

    def buff_effect(self, caster, target=None):
        if self.buff_stat == "damage":
            caster.damage += self.buff_amount
        return f"{caster.name} получает бафф {self.buff_stat} на {self.buff_amount} в течение {self.duration} ходов."


class SpellFactory:
    @staticmethod
    def create_random_spell():
        spell_type = rn.choice([AttackSpell, HealingSpell, BuffSpell])

        prefixes = ["Огненный", "Магический", "Темный", "Земной", "Ледяной"]
        suffixes = ["Шар", "Щит", "Стрела", "Клинок", "Касание"]
        name = f"{rn.choice(prefixes)} {rn.choice(suffixes)}"

        mana_cost = rn.randint(5, 25)

        if spell_type == AttackSpell:
            damage = rn.randint(10, 50)
            return AttackSpell(name=name, mana_cost=mana_cost, damage=damage)

        elif spell_type == HealingSpell:
            heal_amount = rn.randint(15, 40)
            return HealingSpell(name=name, mana_cost=mana_cost, heal_amount=heal_amount)

        elif spell_type == BuffSpell:
            buff_stat = "damage"
            buff_amount = rn.randint(5, 15)
            duration = rn.randint(2, 5)
            return BuffSpell(name=name, mana_cost=mana_cost, buff_stat=buff_stat, buff_amount=buff_amount, duration=duration)

