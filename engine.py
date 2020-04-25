import tcod
import tcod.console
import tcod.event

from input_handlers import handle_keys
from entity import Entity
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    colours = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150)
    }

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(screen_width, screen_height, 'tcod tutorial part 2', vsync=True)
    con = tcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', tcod.white)
    npc = Entity(int(screen_width / 2) - 5, int(screen_height / 2) - 5, '!', tcod.yellow)
    entities = [npc, player]

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

        # exit
        if key.vk == tcod.KEY_ESCAPE:
            return True

        # draw to screen
        render_all(con, entities, game_map, screen_width, screen_height, colours)
        tcod.console_flush()
        clear_all(con, entities)


if __name__ == '__main__':
    main()
