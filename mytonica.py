from pygamelib import engine, base, board_items, constants, actuators
from pygamelib.assets import graphics
from pygamelib.gfx import core
import simpleaudio as sa
import sys
import os
import time
import copy
import random
from game import life, media, levels

difficulties = {"easy": 0.25, "normal": 0.1, "hard": 0.01}
current_difficulty = "normal"

wave_obj = list()

# Get current working directory
wd = ""
try:
    wd = sys._MEIPASS
except AttributeError:
    wd = os.getcwd()

# wave_obj.append(sa.WaveObject.from_wave_file(os.path.join(wd, "sfx", "sound_01.wav")))
# wave_obj.append(sa.WaveObject.from_wave_file(os.path.join(wd, "sfx", "sound_02.wav")))


def load_sounds(game):
    pass


def load_sprites(game):
    game.sprites = core.SpriteCollection.load_json_file(
        os.path.join(wd, "gfx", "mytonica.spr")
    )


def display_sprite_at(game, spr, row, column):
    for r in range(0, spr.size[1]):
        for c in range(0, spr.size[0]):
            game.screen.display_at(
                spr.sprixel(r, c), row + r, column + c,
            )


def title_screen(game):
    if game.sprites is None:
        load_sprites(game)
    with game.terminal.cbreak(), game.terminal.hidden_cursor(), (
        game.terminal.fullscreen()
    ):
        k = None
        menu_index = 0
        while True:
            if k == "q":
                game.stop()
                break
            elif k == engine.key.ENTER:  #  or (k is not None and k.name == "KEY_ENTER")
                if menu_index % 4 == 0:
                    game.current_state = "tutorial"
                    break
                elif menu_index % 4 == 1:
                    game.current_state = "game"
                    break
                elif menu_index % 4 == 2:
                    game.current_state = "credits"
                    break
                else:
                    game.stop()
                    break
            elif k == engine.key.LEFT or k == engine.key.DOWN:
                menu_index -= 1
            elif k == engine.key.RIGHT or k == engine.key.UP:
                menu_index += 1

            # game.clear_screen()
            print(
                f"{game.terminal.home}{game.terminal.on_color_rgb(39,43,47)}{game.terminal.clear}"
            )
            game.screen.display_at(base.Text.magenta_bright("#olcCodeJam2020"), 3, 2)
            title = game.sprites["title_screen"]
            rstart = int((game.screen.height - title.size[1]) / 2)
            cstart = int(game.screen.width / 2) - 4 - int(title.size[0] / 2)
            display_sprite_at(game, title, rstart, cstart)
            offset = round((title.size[0] - 29) / 2)
            text = "Tutorial"
            if menu_index % 4 == 0:
                text = base.Text.green_bright("Tutorial")
            game.screen.display_at(text, rstart + title.size[1] + 1, offset + cstart)
            text = "Play"
            if menu_index % 4 == 1:
                text = base.Text.green_bright("Play")
            game.screen.display_at(
                text, rstart + title.size[1] + 1, offset + cstart + 10
            )
            text = "Credits"
            if menu_index % 4 == 2:
                text = base.Text.green_bright("Credits")
            game.screen.display_at(
                text, rstart + title.size[1] + 1, offset + cstart + 16
            )
            text = "Quit"
            if menu_index % 4 == 3:
                text = base.Text.green_bright("Quit")
            game.screen.display_at(
                text, rstart + title.size[1] + 1, offset + cstart + 25
            )
            note = game.sprites["title_note"]
            display_sprite_at(
                game, note, rstart - note.size[1], cstart - note.size[0] - 2
            )
            display_sprite_at(
                game, note, rstart + title.size[1], cstart + title.size[0]
            )
            display_sprite_at(
                game, note, rstart + title.size[1] + 5, cstart + int(title.size[0] / 2),
            )
            display_sprite_at(
                game,
                note.flip_vertically(),
                rstart - note.size[1] - 5,
                cstart + int(2 * title.size[0] / 3),
            )

            game.screen.display_at(
                base.Text.green_bright("build with pygamelib"),
                game.screen.height - 1,
                game.screen.width - 20,
            )
            k = game.get_key()


