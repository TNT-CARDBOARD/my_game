import os
import re
import sys
import random

CELL_WIDTH = 10
CELL_HEIGHT = 5

FIELD = r"""
..........................................#################..........................................
..................................########........#........########..................................
..............................####................#................####..............................
..........................####....................#....................####..........................
......................####........................#........................####......................
....................##....#.......................#.......................#....##....................
..................#........#......................#......................#........#..................
................#...........#.....................#.....................#...........#................
..............#..............#...........@1.......#.........@2.........#..............#..............
............##................#................#######................#................##............
...........#...................##....##########...#...##########.....#...................#...........
..........#.....................##.##.............#.............##..#.....................#..........
........#.......................###...............#................##.......................#........
.......#............@3........#....#..............#...............#...#.........@4...........#.......
......###...................#.......#.............#.............##......#...................###......
.....#....##..............#..........#............#............##.........#..............##....#.....
....#.........##........#.............#...........#...........##............#.........##........#....
....#............##....#...............#..........#..........##..............#.....##...........#....
...#................###.................#......@6.#....@7...#.................###................#...
..#..................#.##................#...###########...#................##.#..................#..
..#.................#.....+#......@5......###...........###........@8....##.....#.................#..
.#.................#..........##........##.................##.........##.........#.................#.
.#.................#.............##...##.....................##....#.............#.................#.
.#................#.................##.........................##.................#................#.
#.................#.................#...........................#.................#.................#
#........@9.......#.......@A........#...........................#.........@B......#........@C.......#
#................#.................#.............................#.................#................#
####################################..............@0.............####################################
#................#.................#.............................#.................#................#
#.................#.................#...........................#.................#.................#
#.................#.................#...........................#.................#.................#
.#................#.................##.........................##.................#................#.
.#.................#..............#...##.....................##...##.............#.................#.
.#.................#......@E..##........##.................##........##....@J....#.................#.
..#.................#......##.............###...........###..............#......#.................#..
..#..................#..##...............#...###########...#................##.#..................#..
...#.......@D........##.................#.........#.........#.................###.........@K.....#...
....#............##+...#...............#..........#..........#...............#....##.............#...
....#.........##........#.............#...........#...........#.............#........##.........#....
.....#.....##............-#.....@F...#............#............#......@I..##............##.....#.....
......#.##.................##.......#.............#.............#.......##..................###......
.......#.....................##....#..............#..............##...##.....................#.......
........#.......................###.........@G....#.......@H......###.......................#........
.........##......................#.##.............#.............##..#.....................##.........
...........#.........@L.........#......########...#..#########.......#..........@O.......#...........
............##................##...............######.................#................##............
..............#..............##...................#....................#..............#..............
................#...........#-....................#.....................#...........#................
..................#........#......................#......................#........#..................
....................##....#.......................#.......................#....##....................
.......................#.#........................#........................#-#.......................
.........................###.............@M.......#..........@N..........###.........................
.............................####.................#.................####.............................
.................................#######..........#..........#######.................................
........................................#####################........................................
"""

FIELD_LINES_STR = [line for line in FIELD.splitlines() if line.strip() != ""]
max_field_w = max(len(line) for line in FIELD_LINES_STR)
canvas_original = []
for line_s in FIELD_LINES_STR:
    canvas_original.append(list(line_s.ljust(max_field_w, '.')))

allowed_cells = {}
for r_idx, line_s in enumerate(FIELD_LINES_STR):
    for m in re.finditer(r'@([0-9A-Z])', line_s):
        label = m.group(1)
        c_idx = m.start()
        allowed_cells[label] = (r_idx, c_idx)

for label, (r, c_of_at) in allowed_cells.items():
    if 0 <= r < len(canvas_original) and 0 <= c_of_at < len(canvas_original[r]):
        canvas_original[r][c_of_at] = '.'
    if 0 <= r < len(canvas_original) and 0 <= c_of_at + 1 < len(canvas_original[r]):
        canvas_original[r][c_of_at + 1] = '.'

CANVAS_HEIGHT = len(canvas_original)
CANVAS_WIDTH = len(canvas_original[0]) if canvas_original else 0
board = {label: None for label in allowed_cells}
neighbors_map = {
    '0': ['A', 'B', 'F', 'G', 'H', '5', '6', '7', '8', 'J', 'I', 'E'], '1': ['2', '5', '6', '3', '7'], '2': ['1', '6', '7', '8', '4'], '3': ['9', 'A', '5', '6', '1'], '4': ['2', '7', '8', 'B', 'C'], '5': ['1', '6', 'A', '3', '9', '0'], '6': ['1', '2', '5', '3', '7', '0'], '7': ['2', '1', '6', '8', '4', '0'], '8': ['7', '2', '4', 'C', 'B', '0'], '9': ['D', 'E', 'A', '5', '3'], 'A': ['3', '9', 'D', 'E', '5', '0'], 'B': ['8', '4', 'C', 'K', 'J', '0'], 'C': ['4', '8', 'B', 'K', 'J'], 'D': ['9', 'A', 'E', 'F', 'L'], 'E': ['A', '9', 'D', 'L', 'F', '0'], 'F': ['E', 'D', 'L', 'M', 'G', '0'], 'G': ['F', 'L', 'M', 'N', 'H', '0'], 'H': ['G', 'M', 'N', 'O', 'I', '0'], 'I': ['H', 'N', 'O', 'K', 'J', '0'], 'J': ['I', 'O', '0', 'K', 'C', 'B'], 'K': ['O', 'I', 'J', 'B', 'C'], 'L': ['D', 'E', 'F', 'G', 'M'], 'M': ['L', 'F', 'G', 'H', 'N'], 'N': ['M', 'G', 'H', 'I', 'O'], 'O': ['N', 'H', 'I', 'J', 'K']
}

def get_blue_soldier_art(): return ["..//\\.♤.", ".//==╘║.", "..\\//.║."]
def get_blue_archer_art(): return ["...O..⎫", "..╘┼╘─┆→", "../.\\.⎭"]
def get_blue_knight_art(): return ["...O...", "../|╘─┄┄", "../.\\..."]
def get_blue_mage_art(): return ["...O.◆..", "../|╘┃..", "..⎧║⎫┃.."]

def get_red_soldier_art(): return ["..//\\.╋.", ".//==╘║.", "..\\//.║."] 
def get_red_archer_art(): return ["...●..⎫", "..╘┼╘─┆»", "../.\\.⎭"]  
def get_red_knight_art(): return ["...●...", "../|╘─┄┄", "../.\\..."] 
def get_red_mage_art(): return ["...●.◊..", "../|╘┃..", "..⎧║⎫┃.."]

