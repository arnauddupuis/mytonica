from pygamelib import engine, base, board_items, constants, actuators
from pygamelib.assets import graphics
from pygamelib.gfx import core
import simpleaudio as sa
import sys
import os
import time
import copy
import random
from game import life, media

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
    game.sprites = core.SpriteCollection.load_json_file("gfx/mytonica.spr")


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
    if game.state == constants.RUNNING:
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
                # TODO: change this to look for potential partners and select the best.
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
                    i = game.current_board().item(nr, nc)
                    # if (
                    #     not isinstance(i, board_items.BoardItemVoid)
                    #     and not isinstance(i, board_items.Player)
                    #     and not isinstance(i, life.GeneticMaterial)
                    # ):
                    # print(
                    #     f"Found a potential partner: {i} (self: {i == npc}) (time: {abs(i.timestamp - npc.timestamp)} {abs(i.timestamp - npc.timestamp) >= min_dt})"
                    # )
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
                                            game.life_pool.append(baby)
                                            game.current_board().place_item(
                                                baby, nr, nc
                                            )
                                            done = True
                                            break
                                    if done:
                                        break
                                if done:
                                    break
                        break
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
    game.life_pool.append(o)


def update(game, inkey, elapsed_time):
    game.cleanup_timer += elapsed_time
    # Take care of inputs
    ppos = game.player.pos
    dir_map = {
        engine.key.UP: constants.UP,
        engine.key.DOWN: constants.DOWN,
        engine.key.LEFT: constants.LEFT,
        engine.key.RIGHT: constants.RIGHT,
    }
    if inkey in dir_map:
        # wave_obj[game.wave_index % 2].play()
        # game.wave_index += 1
        game.move_player(dir_map[inkey], 1)
        if game.player_mode == "place":
            place_cell(game, ppos[0], ppos[1])
    elif inkey == "q":
        game.stop()
    elif inkey == "1" or inkey == "2" or inkey == "3":
        # c = None
        # if inkey == "1":
        #     c = media.Color(255, 0, 0)
        # elif inkey == "2":
        #     c = media.Color(0, 255, 0)
        # else:
        #     c = media.Color(0, 0, 255)
        # o = life.Organism(cells=[life.Cell(multi_color=False, color1=c)])
        o = copy.deepcopy(
            game.available_cells[game.cell_index % len(game.available_cells)]
        )
        o.timestamp = time.time()
        min_dir = 0
        max_dir = 5
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
        o.starting_position = game.player.pos
        o.actuator.pause()
        game.current_board().place_item(
            o, game.player.row, game.player.column,
        )
        game.life_pool.append(o)
    elif inkey == engine.key.SPACE:
        for c in game.life_pool:
            c.actuator.start()
    elif inkey == engine.key.PAGE_UP:
        game.cell_index += 1
    elif inkey == engine.key.PAGE_DOWN:
        game.cell_index -= 1
    elif inkey == engine.key.F1:
        game.player_mode = "move"
        game.player.sprixel.fg_color = game.terminal.color_rgb(255, 255, 255)
    elif inkey == engine.key.F2:
        game.player_mode = "place"
        game.player.sprixel.fg_color = game.terminal.color_rgb(0, 255, 0)
    elif inkey.name == "KEY_TAB":
        game.current_board().ui_border_top = graphics.GREEN_SQUARE
        game.current_board().ui_border_bottom = graphics.GREEN_SQUARE
        game.current_board().ui_border_left = graphics.GREEN_SQUARE
        game.current_board().ui_border_right = graphics.GREEN_SQUARE

    # Now update life
    update_life(game, elapsed_time)

    # Then display stuff
    redraw_screen(game)
    game.screen.display_line(f"FPS: {1/elapsed_time:2.2f}")

    # for npc in game.life_pool:
    #     game.screen.display_line(
    #         f"{npc} : {npc.lifespan} moveset: {npc.actuator.moveset}"
    #     )


def redraw_screen(game):
    game.screen.display_line(f"Mode: {game.player_mode}")
    game.display_board()
    game.screen.display_line(
        f"Cell: {game.available_cells[game.cell_index % len(game.available_cells)]}"
    )
    game.screen.display_line(f"Population: {len(game.life_pool)}")
    print(
        f"vp:  {game.partial_display_viewport} gpos: {game.player.pos} #movables: {len(game.current_board().get_movables())}"
    )
    if game.cleanup_timer > 5.0:
        clean_up(game)
        game.cleanup_timer = 0
    # for r in range(0, b.height):
    #     for c in range(0, b.width):
    #         i = b.item(r, c)
    #         if isinstance(i, life.Organism):
    #             game.screen.display_line(
    #                 f"{i} {type(i)} {i.lifespan} {i not in game.life_pool}"
    #             )

    print(game.terminal.clear_eos)


def pickup(params):
    game = params[0]
    gene = params[1]
    gene.sprixel.fg_color = game.terminal.color_rgb(255, 0, 0)


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
game.life_pool = list()
game.player_mode = "move"
game.available_cells = [
    life.Organism(cells=[life.Cell(multi_color=False, color1=media.Color(255, 0, 0))]),
    life.Organism(cells=[life.Cell(multi_color=False, color1=media.Color(0, 255, 0))]),
    life.Organism(cells=[life.Cell(multi_color=False, color1=media.Color(0, 0, 255))]),
]
o = life.Organism(
    cells=[life.Cell(multi_color=False, color1=media.Color(255, 0, 255))],
)
o.actuator = actuators.RandomActuator(moveset=[constants.RIGHT])
game.available_cells.append(o)
game.current_generation = {}
game.cell_index = 0
game.enable_partial_display = False
game.partial_display_viewport = [
    int((game.screen.width) / 2),
    int((game.screen.height - 5) / 2),
]
game.current_state = "title_screen"
game.cleanup_timer = 0

b = engine.Board(
    size=[60, 30],
    DISPLAY_SIZE_WARNING=False,
    ui_borders=graphics.WHITE_SQUARE,
    ui_board_void_cell=graphics.BLACK_SQUARE,
)
gene = life.GeneticMaterial(action=pickup, action_parameters=[game])
gene.action_parameters.append(gene)
b.place_item(gene, 5, 10)

game.add_board(1, b)
game.change_level(1)

while game.state != constants.STOPPED:
    if game.current_state == "title_screen":
        title_screen(game)
    elif game.current_state == "game":
        game.run()
        # game.start()
        # with game.terminal.cbreak():
        #     while game.state != constants.STOPPED:
        #         # in_key = game.get_key()
        #         in_key = game.terminal.inkey()
        #         elapsed = time.time() - game.previous_time
        #         game.previous_time = time.time()
        #         game.player.dtmove += elapsed
        #         update(game, in_key, elapsed)
    elif game.current_state == "credits":
        credits_screen(game)