def credits_screen(game):
    if game.sprites is None:
        load_sprites(game)
    with game.terminal.cbreak(), game.terminal.hidden_cursor(), (
        game.terminal.fullscreen()
    ):
        print(
            f"{game.terminal.home}{game.terminal.on_color_rgb(39,43,47)}{game.terminal.clear}"
        )
        display_sprite_at(
            game,
            game.sprites["title_screen"],
            2,
            int(game.screen.width / 2)
            - 4
            - int(game.sprites["title_screen"].size[0] / 2),
        )
        text = "Code, artwork, sound and coffee consumption:"
        game.screen.display_at(
            base.Text.white_bright(text),
            game.sprites["title_screen"].size[1] + 5,
            int(game.screen.width / 2) - 2 - int(2 * len(text) / 3),
        )
        text2 = "Arnaud Dupuis"
        game.screen.display_at(
            base.Text.magenta_bright(text2),
            game.sprites["title_screen"].size[1] + 5,
            int(game.screen.width / 2) - 1 - int(2 * len(text) / 3) + len(text),
        )
        text = "Made with the pygamelib:"
        game.screen.display_at(
            base.Text.white_bright(text),
            game.sprites["title_screen"].size[1] + 7,
            int((game.screen.width / 2) - 4 - len(text)),
        )
        text2 = "https://www.pygamelib.org"
        game.screen.display_at(
            base.Text.green_bright(game.terminal.link(text2, text2)),
            game.sprites["title_screen"].size[1] + 7,
            int(game.screen.width / 2) - 2,
        )
        text = "https://8bitscoding.io"
        game.screen.display_at(
            base.Text.cyan(game.terminal.link(text, text)),
            game.sprites["title_screen"].size[1] + 9,
            int(game.screen.width / 2) - 2 - int(len(text) / 2),
        )
        # Back to title screen
        game.screen.display_at(
            "Press ENTER to return to the main menu.", game.screen.height - 1, 1
        )
        game.current_state = "title_screen"
        input()


