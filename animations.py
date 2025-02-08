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
    max_y, max_x = stdscr.getmaxyx()
    for _ in range(3):
        stdscr.clear()
        for i, line in enumerate(player_char):
            if player_pos[0] + i < max_y and player_pos[1] + len(line) < max_x:
                stdscr.addstr(player_pos[0] + i, player_pos[1], line)
        for i, line in enumerate(enemy_char):
            if enemy_pos[0] + i < max_y and enemy_pos[1] + len(line) < max_x:
                stdscr.addstr(enemy_pos[0] + i, enemy_pos[1], line)
        if player_pos[0] + 4 < max_y and player_pos[1] + len(f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}") < max_x:
            stdscr.addstr(player_pos[0] + 4, player_pos[1], f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}")
        if enemy_pos[0] + 4 < max_y and enemy_pos[1] + len(f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}") < max_x:
            stdscr.addstr(enemy_pos[0] + 4, enemy_pos[1], f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}")
        stdscr.refresh()
        curses.napms(500)
        if attacker == player:
            if player_pos[0] + 1 < max_y and player_pos[1] + 4 + len("-->") < max_x:
                stdscr.addstr(player_pos[0] + 1, player_pos[1] + 4, "-->")
        else:
            if enemy_pos[0] + 1 < max_y and enemy_pos[1] - 4 - len("<--") >= 0:
                stdscr.addstr(enemy_pos[0] + 1, enemy_pos[1] - 4, "<--")
        stdscr.refresh()
        curses.napms(500)
    stdscr.clear()
    for i, line in enumerate(player_char):
        if player_pos[0] + i < max_y and player_pos[1] + len(line) < max_x:
            stdscr.addstr(player_pos[0] + i, player_pos[1], line)
    for i, line in enumerate(enemy_char):
        if enemy_pos[0] + i < max_y and enemy_pos[1] + len(line) < max_x:
            stdscr.addstr(enemy_pos[0] + i, enemy_pos[1], line)
    if player_pos[0] + 4 < max_y and player_pos[1] + len(f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}") < max_x:
        stdscr.addstr(player_pos[0] + 4, player_pos[1], f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}")
    if enemy_pos[0] + 4 < max_y and enemy_pos[1] + len(f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}") < max_x:
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
    max_y, max_x = stdscr.getmaxyx()
    for _ in range(3):
        stdscr.clear()
        for i, line in enumerate(player_char):
            if player_pos[0] + i < max_y and player_pos[1] + len(line) < max_x:
                stdscr.addstr(player_pos[0] + i, player_pos[1], line)
        for i, line in enumerate(enemy_char):
            if enemy_pos[0] + i < max_y and enemy_pos[1] + len(line) < max_x:
                stdscr.addstr(enemy_pos[0] + i, enemy_pos[1], line)
        if player_pos[0] + 4 < max_y and player_pos[1] + len(f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}") < max_x:
            stdscr.addstr(player_pos[0] + 4, player_pos[1], f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}")
        if enemy_pos[0] + 4 < max_y and enemy_pos[1] + len(f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}") < max_x:
            stdscr.addstr(enemy_pos[0] + 4, enemy_pos[1], f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}")
        if player_pos[0] + 1 < max_y and player_pos[1] + 4 + len(fireball) < max_x:
            stdscr.addstr(player_pos[0] + 1, player_pos[1] + 4, fireball)
        stdscr.refresh()
        curses.napms(500)
        fireball = "   " if fireball == " * " else " * "
    stdscr.clear()
    for i, line in enumerate(player_char):
        if player_pos[0] + i < max_y and player_pos[1] + len(line) < max_x:
            stdscr.addstr(player_pos[0] + i, player_pos[1], line)
    for i, line in enumerate(enemy_char):
        if enemy_pos[0] + i < max_y and enemy_pos[1] + len(line) < max_x:
            stdscr.addstr(enemy_pos[0] + i, enemy_pos[1], line)
    if player_pos[0] + 4 < max_y and player_pos[1] + len(f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}") < max_x:
        stdscr.addstr(player_pos[0] + 4, player_pos[1], f"HP: {player.hp} MP: {player.manabank} Урон: {player.damage}")
    if enemy_pos[0] + 4 < max_y and enemy_pos[1] + len(f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}") < max_x:
        stdscr.addstr(enemy_pos[0] + 4, enemy_pos[1], f"HP: {target.hp} MP: {target.manabank} Урон: {target.damage}")
    stdscr.refresh()
    curses.napms(500)

def animate_run(stdscr):
    curses.curs_set(0)  # Скрыть курсор
    stdscr.clear()
    runner = [
        " O ",
        "/|\\",
        "/ \\"
    ]
    max_y, max_x = stdscr.getmaxyx()
    for _ in range(3):
        stdscr.clear()
        for i, line in enumerate(runner):
            if 5 + i < max_y and 10 + len(line) < max_x:
                stdscr.addstr(5 + i, 10, line)
        stdscr.refresh()
        curses.napms(500)
        stdscr.clear()
        for i, line in enumerate(runner):
            if 5 + i < max_y and 20 + len(line) < max_x:
                stdscr.addstr(5 + i, 20, line)
        stdscr.refresh()
        curses.napms(500)
    stdscr.clear()
    for i, line in enumerate(runner):
        if 5 + i < max_y and 30 + len(line) < max_x:
            stdscr.addstr(5 + i, 30, line)
    stdscr.refresh()
    curses.napms(500)