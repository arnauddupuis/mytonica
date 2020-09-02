from pygamelib import engine, base, board_items, constants, actuators
from pygamelib.assets import graphics
import simpleaudio as sa
import sys
import os
import time
import copy
from game import life, media

wave_obj = list()
# Get current working directory
wd = ""
try:
    wd = sys._MEIPASS
except AttributeError:
    wd = os.getcwd()

wave_obj.append(sa.WaveObject.from_wave_file(os.path.join(wd, "sfx", "sound_01.wav")))
wave_obj.append(sa.WaveObject.from_wave_file(os.path.join(wd, "sfx", "sound_02.wav")))


def load_sounds(g):
    pass


def title_screen(g):
    with g.terminal.cbreak(), g.terminal.hidden_cursor(), (g.terminal.fullscreen()):
        k = None
        while True:
            if k == "q":
                break
            elif k == engine.key.ENTER:
                g.current_state = "game"
                break
            g.clear_screen()
            g.screen.display_at(base.Text.magenta_bright("#oldCodeJam2020"), 2, 0)
            g.screen.display_at(
                "Mytonica", int((g.screen.height - 1) / 2), int(g.screen.width / 2) - 4
            )
            g.screen.display_at(
                base.Text.green_bright("build with pygamelib"),
                g.screen.height - 1,
                g.screen.width - 20,
            )
            k = g.get_key()


# I'm forced to write that function, it means that we need a hook to actuate functions
# in the pygamelib to process specific data.
def update_life(game, elapsed_time):
    if game.state == constants.RUNNING:
        if game.current_level in game._boards.keys():
            for idx in range(len(game.life_pool) - 1, 0, -1):
                npc = game.life_pool[idx]
                if npc.lifespan <= 0:
                    try:
                        game.current_board().remove_item(npc)
                    except base.PglException:
                        pass
                    else:
                        del game.life_pool[idx]
                if npc.actuator.state == constants.RUNNING:
                    # Account for movement speed
                    npc.dtmove += elapsed_time
                    if (
                        game.mode == constants.MODE_RT
                        and npc.dtmove < npc.movement_speed
                    ):
                        continue
                    # Since version 1.2.0 horizontal and vertical movement
                    # amplitude can be different so we proceed in 2 steps:
                    #  1 - build a unit direction vector
                    #  2 - use its component to build a movement vector
                    d = base.Vector2D.from_direction(npc.actuator.next_move(), 1)
                    game._boards[game.current_level]["board"].move(
                        npc,
                        base.Vector2D(
                            d.row * npc.step_vertical, d.column * npc.step_horizontal,
                        ),
                    )
                    npc.lifespan -= 1


def update(game, inkey, elapsed_time):
    if inkey == engine.key.UP:
        wave_obj[game.wave_index % 2].play()
        game.wave_index += 1
        game.move_player(constants.UP, 1)
    elif inkey == engine.key.DOWN:
        wave_obj[game.wave_index % 2].play()
        game.wave_index += 1
        game.move_player(constants.DOWN, 1)
    elif inkey == engine.key.LEFT:
        wave_obj[game.wave_index % 2].play()
        game.wave_index += 1
        game.move_player(constants.LEFT, 1)
    elif inkey == engine.key.RIGHT:
        wave_obj[game.wave_index % 2].play()
        game.wave_index += 1
        game.move_player(constants.RIGHT, 1)
    elif inkey == "q":
        game.stop()
    elif inkey == engine.key.SPACE:
        o = copy.deepcopy(
            game.available_cells[game.cell_index % len(game.available_cells)]
        )
        o.actuator = actuators.RandomActuator(
            moveset=[constants.UP, constants.DOWN, constants.LEFT, constants.RIGHT,]
        )
        game.current_board().place_item(
            o, game.player.row, game.player.column,
        )
        game.life_pool.append(o)
    elif inkey == engine.key.F1:
        game.cell_index += 1
    update_life(game, elapsed_time)
    game.display_board()
    game.screen.display_line(
        f"Cell: {game.available_cells[game.cell_index % len(game.available_cells)]}"
    )
    game.screen.display_line(f"Population: {len(game.life_pool)}")
    print(f"vp:  {game.partial_display_viewport} gpos: {game.player.pos}")


game = engine.Game(mode=constants.MODE_RT, user_update=update)
game.player = board_items.Player(model=graphics.Models.MAGE)
game.wave_index = 0
game.life_pool = list()
game.available_cells = [
    life.Organism(cells=[life.Cell(multi_color=False, color1=media.Color(255, 0, 0))]),
    life.Organism(cells=[life.Cell(multi_color=False, color1=media.Color(0, 255, 0))]),
    life.Organism(cells=[life.Cell(multi_color=False, color1=media.Color(0, 0, 255))]),
]
game.cell_index = 0
game.enable_partial_display = False
game.partial_display_viewport = [
    int((game.screen.width) / 2),
    int((game.screen.height - 5) / 2),
]
game.current_state = "title_screen"


b = engine.Board(
    size=[60, 30],
    DISPLAY_SIZE_WARNING=False,
    ui_borders=graphics.WHITE_SQUARE,
    ui_board_void_cell=graphics.BLACK_SQUARE,
)
for k in range(5, 29):
    b.place_item(life.Cell(), k, k)

b.place_item(life.Organism(cells=[b.item(5, 5), b.item(6, 6)]), 5, 10)
b.place_item(
    life.Organism(cells=[[b.item(7, 7), b.item(8, 8)], [b.item(9, 9), b.item(18, 18)]]),
    5,
    30,
)

game.add_board(1, b)
game.change_level(1)

while game.state != constants.STOPPED:
    if game.current_state == "title_screen":
        title_screen(game)
    elif game.current_state == "game":
        game.run()