token_arts = {
    'B': {
        "Soldier": get_blue_soldier_art(), "Archer": get_blue_archer_art(),
        "Knight": get_blue_knight_art(), "Mage": get_blue_mage_art()
    },
    'R': {
        "Soldier": get_red_soldier_art(), "Archer": get_red_archer_art(),
        "Knight": get_red_knight_art(), "Mage": get_red_mage_art()
    }
}

class Token:
    def __init__(self, side, tclass, hp, attack, defense):
        self.side = side
        self.tclass = tclass
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.frozen = 0
        self.cooldown = 0
        if tclass == "Archer": self.special_used = False
        else: self.special_used = None
        if tclass == "Knight": self.special_attack_cooldown = 0
        else: self.special_attack_cooldown = None
        if tclass == "Soldier":
            self.knockback_cooldown = 0
            self.shield_repair_cooldown = 0
            self.max_defense = defense
        else:
            self.knockback_cooldown = None
            self.shield_repair_cooldown = None
            self.max_defense = None
            
    def __str__(self):
        return f"{self.tclass} ({self.side})"
    
    def get_stats_str(self):
        base_stats = f"H:{self.hp} A:{self.attack} D:{self.defense}"
        status_indicators = []
        if self.frozen > 0: status_indicators.append("[F]")
        if self.tclass == "Mage" and self.cooldown > 0: status_indicators.append(f"HC:{self.cooldown}")
        elif self.tclass == "Knight" and self.special_attack_cooldown > 0: status_indicators.append(f"SC:{self.special_attack_cooldown}")
        elif self.tclass == "Soldier":
            if self.knockback_cooldown > 0: status_indicators.append(f"KC:{self.knockback_cooldown}")
            if self.shield_repair_cooldown > 0: status_indicators.append(f"RC:{self.shield_repair_cooldown}")
        elif self.tclass == "Archer" and self.special_used: status_indicators.append("[SU]")
        return f"{base_stats} {' '.join(status_indicators)}".strip()

def token_block(token):
    block = []
    art = token_arts[token.side][token.tclass]
    
    for i in range(3):
        art_line_content = art[i] if i < len(art) else ""
        block.append(art_line_content.center(CELL_WIDTH, ' '))

    block.append(" " * CELL_WIDTH) 

    stats_display_str = token.get_stats_str()
    if len(stats_display_str) < CELL_WIDTH:
        block.append(stats_display_str.center(CELL_WIDTH, ' '))
    else:
        block.append(stats_display_str) 

    return block