def tuto_update(game, inkey, elapsed_time):
    update(game, inkey, elapsed_time)
    if game.lvl_object.state == 0:
        game.screen.display_line(
            "Welcome Main Loop Controller (MLC).\n"
            f"We are tasked with the development of this new organic machine called '{base.Text.green('life')}'.\n"
            "The Master Control Program thinks that it will be the greatest machine ever!\n\n"
            f"First, let's review the controls: {base.Text.blue_bright('TAB')} allow you to switch between your encoding pad, your cells pool pad and the commands pad.\n"
            "Try it now."
        )
        if inkey.name == "KEY_TAB":
            game.lvl_object.state += 1
    elif game.lvl_object.state == 1:
        game.screen.display_line(
            "Wonderful!\n"
            "Each pad has it's own usage. However they share some similarities.\n"
            f"In all pads, use the {base.Text.blue_bright('arrow keys')} to move the cursor.\n"
            f"When you hit {base.Text.blue_bright('ENTER')} while focused on cell pool "
            "or commands, the item is selected and the focus comes back to the encoding pad.\n"
            f"In the COMMANDS pad you need to hit {base.Text.blue_bright('ENTER')} to select a command. If you don't the command is cancelled and nothing changes."
            "Try it now."
        )
        if inkey in [engine.key.UP, engine.key.DOWN, engine.key.LEFT, engine.key.RIGHT]:
            game.lvl_object.state += 1
            game.focus_index = 0
            game.cmds_focus_index = 0
            game.cmds_select_index = 0
    elif game.lvl_object.state == 2:
        game.screen.display_line(
            "Fantastic!\n\n"
            f"The {base.Text.magenta_bright('encoding pad')} is where the program happen.\n"
            f"You're main goal is to collect genetic material ({graphics.GeometricShapes.CIRCLE_WITH_LOWER_HALF_BLACK+graphics.GeometricShapes.CIRCLE_WITH_UPPER_HALF_BLACK}) to create more complex cells.\n"
            f"Position cells on the pad by moving your cursor and pressing the {base.Text.blue_bright('space bar')}.\n"
            f"You have 4 base cells, they all move in only one direction {game.terminal.color_rgb(255,0,0)}up{game.terminal.normal}, "
            f"{game.terminal.color_rgb(0,255,0)}down{game.terminal.normal}, {game.terminal.color_rgb(0,0,255)}left{game.terminal.normal} "
            f"and {game.terminal.color_rgb(255,0,255)}right{game.terminal.normal}.\n"
            "Place some cells on the encoding pad so the cells go get the genetic material. Pay attention to the walls: your cells can't go through they have to find their way around."
        )
        if inkey.name == "KEY_SPACE" or inkey == engine.key.SPACE:
            game.lvl_object.state += 1
    elif game.lvl_object.state == 3:
        game.screen.display_line(
            f"Once positionned on the pad, you can {base.Text.green_bright('RUN')} the simulation.\n"
            "Pay attention to the maximum number of cells you have at your disposal."
            "The cell will move, reproduce and evolve. Diversity and harmony is key.\n"
            "Watching and listening them live and evolve is fascinating!\n"
            "Oh yes, they make weird sounds... MCP thinks it is a feature... I am not so sure..."
        )
        if game.cmds_select_index == 1:
            game.lvl_object.state += 1
    elif game.lvl_object.state == 4:
        game.screen.display_line(
            "During the real simulations the traits of the selected cell is going to be displayed here.\n"
            f"If you think that your simulation is not worth keeping you can {base.Text.green_bright('RESET')} the simulation.\n"
            "Cell evolve and mutate, giving you the opportunity to gain more material. Hopefully new colors and complex cords are going to emerge!\n"
            "At each stage you will get more cells (but never more than 24, new ones replacing the old ones).\n"
            "Your simulation is going to be graded based on your efficiency. Do not disappoint us MLC!\n"
            f"One last thing: be careful, not every program is sold to that '{base.Text.green('life')}' thing... You might encounter resistance and sabotage..."
        )
        if len(game.current_board().get_immovables(type="genetic_material")) == 0:
            game.screen.display_line(
                f"Press the {base.Text.blue_bright('ESC')} button to continue."
            )
            if inkey == engine.key.ESC:
                game.lvl_object.state += 1
    elif game.lvl_object.state == 5:
        game.screen.display_line(
            "The new genetic material is now available in your CELL POOL.\n"
            "Use it wisely! Good luck!\n\n"
            f"Press the {base.Text.blue_bright('ESC')} button to finish this tutorial."
        )
        if inkey == engine.key.ESC:
            goto_level(game, 1)


def tutorial(game):
    goto_level(game, 0)
    game.user_update = tuto_update
    game.current_state = "game"


def goto_level(game, lvl_number):
    # We should try to see if a board is already loaded but... no time!!!!
    lvl = levels.Level(lvl_number)
    lvl.board = game.load_board(os.path.join(wd, lvl.map), lvl.number)
    for i in lvl.board.get_immovables(type="genetic_material"):
        p = i.pos
        lvl.board.clear_cell(p[0], p[1])
        gene = life.GeneticMaterial(action=pickup, action_parameters=[game])
        gene.action_parameters.append(gene)
        lvl.board.place_item(gene, p[0], p[1])

    game.change_level(lvl.number)
    game.user_update = update
    game.life_pool = list()
    game.cell_index = 0
    game.focus_index = 0
    game.cells_focus_index = 0
    game.cmds_focus_index = 0
    game.cmds_select_index = 0
    game.used_cells = 0
    game.lvl_object = lvl


