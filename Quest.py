class Quest:
    def __init__(self, name, description, reward, condition):
        """
        :param name: Название квеста.
        :param description: Описание квеста.
        :param reward: Награда за выполнение.
        :param condition: Условие выполнения (функция).
        """
        self.name = name
        self.description = description
        self.reward = reward
        self.condition = condition
        self.completed = False

    def check_completion(self, player):
        """Проверяет выполнение квеста."""
        if self.condition(player):
            self.completed = True
            print(f"Квест '{self.name}' выполнен!")
            player.gold += self.reward
            print(f"Вы получили {self.reward} монет в награду.")