def overlay_token(canvas, cell_label_key, block_lines):
    r_anchor, c_anchor_of_at = allowed_cells[cell_label_key] 
    top = r_anchor - (CELL_HEIGHT - 1) 
    left_offset_for_block_start = c_anchor_of_at - (CELL_WIDTH // 2)
    
    for i, line_str_from_block in enumerate(block_lines):
        current_line_content = line_str_from_block.strip() 
        left_for_this_line = left_offset_for_block_start
        if i == 4: 
            actual_content_len = len(line_str_from_block.strip()) 
            left_for_this_line = c_anchor_of_at - (actual_content_len // 2)

        for j, char_from_block in enumerate(line_str_from_block): 
            if char_from_block != ' ': 
                y, x = top + i, left_for_this_line + j
                if 0 <= y < CANVAS_HEIGHT and 0 <= x < CANVAS_WIDTH:
                    canvas[y][x] = char_from_block

def print_board():
    canvas = [row[:] for row in canvas_original] 
    LABEL_CONTENT_WIDTH = 3 

    for cell_label_key, _ in allowed_cells.items(): 
        token_on_cell = board.get(cell_label_key)
        r_anchor, c_anchor_of_at = allowed_cells[cell_label_key] 

        if token_on_cell is None:
            display_label_str = cell_label_key.center(LABEL_CONTENT_WIDTH)
            y_for_label = r_anchor
            x_start_for_label = c_anchor_of_at - (len(display_label_str) // 2)

            for k, char_label in enumerate(display_label_str):
                if char_label != ' ': 
                    final_x = x_start_for_label + k
                    if 0 <= y_for_label < CANVAS_HEIGHT and 0 <= final_x < CANVAS_WIDTH:
                        canvas[y_for_label][final_x] = char_label
        else:
            block_content_for_token = token_block(token_on_cell) 
            overlay_token(canvas, cell_label_key, block_content_for_token)
            
    if os.name == 'nt': os.system("cls")
    else: os.system("clear")
    for line_list in canvas: print("".join(line_list))

def choose_option(prompt, options_list_of_tuples): 
    if not options_list_of_tuples:
        print("Нет доступных опций.")
        return None

    print("\n" + prompt)
    for i, (display_str, _) in enumerate(options_list_of_tuples, start=1):
        print(f"{i}: {display_str}")
    print("0: Завершить игру (или отменить текущий выбор, если применимо)")
    
    while True:
        inp = input("Ваш выбор: ")
        if inp.strip().lower() in ['q', 'quit']:
            print("Завершение игры.")
            sys.exit(0)
        if inp.strip() == '0': 
            print("Завершение игры по выбору '0'.") 
            sys.exit(0)
        try:
            choice_num = int(inp)
            if 1 <= choice_num <= len(options_list_of_tuples):
                return options_list_of_tuples[choice_num - 1][1] 
            else:
                print(f"Неверный номер. Введите число от 1 до {len(options_list_of_tuples)} или 0 для выхода.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите номер опции.")

def extended_targets(source_label):
    direct_neighbors = set(neighbors_map.get(source_label, []))
    all_extended = set(direct_neighbors)
    for nbr in direct_neighbors:
        all_extended.update(neighbors_map.get(nbr, []))
    all_extended.discard(source_label)
    return list(all_extended)

def select_targets_in_radius(prompt, source_cell, radius_func, current_player_side, max_targets=1, target_must_be_enemy=True, can_cancel=True):
    potential_target_cells = radius_func(source_cell)
    valid_targets_info = [] 

    for t_cell in potential_target_cells:
        token_on_cell = board.get(t_cell)
        if token_on_cell:
            if target_must_be_enemy and token_on_cell.side == current_player_side:
                continue 
            if not target_must_be_enemy and token_on_cell.side != current_player_side: 
                if source_cell == t_cell: 
                    pass
                else: 
                    continue 
            
            valid_targets_info.append( (f"{token_on_cell} на {t_cell} ({token_on_cell.get_stats_str()})", t_cell) )
        elif not target_must_be_enemy and not token_on_cell : 
            pass 

    if not valid_targets_info:
        if target_must_be_enemy : print("Нет доступных вражеских целей в указанном радиусе.")
        return []

    selected_target_cells = []
    
    for i in range(max_targets):
        if not valid_targets_info: break 

        current_prompt = prompt
        current_options = list(valid_targets_info) 

        if selected_target_cells and i < max_targets:
             current_options.append( ("Завершить выбор целей", "done_selecting") )
        
        if can_cancel and i == 0: 
            current_options.append( ("Отменить действие", "cancel_action") )

        chosen_target_cell_or_command = choose_option(f"{current_prompt} (Цель {i+1}/{max_targets}):", current_options)

        if chosen_target_cell_or_command == "done_selecting": break
        if chosen_target_cell_or_command == "cancel_action": return [] 
        if chosen_target_cell_or_command is None: 
            return [] 

        if chosen_target_cell_or_command:
            selected_target_cells.append(chosen_target_cell_or_command)
            valid_targets_info = [(disp, cell) for disp, cell in valid_targets_info if cell != chosen_target_cell_or_command]
        else: 
            if not can_cancel: 
                print("Выбор цели обязателен.")
                return [] 
            break 
            
    return selected_target_cells

def apply_damage_to_target(target_token, damage_amount, attacker_name="Атакующий"):
    if not target_token: return "target_gone" 

    print(f"{attacker_name} пытается нанести {damage_amount} урона по {target_token} (H:{target_token.hp} D:{target_token.defense}).")
    
    if target_token.defense > 0:
        if damage_amount <= target_token.defense:
            target_token.defense -= damage_amount
            print(f"Щит {target_token} поглотил {damage_amount} урона. Осталось щита: {target_token.defense}.")
        else: 
            print(f"Щит {target_token} ({target_token.defense}) не выдержал {damage_amount} урона и был уничтожен (обнулен).")
            target_token.defense = 0
            print(f"ХП {target_token} не изменилось от этой атаки по щиту.")
    else: 
        target_token.hp -= damage_amount
        print(f"{target_token} получает {damage_amount} урона напрямую в HP. Осталось HP: {target_token.hp}.")

    if target_token.hp <= 0:
        print(f"{target_token} побеждён!")
        return "dead"
    return "alive"

def combat(attacker, defender, attacker_cell, defender_cell, allow_counterattack=True):
    if not attacker:
        return {"attacker_status": "dead", "defender_status": "alive" if defender else "dead"}
    if not defender:
        return {"attacker_status": "alive", "defender_status": "dead"}

    results = {"attacker_status": "alive", "defender_status": "alive"}

    print(f"\n{attacker} ({attacker.get_stats_str()}) атакует {defender} ({defender.get_stats_str()})!")
    defender_status_after_attack = apply_damage_to_target(defender, attacker.attack, str(attacker))
    
    if defender_status_after_attack == "dead":
        board[defender_cell] = None
        results["defender_status"] = "dead"
        return results 
    elif defender_status_after_attack == "target_gone": 
        results["defender_status"] = "dead" 
        return results

    if allow_counterattack:
        if board.get(defender_cell) == defender and defender.hp > 0 :
            print(f"\n{defender} ({defender.get_stats_str()}) контратакует {attacker} ({attacker.get_stats_str()})!")
            if board.get(attacker_cell) == attacker and attacker.hp > 0:
                attacker_status_after_counter = apply_damage_to_target(attacker, defender.attack, str(defender))
                if attacker_status_after_counter == "dead":
                    board[attacker_cell] = None
                    results["attacker_status"] = "dead"
                elif attacker_status_after_counter == "target_gone": 
                    results["attacker_status"] = "dead"
            else:
                print(f"{attacker} уже не на клетке {attacker_cell} или побежден, контратака невозможна.")
        else:
            print(f"{defender} не может контратаковать (побежден или не на клетке).")
            
    return results

def mage_attack_menu(mage_token, mage_cell_label, current_turn_side):
    if not mage_token or not board.get(mage_cell_label) == mage_token or mage_token.hp <= 0:
        return False # Маг не может действовать

    print(f"\nДействия Мага ({mage_token.get_stats_str()}) на {mage_cell_label}:")
    
    actions_taken_count = 0
    max_actions_per_turn = 2
    
    # Состояния для отслеживания использованных способностей в этом ходу
    heal_used_this_turn = False
    
    while actions_taken_count < max_actions_per_turn:
        if not (board.get(mage_cell_label) == mage_token and mage_token.hp > 0): # Проверка, жив ли маг
            print("Маг больше не может действовать (побежден или исчез).")
            break

        action_number_str = "Первое" if actions_taken_count == 0 else "Второе"
        print(f"\n--- {action_number_str} действие мага ({actions_taken_count+1}/{max_actions_per_turn}) ---")

        current_action_options = []
        # 1. Огненный шар (атака 1 цели)
        current_action_options.append(("Огненный шар (1 враг в радиусе)", "fireball_single"))
        # 2. Заморозка
        current_action_options.append(("Заморозка (1 враг в радиусе)", "freeze"))
        # 3. Лечение
        if mage_token.cooldown == 0 and not heal_used_this_turn:
            current_action_options.append(("Лечение (1 союзник или себя в радиусе)", "heal"))
        elif heal_used_this_turn:
             current_action_options.append(("(Лечение уже использовано в этом ходу)", None))
        else: # Кулдаун активен
            current_action_options.append((f"Лечение (недоступно, КД: {mage_token.cooldown})", None))
        
        if actions_taken_count > 0 : # Если хотя бы одно действие уже сделано
             current_action_options.append(("Завершить действия мага", "finish_mage_turn"))
        current_action_options.append(("Отменить все действия мага и выбрать другой токен/действие", "cancel_all_mage_actions"))


        mage_choice = choose_option(f"Выберите {action_number_str.lower()} действие:", current_action_options)

        action_performed_in_this_step = False

        if not mage_choice or mage_choice == "cancel_all_mage_actions":
            print("Все действия мага отменены.")
            return False # Игрок отменил полностью, возвращаемся к выбору токена
        
        if mage_choice == "finish_mage_turn":
            print("Маг завершает свои действия.")
            break # Выход из цикла while actions_taken_count < max_actions_per_turn

        elif mage_choice == "fireball_single":
            print("Маг готовит Огненный шар (1 цель)...")
            targets = select_targets_in_radius("Выберите цель для Огненного шара", mage_cell_label, extended_targets, current_turn_side, max_targets=1, target_must_be_enemy=True)
            if targets:
                target_cell = targets[0]
                defender = board.get(target_cell)
                if defender:
                    print(f"Огненный шар летит в {defender} на {target_cell}.")
                    status = apply_damage_to_target(defender, mage_token.attack, f"{mage_token} (Огненный шар)")
                    if status == "dead": board[target_cell] = None
                    action_performed_in_this_step = True
                else: print(f"Цель на {target_cell} для Огненного шара больше не существует.")
            else: print("Огненный шар отменен, цель не выбрана.")
        
        elif mage_choice == "freeze":
            print("Маг готовит Заморозку...")
            targets = select_targets_in_radius("Выберите цель для Заморозки", mage_cell_label, extended_targets, current_turn_side, max_targets=1, target_must_be_enemy=True)
            if targets:
                target_cell = targets[0]
                defender = board.get(target_cell)
                if defender:
                    defender.frozen = 2 
                    print(f"{defender} на {target_cell} заморожен!")
                    action_performed_in_this_step = True
                else: print(f"Цель на {target_cell} для заморозки больше не существует.")
            else: print("Заморозка отменена, цель не выбрана.")

        elif mage_choice == "heal":
            if mage_token.cooldown == 0 and not heal_used_this_turn:
                print("Маг готовит Лечение...")
                heal_candidate_options = []
                cells_for_heal_check = list(set(extended_targets(mage_cell_label) + [mage_cell_label]))
                for cell_key in cells_for_heal_check:
                    token_on_cell = board.get(cell_key)
                    if token_on_cell and token_on_cell.side == current_turn_side and token_on_cell.hp < token_on_cell.max_hp:
                        heal_candidate_options.append(
                            (f"Вылечить {token_on_cell} на {cell_key} ({token_on_cell.get_stats_str()})", cell_key)
                        )
                if not heal_candidate_options:
                    print("Нет раненых союзников в радиусе (или маг здоров).")
                else:
                    heal_candidate_options.append(("Отменить лечение", "cancel_heal_action"))
                    chosen_ally_cell_to_heal = choose_option("Выберите цель для Лечения:", heal_candidate_options)
                    if chosen_ally_cell_to_heal and chosen_ally_cell_to_heal != "cancel_heal_action":
                        token_to_heal = board.get(chosen_ally_cell_to_heal)
                        if token_to_heal:
                            heal_amount = 2
                            token_to_heal.hp = min(token_to_heal.hp + heal_amount, token_to_heal.max_hp)
                            print(f"Маг лечит {token_to_heal} на {chosen_ally_cell_to_heal} на {heal_amount} HP. (Новое HP: {token_to_heal.hp})")
                            mage_token.cooldown = 5 
                            heal_used_this_turn = True
                            action_performed_in_this_step = True
                        else: print(f"Цель для лечения на {chosen_ally_cell_to_heal} исчезла.")
                    else: print("Лечение отменено.")
            else:
                print("Лечение недоступно или уже использовано в этом ходу.")
        
        if action_performed_in_this_step:
            actions_taken_count += 1
        else:
            # Если действие не было выполнено (например, отмена выбора цели),
            # не увеличиваем счетчик действий, даем попробовать еще раз для этого "заряда"
            print("Действие не было завершено. Попробуйте еще раз или отмените.")
            # Можно добавить опцию "Пропустить это малое действие и перейти к следующему/завершить"
            # Но пока для простоты, если отменил выбор цели, то этот "заряд" не потрачен.

    # Возвращаем True, если было совершено хотя бы одно малое действие,
    # чтобы main() знала, что ход игрока должен быть завершен.
    return actions_taken_count > 0

def archer_area_attack_action(archer_token, archer_cell_label, current_turn_side):
    if not archer_token: return False
    print("\nДействия Лучника:")
    action_options = []
    if not archer_token.special_used:
        action_options.append( ("Зональная атака (1 раз за игру, урон по всем соседям цели)", "special_area_attack") )
    action_options.append( ("Обычная атака (1 враг в радиусе)", "normal_ranged_attack") )
    action_options.append(("Отмена", "cancel"))

    archer_choice = choose_option("Выберите тип атаки:", action_options)

    if not archer_choice or archer_choice == "cancel" or archer_choice is None:
        print("Действие лучника отменено.")
        return False

    if archer_choice == "special_area_attack" and not archer_token.special_used:
        print("Лучник готовит Зональную атаку...")
        primary_targets = select_targets_in_radius(
            "Выберите основную вражескую цель для зональной атаки",
            archer_cell_label, extended_targets, current_turn_side,
            max_targets=1, target_must_be_enemy=True
        )
        if not primary_targets:
            print("Зональная атака отменена, основная цель не выбрана.")
            return False 
        
        primary_target_cell = primary_targets[0]
        primary_defender = board.get(primary_target_cell)

        if not primary_defender: 
            print(f"Основная цель на {primary_target_cell} больше не существует.")
            archer_token.special_used = True 
            return True 

        print(f"\nЛучник ({archer_token.get_stats_str()}) атакует основную цель: {primary_defender} ({primary_defender.get_stats_str()}) на {primary_target_cell}.")
        
        # Атака основной цели
        status_primary = apply_damage_to_target(primary_defender, archer_token.attack, f"{archer_token} (основная цель)")
        if status_primary == "dead":
            board[primary_target_cell] = None
        
        archer_token.special_used = True 

        # Проверяем, жив ли лучник после атаки основной цели (хотя контратаки нет)
        if not (board.get(archer_cell_label) == archer_token and archer_token.hp > 0):
            print("Лучник погиб или исчез во время атаки основной цели!")
            return True 
        
        print(f"\nЗональный эффект вокруг {primary_target_cell}!")
        area_damage = archer_token.attack // 2 
        if area_damage == 0 and archer_token.attack > 0 : area_damage = 1 
        
        cells_for_area_damage = neighbors_map.get(primary_target_cell, [])
        
        for secondary_target_cell in cells_for_area_damage:
            token_in_area = board.get(secondary_target_cell)
            if token_in_area: 
                # Не бьем по основной цели еще раз, если она и есть сосед (маловероятно)
                if secondary_target_cell == primary_target_cell and status_primary != "dead": 
                    continue 

                print(f"Зональный урон ({area_damage}) по {token_in_area} ({token_in_area.get_stats_str()}) на {secondary_target_cell}.")
                status_secondary = apply_damage_to_target(token_in_area, area_damage, "Зональная атака лучника")
                if status_secondary == "dead":
                    board[secondary_target_cell] = None
        return True 

    elif archer_choice == "normal_ranged_attack":
        print("Лучник готовит обычную дальнюю атаку...")
        targets = select_targets_in_radius(
            "Выберите вражескую цель для обычной атаки",
            archer_cell_label, extended_targets, current_turn_side,
            max_targets=1, target_must_be_enemy=True
        )
        if not targets:
            print("Обычная атака лучника отменена, цель не выбрана.")
            return False

        target_cell = targets[0]
        defender = board.get(target_cell)
        if defender:
            print(f"\nЛучник ({archer_token.get_stats_str()}) атакует {defender} ({defender.get_stats_str()}) на {target_cell}.")
            # Используем apply_damage_to_target, т.к. нет контратаки для дальней атаки
            status = apply_damage_to_target(defender, archer_token.attack, str(archer_token))
            if status == "dead":
                board[target_cell] = None
            return True
        else:
            print(f"Цель на {target_cell} для атаки больше не существует.")
            return False 
    return False

def knight_actions_menu(knight_token, knight_cell, current_turn_side):
    if not knight_token: return False
    print(f"\nДействия Рыцаря на {knight_cell}:")
    action_options = []
    
    can_melee_attack = any(
        board.get(n_cell) and board[n_cell].side != current_turn_side
        for n_cell in neighbors_map.get(knight_cell, [])
    )
    if can_melee_attack:
        action_options.append( ("Обычный удар (соседний враг)", "melee_normal") )

    if knight_token.special_attack_cooldown == 0 and can_melee_attack:
        action_options.append( ("Специальный удар (x2 урон, кулдаун 10 ходов)", "melee_special") )
    elif can_melee_attack: 
        action_options.append( (f"Специальный удар (недоступно, КД: {knight_token.special_attack_cooldown})", None) )
    
    action_options.append(("Отмена", "cancel"))

    if not any(val for _, val in action_options if val and val != "cancel"):
        print("Рыцарь не может атаковать (нет целей или способности на кулдауне).")
        return False

    chosen_action = choose_option("Выберите действие Рыцаря:", action_options)

    if not chosen_action or chosen_action == "cancel" or chosen_action is None:
        print("Действие Рыцаря отменено.")
        return False

    if chosen_action == "melee_normal" or chosen_action == "melee_special":
        melee_targets_info = []
        for n_cell in neighbors_map.get(knight_cell, []):
            token_on_cell = board.get(n_cell)
            if token_on_cell and token_on_cell.side != current_turn_side:
                melee_targets_info.append( (f"Атаковать {token_on_cell} на {n_cell} ({token_on_cell.get_stats_str()})", n_cell) )
        
        if not melee_targets_info: 
            print("Нет соседних врагов для атаки.")
            return False
        
        melee_targets_info.append(("Отменить удар", "cancel_strike"))
        target_cell_for_strike = choose_option("Выберите цель для удара:", melee_targets_info)
        
        if not target_cell_for_strike or target_cell_for_strike == "cancel_strike":
            print("Удар отменен.")
            return False

        defender = board.get(target_cell_for_strike)
        if not defender: print(f"Цель на {target_cell_for_strike} исчезла."); return False

        if chosen_action == "melee_special":
            if knight_token.special_attack_cooldown == 0:
                knight_special_attack(knight_token, defender, knight_cell, target_cell_for_strike)
                # Кулдаун устанавливается внутри knight_special_attack
                return True
            else: 
                print("Специальный удар на кулдауне.")
                return False # Не удалось выполнить
        else: 
            combat(knight_token, defender, knight_cell, target_cell_for_strike)
            return True
    return False

def knight_special_attack(attacker, defender, attacker_cell, defender_cell):
    if not attacker: return {"attacker_status": "dead", "defender_status": "alive" if defender else "dead"}
    if not defender: return {"attacker_status": "alive", "defender_status": "dead"}

    print(f"\n{attacker} ({attacker.get_stats_str()}) использует СПЕЦИАЛЬНЫЙ УДАР против {defender} ({defender.get_stats_str()}) на {defender_cell}!")
    results = {"attacker_status": "alive", "defender_status": "alive"}
    
    # РЫЦАРЬ АТАКУЕТ С ДВОЙНОЙ СИЛОЙ
    special_attack_value = attacker.attack * 2
    
    # Применяем специальный урон Рыцаря к защитнику
    defender_status_after_special = apply_damage_to_target(defender, special_attack_value, f"{attacker} (спец. удар x2)")
    
    # Кулдаун ставится независимо от исхода атаки по защитнику, если атакующий (Рыцарь) жив
    if attacker and board.get(attacker_cell) == attacker: # Проверяем, что рыцарь все еще на доске и это он
         attacker.special_attack_cooldown = 10 

    if defender_status_after_special == "dead":
        board[defender_cell] = None
        results["defender_status"] = "dead"
        return results # Защитник убит, контратаки нет
    elif defender_status_after_special == "target_gone": # Если цель исчезла до удара
        results["defender_status"] = "dead" # Считаем, что цели нет
        return results

    # КОНТРАТАКА ЗАЩИТНИКА (стандартный урон)
    # Проверяем, жив ли еще защитник и на доске ли он
    if board.get(defender_cell) == defender and defender.hp > 0: 
        print(f"\n{defender} ({defender.get_stats_str()}) контратакует {attacker} ({attacker.get_stats_str()}) после спец. удара!")
        # Проверяем, жив ли атакующий (Рыцарь) перед контратакой
        if board.get(attacker_cell) == attacker and attacker.hp > 0: 
            attacker_status_after_counter = apply_damage_to_target(attacker, defender.attack, str(defender)) # Обычная атака защитника
            if attacker_status_after_counter == "dead":
                board[attacker_cell] = None
                results["attacker_status"] = "dead"
            elif attacker_status_after_counter == "target_gone": # Если Рыцарь исчез
                 results["attacker_status"] = "dead" 
        else:
            print(f"{attacker} не может быть контратакован (побежден или не на клетке).")
    else:
        print(f"{defender} не может контратаковать (уже побежден или не на клетке).")
            
    return results

def soldier_knockback_attack(attacker, defender, attacker_cell, defender_cell):
    if not attacker: return {"attacker_status": "dead", "defender_status": "alive" if defender else "dead"}
    if not defender: return {"attacker_status": "alive", "defender_status": "dead"}

    print(f"\n{attacker} ({attacker.get_stats_str()}) на {attacker_cell} использует отбрасывающую атаку на {defender} ({defender.get_stats_str()}) на {defender_cell}!")
    results = {"attacker_status": "alive", "defender_status": "alive"}
    
    knockback_damage = 2 
    defender_status_after_kb_dmg = apply_damage_to_target(defender, knockback_damage, f"{attacker} (отбрасывание)")
    
    if attacker and board.get(attacker_cell) == attacker: # Если солдат еще жив
        attacker.knockback_cooldown = 7

    if defender_status_after_kb_dmg == "dead":
        board[defender_cell] = attacker 
        if attacker_cell != defender_cell and board.get(attacker_cell) == attacker : board[attacker_cell] = None
        results["defender_status"] = "dead"
        return results
    elif defender_status_after_kb_dmg == "target_gone": 
        if board.get(defender_cell) is None and board.get(attacker_cell) == attacker:
            board[defender_cell] = attacker
            if attacker_cell != defender_cell: board[attacker_cell] = None
        results["defender_status"] = "dead" # Считаем, что цели нет
        return results

    empty_neighbors_for_defender = [
        nbr for nbr in neighbors_map.get(defender_cell, []) 
        if board.get(nbr) is None and nbr != attacker_cell 
    ]

    if empty_neighbors_for_defender:
        new_pos_for_defender = random.choice(empty_neighbors_for_defender)
        print(f"Враг {defender} отброшен с {defender_cell} на {new_pos_for_defender}.")
        board[new_pos_for_defender] = defender 
        board[defender_cell] = attacker      
        if attacker_cell != defender_cell and board.get(attacker_cell) == attacker : board[attacker_cell] = None 
    else:
        print(f"Нет свободной клетки для отбрасывания {defender}. Враг остается на месте.")
    
    return results

def repair_shield(soldier_token):
    if not soldier_token: return False
    if soldier_token.max_defense is None or soldier_token.max_defense == 0:
        print(f"{soldier_token} не имеет щита для ремонта.")
        return False 
    if soldier_token.defense >= soldier_token.max_defense:
        print(f"{soldier_token} уже имеет максимальную защиту.")
        return False 

    repair_amount = max(1, int(0.25 * soldier_token.max_defense))
    old_def = soldier_token.defense
    soldier_token.defense = min(soldier_token.defense + repair_amount, soldier_token.max_defense)
    print(f"{soldier_token} ремонтирует щит: {old_def} -> {soldier_token.defense} (восстановлено {soldier_token.defense - old_def}).")
    soldier_token.shield_repair_cooldown = 6
    return True 

board["3"] = Token('B', "Soldier", 10, 5, 4); board["4"] = Token('B', "Mage", 6, 3, 2)
board["C"] = Token('B', "Knight", 5, 4, 8); board["2"] = Token('B', "Archer", 4, 7, 1) 
board["L"] = Token('R', "Soldier", 10, 5, 4); board["O"] = Token('R', "Mage", 6, 3, 2)
board["K"] = Token('R', "Knight", 5, 4, 8); board["N"] = Token('R', "Archer", 4, 7, 1) 

def get_available_moves(cell_label, token):
    empty_moves = []
    enemy_moves_info = [] 
    for nbr_label in neighbors_map.get(cell_label, []):
        target_on_nbr = board.get(nbr_label)
        if target_on_nbr is None: empty_moves.append(nbr_label)
        elif target_on_nbr.side != token.side:
            if token.tclass == "Soldier" and token.knockback_cooldown == 0:
                enemy_moves_info.append((nbr_label, "knockback"))
            enemy_moves_info.append((nbr_label, "normal_attack")) 
    return empty_moves, enemy_moves_info

def update_statuses_and_cooldowns():
    for token_obj in board.values(): 
        if token_obj is not None:
            if token_obj.frozen > 0:
                token_obj.frozen -= 1
                if token_obj.frozen == 0: print(f"{token_obj} разморожен.")
            if token_obj.tclass == "Mage" and token_obj.cooldown > 0: token_obj.cooldown -= 1
            if token_obj.tclass == "Knight" and token_obj.special_attack_cooldown > 0: token_obj.special_attack_cooldown -=1
            if token_obj.tclass == "Soldier":
                if token_obj.knockback_cooldown > 0: token_obj.knockback_cooldown -= 1
                if token_obj.shield_repair_cooldown > 0: token_obj.shield_repair_cooldown -= 1

def main():
    current_turn_side = 'B'
    turn_count = 1
    main_loop_active = True

    while main_loop_active:
        print(f"\n--- Ход {turn_count} ({'Синие' if current_turn_side == 'B' else 'Красные'}) ---")
        update_statuses_and_cooldowns()
        print_board()

        blue_tokens_exist = any(t and t.side == 'B' for t in board.values())
        red_tokens_exist = any(t and t.side == 'R' for t in board.values())
        if not blue_tokens_exist: print("\nПОБЕДИЛИ КРАСНЫЕ!"); main_loop_active = False; continue
        if not red_tokens_exist: print("\nПОБЕДИЛИ СИНИЕ!"); main_loop_active = False; continue

        action_for_current_player_done = False
        
        player_token_choices_for_turn = [] # Список кортежей (display_str, (cell, token_obj))
        all_player_tokens_are_frozen = True
        has_any_active_tokens = False

        for cell, token_obj_loop in board.items():
            if token_obj_loop and token_obj_loop.side == current_turn_side:
                has_any_active_tokens = True # У игрока в принципе есть токены
                if token_obj_loop.frozen == 0:
                    all_player_tokens_are_frozen = False
                    display_str = f"{token_obj_loop} на {cell} ({token_obj_loop.get_stats_str()})"
                    player_token_choices_for_turn.append( (display_str, (cell, token_obj_loop)) )
        
        if not has_any_active_tokens : 
            print(f"У игрока {current_turn_side} нет токенов на поле. Пропуск хода.")
            action_for_current_player_done = True
        elif all_player_tokens_are_frozen:
            print(f"Все токены игрока {current_turn_side} заморожены. Ход пропускается.")
            action_for_current_player_done = True
        
        if action_for_current_player_done: 
            current_turn_side = 'R' if current_turn_side == 'B' else 'B'
            turn_count += 1
            if main_loop_active: input("\nНажмите Enter для следующего хода...")
            continue 

        while not action_for_current_player_done and main_loop_active:
            # Обновляем список активных токенов для выбора на каждой итерации этого цикла
            current_player_active_tokens_for_choice = []
            for cell, token_obj_loop in board.items():
                 if token_obj_loop and token_obj_loop.side == current_turn_side and token_obj_loop.frozen == 0:
                    display_str = f"{token_obj_loop} на {cell} ({token_obj_loop.get_stats_str()})"
                    current_player_active_tokens_for_choice.append( (display_str, (cell, token_obj_loop)) )
            
            if not current_player_active_tokens_for_choice: # Все активные токены могли быть убиты/заморожены действиями других своих же токенов
                print(f"У игрока {current_turn_side} не осталось доступных для хода токенов.")
                action_for_current_player_done = True
                break

            options_for_player_action_selection = list(current_player_active_tokens_for_choice) 
            options_for_player_action_selection.append(("Пропустить ход (завершить ход игрока)", "skip_player_turn"))

            print(f"\nХод игрока {current_turn_side}.")
            chosen_token_tuple_or_skip_command = choose_option("Выберите токен для действия или пропустите ход:", options_for_player_action_selection)

            if chosen_token_tuple_or_skip_command is None: 
                main_loop_active = False; break 
            
            if chosen_token_tuple_or_skip_command == "skip_player_turn":
                print(f"Игрок {current_turn_side} пропускает ход.")
                action_for_current_player_done = True
                break 

            chosen_token_cell, chosen_token_obj = chosen_token_tuple_or_skip_command
            current_pos_of_token = chosen_token_cell # Это позиция токена НА МОМЕНТ ВЫБОРА
            
            token_action_loop_active = True 
            while token_action_loop_active and main_loop_active:
                # Проверяем актуальное состояние токена перед каждым меню действий для него
                actual_token_on_cell = board.get(current_pos_of_token)
                if not (actual_token_on_cell == chosen_token_obj and chosen_token_obj.hp > 0 and chosen_token_obj.frozen == 0):
                    print(f"{chosen_token_obj} больше не доступен для действий на {current_pos_of_token} (возможно, был перемещен, убит или заморожен).")
                    action_for_current_player_done = False # Возврат к выбору другого токена / пропуска хода игрока
                    token_action_loop_active = False # Выход из цикла действий этого токена
                    continue # К началу цикла while not action_for_current_player_done

                token_action_choices = [("Переместиться", "move")]
                if chosen_token_obj.tclass == "Soldier" and chosen_token_obj.shield_repair_cooldown == 0:
                    token_action_choices.append(("Ремонт щита (остаться на месте)", "repair_shield"))
                
                # Проверяем, есть ли вообще осмысленные способности/атаки с текущей клетки
                can_use_ability_here = False
                if chosen_token_obj.tclass == "Mage":
                    has_mage_targets = any(board.get(t_cell) and board.get(t_cell).side != current_turn_side for t_cell in extended_targets(current_pos_of_token))
                    can_heal_mage = chosen_token_obj.cooldown == 0 and any(
                        token_on_cell and token_on_cell.side == current_turn_side and token_on_cell.hp < token_on_cell.max_hp
                        for token_on_cell in [board.get(c) for c in list(set(extended_targets(current_pos_of_token) + [current_pos_of_token]))] if token_on_cell
                    )
                    if has_mage_targets or can_heal_mage: can_use_ability_here = True
                elif chosen_token_obj.tclass == "Archer":
                    if any(board.get(t_cell) and board.get(t_cell).side != current_turn_side for t_cell in extended_targets(current_pos_of_token)):
                        can_use_ability_here = True
                elif chosen_token_obj.tclass == "Knight" or chosen_token_obj.tclass == "Soldier":
                    if any(board.get(n_cell) and board.get(n_cell).side != current_turn_side for n_cell in neighbors_map.get(current_pos_of_token, [])):
                        can_use_ability_here = True
                
                if can_use_ability_here:
                    token_action_choices.append((f"Использовать способность/Атаковать ({chosen_token_obj.tclass} с текущей клетки)", "ability_attack_here"))
                
                token_action_choices.append(("Отменить действие с этим токеном (выбрать другой токен/пропустить ход)", "cancel_this_token_action"))

                chosen_token_action_key = choose_option(f"Действие для {chosen_token_obj} на {current_pos_of_token} ({chosen_token_obj.get_stats_str()}):", token_action_choices)

                if not chosen_token_action_key: 
                    main_loop_active = False; token_action_loop_active = False; action_for_current_player_done = True; break
                
                if chosen_token_action_key == "cancel_this_token_action":
                    token_action_loop_active = False 
                    action_for_current_player_done = False    
                    break 

                performed_token_final_action = False 
                action_after_move_possible = True # Флаг, что после перемещения на пустую клетку есть еще действия

                if chosen_token_action_key == "repair_shield":
                    if repair_shield(chosen_token_obj):
                        performed_token_final_action = True
                
                elif chosen_token_action_key == "move":
                    empty_moves, enemy_moves_info_list = get_available_moves(current_pos_of_token, chosen_token_obj)
                    movement_options = []
                    for e_move in empty_moves: movement_options.append( (f"На пустую клетку {e_move}", ("move_empty", e_move)) )
                    for en_move_label, atk_type in enemy_moves_info_list:
                        dfndr = board.get(en_move_label)
                        if dfndr: 
                            if atk_type == "knockback": movement_options.append( (f"Атаковать (отбрасывание) {dfndr} на {en_move_label}", ("move_knockback", en_move_label)) )
                            movement_options.append( (f"Переместиться и атаковать {dfndr} на {en_move_label}", ("move_attack_normal", en_move_label)) )
                    
                    if not movement_options:
                        print("Нет доступных клеток для перемещения или атаки при перемещении.")
                        action_after_move_possible = can_use_ability_here # Может ли атаковать с места после неудачного мува
                        if not action_after_move_possible: performed_token_final_action = True # Если и с места не может, ход токена завершен
                    else:
                        movement_options.append( ("Отменить перемещение (остаться на месте)", ("cancel_move", current_pos_of_token)) )
                        chosen_move_action_tuple = choose_option("Куда переместить/атаковать?", movement_options)

                        if chosen_move_action_tuple:
                            move_action_type, target_cell = chosen_move_action_tuple
                            original_attacker_pos_before_move = current_pos_of_token 

                            if move_action_type == "move_empty":
                                print(f"{chosen_token_obj} перемещается с {original_attacker_pos_before_move} на {target_cell}.")
                                board[target_cell] = chosen_token_obj
                                if original_attacker_pos_before_move != target_cell: board[original_attacker_pos_before_move] = None
                                current_pos_of_token = target_cell 
                                
                                # Проверка, есть ли действия с новой позиции
                                can_act_after_empty_move = False
                                if chosen_token_obj.tclass == "Mage":
                                    has_mage_targets = any(board.get(t_cell) and board.get(t_cell).side != current_turn_side for t_cell in extended_targets(current_pos_of_token))
                                    can_heal_mage = chosen_token_obj.cooldown == 0 and any(tk_obj and tk_obj.side == current_turn_side and tk_obj.hp < tk_obj.max_hp for tk_obj in [board.get(c) for c in list(set(extended_targets(current_pos_of_token) + [current_pos_of_token]))] if tk_obj)
                                    if has_mage_targets or can_heal_mage: can_act_after_empty_move = True
                                elif chosen_token_obj.tclass == "Archer":
                                    if any(board.get(t_cell) and board.get(t_cell).side != current_turn_side for t_cell in extended_targets(current_pos_of_token)): can_act_after_empty_move = True
                                elif chosen_token_obj.tclass == "Knight" or chosen_token_obj.tclass == "Soldier":
                                    if any(board.get(n_cell) and board.get(n_cell).side != current_turn_side for n_cell in neighbors_map.get(current_pos_of_token, [])): can_act_after_empty_move = True
                                
                                if not can_act_after_empty_move:
                                    print(f"{chosen_token_obj} переместился на {current_pos_of_token}, но не имеет доступных действий оттуда.")
                                    performed_token_final_action = True
                                else:
                                    action_after_move_possible = True # Даем шанс атаковать/использовать способность
                            
                            elif move_action_type == "move_knockback":
                                defender = board.get(target_cell)
                                if defender: 
                                    soldier_knockback_attack(chosen_token_obj, defender, original_attacker_pos_before_move, target_cell)
                                    new_pos = next((c for c, t in board.items() if t == chosen_token_obj), None)
                                    if new_pos: current_pos_of_token = new_pos
                                    else: current_pos_of_token = None 
                                performed_token_final_action = True 
                            
                            elif move_action_type == "move_attack_normal":
                                defender = board.get(target_cell)
                                if defender: 
                                    results = combat(chosen_token_obj, defender, original_attacker_pos_before_move, target_cell)
                                    if results["defender_status"] == "dead" and results["attacker_status"] == "alive":
                                        board[target_cell] = chosen_token_obj
                                        if original_attacker_pos_before_move != target_cell: board[original_attacker_pos_before_move] = None
                                        current_pos_of_token = target_cell
                                    elif results["attacker_status"] == "dead":
                                         current_pos_of_token = None 
                                performed_token_final_action = True
                            
                            elif move_action_type == "cancel_move":
                                print(f"{chosen_token_obj} остается на {current_pos_of_token}.")
                                action_after_move_possible = can_use_ability_here # Может ли атаковать с места
                                if not action_after_move_possible: performed_token_final_action = True
                        else: 
                            main_loop_active = False; token_action_loop_active = False; action_for_current_player_done = True; break
                
                # Если выбрано "ability_attack_here" ИЛИ (после "move" не было финального действия И есть возможность действовать)
                if chosen_token_action_key == "ability_attack_here" or \
                   (chosen_token_action_key == "move" and not performed_token_final_action and action_after_move_possible):
                    
                    token_still_on_board_and_alive = current_pos_of_token and board.get(current_pos_of_token) == chosen_token_obj and chosen_token_obj.hp > 0
                    
                    if token_still_on_board_and_alive:
                        made_action_with_ability_now = False
                        if chosen_token_obj.tclass == "Mage": made_action_with_ability_now = mage_attack_menu(chosen_token_obj, current_pos_of_token, current_turn_side)
                        elif chosen_token_obj.tclass == "Archer": made_action_with_ability_now = archer_area_attack_action(chosen_token_obj, current_pos_of_token, current_turn_side)
                        elif chosen_token_obj.tclass == "Knight": made_action_with_ability_now = knight_actions_menu(chosen_token_obj, current_pos_of_token, current_turn_side)
                        elif chosen_token_obj.tclass == "Soldier":
                            s_melee_opts = []
                            for nc in neighbors_map.get(current_pos_of_token, []):
                                t_on_nc = board.get(nc)
                                if t_on_nc and t_on_nc.side != current_turn_side: s_melee_opts.append((f"Атаковать {t_on_nc} на {nc} ({t_on_nc.get_stats_str()})", nc))
                            if s_melee_opts:
                                s_melee_opts.append(("Отменить атаку", "cancel_s_atk"))
                                s_target_cell = choose_option(f"Солдат на {current_pos_of_token}, обычная атака:", s_melee_opts)
                                if s_target_cell and s_target_cell != "cancel_s_atk":
                                    s_defender = board.get(s_target_cell)
                                    if s_defender: combat(chosen_token_obj, s_defender, current_pos_of_token, s_target_cell)
                                    made_action_with_ability_now = True
                                else: 
                                    print("Атака солдата отменена.")
                                    # Если отменил, но это было единственное действие (ability_attack_here), то не финальное
                                    if chosen_token_action_key == "ability_attack_here": made_action_with_ability_now = False
                                    else: made_action_with_ability_now = True # Если после move, то ход завершен
                            else: 
                                print(f"У Солдата на {current_pos_of_token} нет целей для атаки с места.")
                                if chosen_token_action_key == "ability_attack_here": made_action_with_ability_now = False
                                else: made_action_with_ability_now = True
                        
                        if made_action_with_ability_now:
                            performed_token_final_action = True
                        # Если выбрал способность с места, но отменил ее или не смог
                        elif chosen_token_action_key == "ability_attack_here" and not made_action_with_ability_now : 
                            print(f"{chosen_token_obj} не смог/отменил способность/атаку с места.")
                            performed_token_final_action = False # Даем шанс выбрать другое действие с этим токеном
                        else: # Если это было после move_empty и способность не удалась/отменена
                             performed_token_final_action = True # Ход токена все равно завершен
                    else: 
                        performed_token_final_action = True 
                
                if performed_token_final_action:
                    token_action_loop_active = False 
                    action_for_current_player_done = True    
                else:
                    # Если ни одно финальное действие не было совершено (например, отмена на всех этапах)
                    # игрок остается в цикле действий для этого токена.
                    print(f"{chosen_token_obj} не совершил финального действия. Выберите другое действие для этого токена.")
            
            if not main_loop_active: break 
        
        if not main_loop_active: break 

        current_turn_side = 'R' if current_turn_side == 'B' else 'B'
        turn_count += 1
        if main_loop_active: 
            input("\nНажмите Enter для следующего хода...")

if __name__ == "__main__":
    main()