def clean_up(game):
    b = game.current_board()
    for r in range(0, b.height):
        for c in range(0, b.width):
            i = b.item(r, c)
            if (
                isinstance(i, life.Organism)
                and i.lifespan <= 0
                and i not in game.life_pool
            ):
                b.clear_cell(r, c)


# I'm forced to write that function, it means that we need a hook to actuate functions
# in the pygamelib to process specific data on top of just moving stuff around.
def update_life(game, elapsed_time):
    if game.state == constants.RUNNING and game.cmds_select_index == 1:
        if game.current_level in game._boards.keys():
            trigger_cleanup = False
            for idx in range(len(game.life_pool) - 1, -1, -1):
                npc = game.life_pool[idx]

                # Mass extinction!!!!
                if npc.lifespan <= 0:
                    try:
                        game.current_board().remove_item(npc)
                    except base.PglException:
                        # if npc.lifespan <= -10:
                        #     del game.life_pool[idx]
                        if npc.lifespan < 0:
                            trigger_cleanup = True
                    else:
                        del game.life_pool[idx]
                # Funny stuff
                min_dt = 1.0
                i = None
                for p in [
                    base.Vector2D.from_direction(constants.UP, 1),
                    base.Vector2D.from_direction(constants.DOWN, 1),
                    base.Vector2D.from_direction(constants.LEFT, 1),
                    base.Vector2D.from_direction(constants.RIGHT, 1),
                ]:
                    nr = npc.row + p.row
                    nc = npc.column + p.column
                    if (
                        nr < 0
                        or nr >= game.current_board().height
                        or nc < 0
                        or nc >= game.current_board().width
                    ):
                        continue
                    tmp_i = game.current_board().item(nr, nc)
                    if isinstance(tmp_i, life.Organism) and isinstance(
                        i, life.Organism
                    ):
                        # Bad but emergency
                        if i.target is None:
                            cd = 999999999999
                            for tmp_g in game.current_board().get_immovables(
                                type="genetic_material"
                            ):
                                d = i.distance_to(tmp_g)
                                if d < cd:
                                    i.target = tmp_g
                                    cd = d
                        if tmp_i.target is None:
                            cd = 999999999999
                            for tmp_g in game.current_board().get_immovables(
                                type="genetic_material"
                            ):
                                d = tmp_i.distance_to(tmp_g)
                                if d < cd:
                                    tmp_i.target = tmp_g
                                    cd = d
                    if isinstance(tmp_i, life.Organism) and i is None:
                        i = tmp_i
                    elif (
                        isinstance(tmp_i, life.Organism)
                        and i is not None
                        and isinstance(i, life.Organism)
                        and i.fitness() < tmp_i.fitness()
                    ):
                        i = tmp_i

                if (
                    isinstance(i, life.Organism)
                    and i != npc
                    and abs(i.timestamp - npc.timestamp) >= min_dt
                ):
                    # print("Making baby with someone else!")
                    baby = npc.reproduce(i)
                    # tmp
                    baby.actuator = actuators.RandomActuator(
                        moveset=[
                            constants.UP,
                            constants.DOWN,
                            constants.LEFT,
                            constants.RIGHT,
                        ]
                    )
                    done = False
                    # yummy... I'll fix that later...
                    if baby is not None:
                        for o in [npc, i]:
                            for dr in range(-1, 2, 1):
                                for dc in range(-1, 2, 1):
                                    nr = o.row + dr
                                    nc = o.column + dc
                                    if (
                                        nr >= 0
                                        and nr < game.current_board().height
                                        and nc >= 0
                                        and nc < game.current_board().width
                                        and isinstance(
                                            game.current_board().item(nr, nc),
                                            board_items.BoardItemVoid,
                                        )
                                    ):
                                        # give the baby a chance to be original
                                        baby.mutate()
                                        # baby.birth()
                                        game.life_pool.append(baby)
                                        game.current_board().place_item(baby, nr, nc)
                                        done = True
                                        break
                                if done:
                                    break
                            if done:
                                break
                    # break
                if trigger_cleanup:
                    clean_up(game)
                    game.cleanup_timer = 0
                # Now moving survivors around
                if npc.actuator.state == constants.RUNNING:
                    # Account for movement speed
                    npc.dtmove += elapsed_time
                    if (
                        game.mode == constants.MODE_RT
                        and npc.dtmove < npc.movement_speed
                    ):
                        continue
                    d = base.Vector2D.from_direction(npc.actuator.next_move(), 1)
                    if d is not None:
                        game._boards[game.current_level]["board"].move(
                            npc,
                            base.Vector2D(
                                d.row * npc.step_vertical,
                                d.column * npc.step_horizontal,
                            ),
                        )
                    npc.lifespan -= 1


