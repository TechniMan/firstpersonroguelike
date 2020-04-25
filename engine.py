import tcod
import tcod.console
import tcod.event

from input_handlers import handle_keys
from entity import Entity
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap
from fov_functions import initialise_fov, recompute_fov


def main():
    screen_width = 80
    screen_height = 50
    # map vars
    map_width = 80
    map_height = 45
    room_min_size = 6
    room_max_size = 10
    max_rooms = 30
    # fov vars
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    fov_recompute = True

    colours = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(screen_width, screen_height, 'tcod tutorial part 2', vsync=True)
    con = tcod.console.Console(screen_width, screen_height)

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.white)
    npc = Entity(int(screen_width / 2) - 5, int(screen_height / 2) - 5, '!', tcod.yellow)
    entities = [npc, player]

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)
    fov_map = initialise_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        # handle inputs
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if exit:
            break
        elif fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        elif move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
                fov_recompute = True

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        # exit
        if key.vk == tcod.KEY_ESCAPE:
            return True

        # draw to screen
        render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colours)
        fov_recompute = False
        tcod.console_flush()
        clear_all(con, entities)


if __name__ == '__main__':
    main()
