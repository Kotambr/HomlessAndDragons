import curses

def animate_attack(stdscr, attacker, target, player, enemy):
    curses.curs_set(0)  # Скрыть курсор
    stdscr.clear()
    player_pos = (5, 10)
    enemy_pos = (5, 50)
    player_char = [
        " O ",
        "/|\\",
        "/ \\"
    ]
    enemy_char = [
        " O ",
        "/|\\",
        "/ \\"
    ]
    for _ in range(3):
        stdscr.clear()
        for i, line in enumerate(player_char):
            stdscr.addstr(player_pos[0] + i, player_pos[1], line)
        for i, line in enumerate(enemy_char):
            stdscr.addstr(enemy_pos[0] + i, enemy_pos[1], line)
        stdscr.addstr(player_pos[0] + 4, player_pos[1], f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}")
        stdscr.addstr(enemy_pos[0] + 4, enemy_pos[1], f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}")
        stdscr.refresh()
        curses.napms(500)
        if attacker == player:
            stdscr.addstr(player_pos[0] + 1, player_pos[1] + 4, "-->")
        else:
            stdscr.addstr(enemy_pos[0] + 1, enemy_pos[1] - 4, "<--")
        stdscr.refresh()
        curses.napms(500)
    stdscr.clear()
    for i, line in enumerate(player_char):
        stdscr.addstr(player_pos[0] + i, player_pos[1], line)
    for i, line in enumerate(enemy_char):
        stdscr.addstr(enemy_pos[0] + i, enemy_pos[1], line)
    stdscr.addstr(player_pos[0] + 4, player_pos[1], f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}")
    stdscr.addstr(enemy_pos[0] + 4, enemy_pos[1], f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}")
    stdscr.refresh()
    curses.napms(500)

def animate_magic(stdscr, player, target):
    curses.curs_set(0)  # Скрыть курсор
    stdscr.clear()
    player_pos = (5, 10)
    enemy_pos = (5, 50)
    player_char = [
        " O ",
        "/|\\",
        "/ \\"
    ]
    enemy_char = [
        " O ",
        "/|\\",
        "/ \\"
    ]
    fireball = " * "
    for _ in range(3):
        stdscr.clear()
        for i, line in enumerate(player_char):
            stdscr.addstr(player_pos[0] + i, player_pos[1], line)
        for i, line in enumerate(enemy_char):
            stdscr.addstr(enemy_pos[0] + i, enemy_pos[1], line)
        stdscr.addstr(player_pos[0] + 4, player_pos[1], f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}")
        stdscr.addstr(enemy_pos[0] + 4, enemy_pos[1], f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}")
        stdscr.addstr(player_pos[0] + 1, player_pos[1] + 4, fireball)
        stdscr.refresh()
        curses.napms(500)
        fireball = "   " if fireball == " * " else " * "
    stdscr.clear()
    for i, line in enumerate(player_char):
        stdscr.addstr(player_pos[0] + i, player_pos[1], line)
    for i, line in enumerate(enemy_char):
        stdscr.addstr(enemy_pos[0] + i, enemy_pos[1], line)
    stdscr.addstr(player_pos[0] + 4, player_pos[1], f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}")
    stdscr.addstr(enemy_pos[0] + 4, enemy_pos[1], f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}")
    stdscr.refresh()
    curses.napms(500)

# def animate_inventory(stdscr):
#     curses.curs_set(0)  # Скрыть курсор
#     stdscr.clear()
#     inventory = [
#         "Инвентарь:",
#         "1. Зелье здоровья",
#         "2. Зелье маны",
#         "3. Меч",
#         "4. Щит"
#     ]
#     for i, line in enumerate(inventory):
#         stdscr.addstr(i, 0, line)
#     stdscr.refresh()
#     curses.napms(2000)

def animate_run(stdscr):
    curses.curs_set(0)  # Скрыть курсор
    stdscr.clear()
    runner = [
        " O ",
        "/|\\",
        "/ \\"
    ]
    for _ in range(3):
        stdscr.clear()
        for i, line in enumerate(runner):
            stdscr.addstr(5 + i, 10, line)
        stdscr.refresh()
        curses.napms(500)
        stdscr.clear()
        for i, line in enumerate(runner):
            stdscr.addstr(5 + i, 20, line)
        stdscr.refresh()
        curses.napms(500)
    stdscr.clear()
    for i, line in enumerate(runner):
        stdscr.addstr(5 + i, 30, line)
    stdscr.refresh()
    curses.napms(500)