def place_cell(game, row, column):
    o = copy.deepcopy(game.available_cells[game.cell_index % len(game.available_cells)])
    o.timestamp = time.time()
    min_dir = 0
    max_dir = 5
    if not isinstance(o.actuator, actuators.Actuator):
        # Give the cell a random movement set. Fitness being measured in part from the
        # distance crawled and the distance to new genetic material.
        o.actuator = actuators.RandomActuator(moveset=[])
        base_directions = [
            constants.UP,
            constants.DOWN,
            constants.LEFT,
            constants.RIGHT,
        ]
        for d in base_directions:
            for _ in range(0, random.randint(min_dir, max_dir)):
                o.actuator.moveset.append(d)
        if len(o.actuator.moveset) == 0:
            o.actuator.moveset.append(random.choice(base_directions))
        o.starting_position = [row, column]
        o.actuator.pause()
    game.current_board().place_item(
        o, row, column,
    )
    cd = 999999999999
    for i in game.current_board().get_immovables(type="genetic_material"):
        d = o.distance_to(i)
        if d < cd:
            o.target = i
            cd = d
    game.life_pool.append(o)


def update(game, inkey, elapsed_time):
    game.cleanup_timer += elapsed_time
    # Take care of inputs
    dir_map = {
        engine.key.UP: constants.UP,
        engine.key.DOWN: constants.DOWN,
        engine.key.LEFT: constants.LEFT,
        engine.key.RIGHT: constants.RIGHT,
    }
    if inkey == "q":
        game.stop()
    elif game.focus_index % 3 == 0:
        # wave_obj[game.wave_index % 2].play()
        # game.wave_index += 1
        if inkey in dir_map and game.cmds_select_index % 4 == 0:
            if (
                game.current_board().item(game.player.pos[0], game.player.pos[1])
                != game.player
            ):
                d = base.Vector2D.from_direction(dir_map[inkey], 1)
                game.current_board().place_item(
                    game.player, game.player.row + d.row, game.player.column + d.column
                )
            else:
                game.move_player(dir_map[inkey], 1)
        elif (
            (
                inkey == engine.key.SPACE
                or (hasattr(inkey, "name") and inkey.name == "KEY_SPACE")
            )
            and game.cmds_select_index % 4 == 0
            and game.lvl_object.allowed_cells - game.used_cells > 0
        ):
            place_cell(game, game.player.pos[0], game.player.pos[1])
            game.used_cells += 1
    elif game.focus_index % 3 == 1:
        if inkey == engine.key.UP:
            game.cell_index -= 3
        elif inkey == engine.key.DOWN:
            game.cell_index += 3
        elif inkey == engine.key.RIGHT:
            game.cell_index += 1
        elif inkey == engine.key.LEFT:
            game.cell_index -= 1
        elif inkey == engine.key.ENTER or (
            hasattr(inkey, "name") and inkey.name == "KEY_ENTER"
        ):
            game.focus_index = 0
    elif game.focus_index % 3 == 2:
        if inkey == engine.key.UP or inkey == engine.key.LEFT:
            game.cmds_focus_index -= 1
        elif inkey == engine.key.DOWN or inkey == engine.key.RIGHT:
            game.cmds_focus_index += 1
        elif inkey == engine.key.ENTER or (
            hasattr(inkey, "name") and inkey.name == "KEY_ENTER"
        ):
            if game.cmds_focus_index % 4 == 0:
                game.cmds_select_index = 0
                for c in game.life_pool:
                    c.actuator.pause()
                game.focus_index = 0
            elif game.cmds_focus_index % 4 == 1:
                game.cmds_select_index = 1
                for c in game.life_pool:
                    c.actuator.start()
                if (
                    game.current_board().item(game.player.row, game.player.column)
                    == game.player
                ):
                    game.current_board().clear_cell(game.player.row, game.player.column)
                game.focus_index = 0
            elif game.cmds_focus_index % 4 == 2:
                game.cmds_select_index = 2
                goto_level(game, game.current_level)
            elif game.cmds_focus_index % 4 == 3:
                game.stop()

    # We must always catch the TAB
    if inkey.name == "KEY_TAB":
        game.focus_index += 1
        if (
            game.focus_index % 3 != 2
            and game.cmds_focus_index % 3 != game.cmds_select_index
        ):
            game.cmds_focus_index = game.cmds_select_index

    # Now update life
    update_life(game, elapsed_time)

    # Then display stuff
    redraw_screen(game)
    # game.screen.display_line(f"FPS: {1/elapsed_time:2.2f}")

    # Now look if the victory condition is met
    if (
        len(game.current_board().get_immovables(type="genetic_material"))
        == game.lvl_object.winning_condition
        and game.cmds_select_index == 1
    ):
        game.score += (
            (game.lvl_object.allowed_cells - game.used_cells) * 5 * game.current_level
        )
        if game.current_level < levels.Level.max_level():
            goto_level(game, game.current_level + 1)
        else:
            game.clear_screen()
            print("\n" * 10)
            print(game.terminal.center("Thank you for playing!!!"))
            time.sleep(2)
            game.stop()
    # Cleanup
    if game.cleanup_timer > 5.0:
        clean_up(game)
        game.cleanup_timer = 0

    # for npc in game.life_pool:
    #     game.screen.display_line(
    #         f"{npc} : {npc.lifespan} moveset: {npc.actuator.moveset}"
    #     )


