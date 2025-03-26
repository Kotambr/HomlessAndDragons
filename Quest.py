class Quest:
    def __init__(self, quest_id, name, description, objectives, rewards, giver=None, is_main=False):
        """
        :param quest_id: уникальный идентификатор квеста
        :param name: название квеста
        :param description: описание квеста
        :param objectives: список этапов квеста (dict: этап -> условие выполнения)
        :param rewards: награды за квест (список предметов, очков опыта и т.д.)
        :param giver: NPC или объект, от которого получен квест
        :param is_main: является ли квест главным
        """
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.objectives = objectives  # {"Этап 1": False, "Этап 2": False}
        self.rewards = rewards
        self.giver = giver
        self.is_main = is_main
        self.completed = False

    def update_objective(self, objective):
        """Обновляет статус выполнения этапа квеста"""
        if objective in self.objectives:
            self.objectives[objective] = True
            print(f"Этап '{objective}' выполнен!")
            self.check_completion()

    def check_completion(self):
        """Проверяет, завершен ли квест"""
        if all(self.objectives.values()):
            self.completed = True
            print(f"Квест '{self.name}' завершен!")
            return True
        return False

    def get_status(self):
        """Возвращает текущее состояние квеста"""
        status = [f"{obj}: {'✔' if done else '❌'}" for obj, done in self.objectives.items()]
        return f"{self.name}:\n" + "\n".join(status)
    
    def triger(self, event_id):
        """Вызывает событие и обновляет журнал заданий"""
        print(f"Событие '{event_id}' произошло!")
        self.quest_log.update_quest(event_id)
    

class QuestLog:
    def __init__(self):
        self.active_quests = {}
        self.completed_quests = []

    def add_quest(self, quest):
        """Добавляет квест в журнал"""
        if quest.quest_id not in self.active_quests:
            self.active_quests[quest.quest_id] = quest
            print(f"Квест '{quest.name}' добавлен в журнал!")

    def update_quest(self, event_id):
        """Обновляет квест при выполнении его этапов на основе события"""
        for quest in self.active_quests.values():
            for objective, completed in quest.objectives.items():
                if not completed and objective == event_id:
                    quest.update_objective(objective)
                    if quest.completed:
                        self.completed_quests.append(quest)
                        del self.active_quests[quest.quest_id]
                    return  # Обновляем только один квест за раз

    def show_log(self):
        """Отображает текущий журнал квестов"""
        print("\nАктивные квесты:")
        for quest in self.active_quests.values():
            print(quest.get_status())
        
        print("\nЗавершенные квесты:")
        for quest in self.completed_quests:
            print(f"{quest.name} - Завершен")



# # Создадим квест


# # Создадим журнал и добавим квест
# quest_log = QuestLog()
# quest_log.add_quest(main_quest)

# # Обновляем квест по мере выполнения
# quest_log.update_quest("Добраться до деревни")
# quest_log.update_quest("Поговорить со старейшиной")

# # Вывод журнала после завершения
# quest_log.show_log()