def draw_box(game, row, column, height, width, selected=False, title=""):
    color = ""
    end_color = ""
    scr = game.screen
    if selected:
        color = base.Fore.GREEN + base.Style.BRIGHT
        end_color = base.Style.RESET_ALL
    scr.display_at(
        f"{color}{graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_RIGHT}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*round(width/2-1-len(title)/2)}"
        f"{title}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*round(width/2-1-len(title)/2)}"
        f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*(width-round(width/2-1-len(title)/2)*2-len(title)-2)}"
        f"{graphics.BoxDrawings.LIGHT_ARC_DOWN_AND_LEFT}{end_color}",
        row,
        column,
    )
    for r in range(1, height - 1):
        scr.display_at(
            f"{color}{graphics.BoxDrawings.LIGHT_VERTICAL}{end_color}", row + r, column
        )
        scr.display_at(
            f"{color}{graphics.BoxDrawings.LIGHT_VERTICAL}{end_color}",
            row + r,
            column + width - 1,
        )
        scr.display_at(
            f"{color}{graphics.BoxDrawings.LIGHT_ARC_UP_AND_RIGHT}"
            f"{graphics.BoxDrawings.LIGHT_HORIZONTAL*(width-2)}"
            f"{graphics.BoxDrawings.LIGHT_ARC_UP_AND_LEFT}{end_color}",
            row + height - 1,
            column,
        )


def constant_to_string(s):
    if type(s) is str:
        return s
    elif s == constants.UP:
        return "UP"
    elif s == constants.DOWN:
        return "DOWN"
    elif s == constants.RIGHT:
        return "RIGHT"
    elif s == constants.LEFT:
        return "LEFT"
    elif s == constants.DRUP:
        return "DRUP"
    elif s == constants.DRDOWN:
        return "DRDOWN"
    elif s == constants.DLDOWN:
        return "DLDOWN"
    elif s == constants.DLUP:
        return "DLUP"


def redraw_screen(game):
    scr = game.screen
    scr.display_line(
        f"Difficulty: {game.lvl_object.difficulty}   Population: {len(game.life_pool)}   Remaining cells: {game.lvl_object.allowed_cells - game.used_cells}   Score: {game.score}"
    )
    if game.focus_index % 3 == 0:
        game.current_board().ui_border_top = graphics.GREEN_SQUARE
        game.current_board().ui_border_bottom = graphics.GREEN_SQUARE
        game.current_board().ui_border_left = graphics.GREEN_SQUARE
        game.current_board().ui_border_right = graphics.GREEN_SQUARE
    else:
        game.current_board().ui_border_top = graphics.WHITE_SQUARE
        game.current_board().ui_border_bottom = graphics.WHITE_SQUARE
        game.current_board().ui_border_left = graphics.WHITE_SQUARE
        game.current_board().ui_border_right = graphics.WHITE_SQUARE
    game.display_board()
    # Cells pool box
    draw_box(
        game,
        2,
        game.current_board().width * 2 + 6,
        20,
        15,
        game.focus_index % 3 == 1,
        "CELL POOL",
    )
    for i in range(0, len(game.available_cells)):
        scr.display_at(
            game.available_cells[i],
            int(i / 3) * 2 + 4,
            game.current_board().width * 2 + 6 + i % 3 * 4 + 2,
        )
        if i == game.cell_index % len(game.available_cells):
            scr.display_at(
                base.Text.green_bright(
                    graphics.GeometricShapes.BLACK_LOWER_RIGHT_TRIANGLE
                ),
                int(i / 3) * 2 + 3,
                game.current_board().width * 2 + 6 + i % 3 * 4 + 1,
            )
            scr.display_at(
                base.Text.green_bright(
                    graphics.GeometricShapes.BLACK_LOWER_LEFT_TRIANGLE
                ),
                int(i / 3) * 2 + 3,
                game.current_board().width * 2 + 6 + i % 3 * 4 + 4,
            )
            scr.display_at(
                base.Text.green_bright(
                    graphics.GeometricShapes.BLACK_UPPER_RIGHT_TRIANGLE
                ),
                int(i / 3) * 2 + 5,
                game.current_board().width * 2 + 6 + i % 3 * 4 + 1,
            )
            scr.display_at(
                base.Text.green_bright(
                    graphics.GeometricShapes.BLACK_UPPER_LEFT_TRIANGLE
                ),
                int(i / 3) * 2 + 5,
                game.current_board().width * 2 + 6 + i % 3 * 4 + 4,
            )

    # Commands box
    draw_box(
        game,
        22,
        game.current_board().width * 2 + 6,
        12,
        15,
        game.focus_index % 3 == 2,
        "COMMANDS",
    )
    color = f"{base.Style.BRIGHT}{base.Fore.WHITE}{base.Back.GREEN}"
    end_color = f"{base.Style.RESET_ALL}"
    scr.display_at(
        f"{color if game.cmds_focus_index%4 == 0 else ''}ENCODE{end_color if game.cmds_focus_index%4 == 0 else ''}",
        24,
        game.current_board().width * 2 + 10,
    )
    scr.display_at(
        f"{color if game.cmds_focus_index%4 == 1 else ''}RUN{end_color if game.cmds_focus_index%4 == 1 else ''}",
        26,
        game.current_board().width * 2 + 11,
    )
    scr.display_at(
        f"{color if game.cmds_focus_index%4 == 2 else ''}RESET{end_color if game.cmds_focus_index%4 == 2 else ''}",
        28,
        game.current_board().width * 2 + 10,
    )
    scr.display_at(
        f"{color if game.cmds_focus_index%4 == 3 else ''}QUIT{end_color if game.cmds_focus_index%4 == 3 else ''}",
        30,
        game.current_board().width * 2 + 11,
    )

    if game.current_level > 0:
        print(game.terminal.clear_eos)
        cc = game.available_cells[game.cell_index % len(game.available_cells)]
        dl = []
        for i in cc.actuator.moveset:
            dl.append(constant_to_string(i))
        scr.display_line(
            f"\n {cc} Lifespan: {cc.initial_lifespan}\n Note: {cc.note}\n Chord: {cc.chord}\n Directions: {', '.join(dl)}"
        )
    print(game.terminal.clear_eos)


def pickup(params):
    game = params[0]
    gene = params[1]
    gene.sprixel.fg_color = game.terminal.color_rgb(255, 0, 0)
    o = life.Organism(cells=[life.Cell(multi_color=False, color1=gene.color)])
    o.actuator = actuators.RandomActuator(moveset=gene.directions)
    o.actuator.pause()
    game.available_cells.append(o)
    game.score += 50
    if len(game.available_cells) > 24:
        game.available_cells = game.available_cells[len(game.available_cells) - 24 :]
    game.current_board().remove_item(gene)


game = engine.Game(
    mode=constants.MODE_RT,
    user_update=update,
    input_lag=difficulties[current_difficulty],
)
game.sprites = None
game.player = board_items.Player(
    sprixel=core.Sprixel("[]", "", game.terminal.color_rgb(255, 255, 255))
)
game.wave_index = 0
game.available_cells = []
o = life.Organism(
    cells=[life.Cell(multi_color=False, color1=media.Color(255, 0, 0))],
    note=media.Note("C"),
)
o.actuator = actuators.RandomActuator(moveset=[constants.UP])
o.actuator.pause()
game.available_cells.append(o)
o = life.Organism(
    cells=[life.Cell(multi_color=False, color1=media.Color(0, 255, 0))],
    note=media.Note("D"),
)
o.actuator = actuators.RandomActuator(moveset=[constants.DOWN])
o.actuator.pause()
game.available_cells.append(o)
o = life.Organism(
    cells=[life.Cell(multi_color=False, color1=media.Color(0, 0, 255))],
    note=media.Note("E"),
)
o.actuator = actuators.RandomActuator(moveset=[constants.LEFT])
o.actuator.pause()
game.available_cells.append(o)
o = life.Organism(
    cells=[life.Cell(multi_color=False, color1=media.Color(255, 0, 255))],
    note=media.Note("F"),
)
o.actuator = actuators.RandomActuator(moveset=[constants.RIGHT])
o.actuator.pause()
game.available_cells.append(o)


game.enable_partial_display = False
game.current_state = "title_screen"
game.cleanup_timer = 0
game.score = 0

k = ""
while game.screen.width < 145 or game.screen.height < 42:
    game.clear_screen()
    if k == "q":
        game.stop()
        break
    print(
        base.Text.red_bright(
            f"This simulation requires a terminal size of 145 columns and 42 lines.\n"
            f"Your current terminal size is {game.screen.width} (columns) by"
            f" {game.screen.height} (rows).\n\n"
            "Please resize your terminal and press any key.\n\n"
            "To quit press 'q'.\n\n"
        )
    )
    k = game.get_key()

goto_level(game, 1)
while game.state != constants.STOPPED:
    if game.current_state == "title_screen":
        title_screen(game)
    elif game.current_state == "game":
        game.run()
    elif game.current_state == "credits":
        credits_screen(game)
    elif game.current_state == "tutorial":
        tutorial(game)

