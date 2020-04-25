import tcod
import tcod.console
import tcod.event

from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap
from fov_functions import initialise_fov, recompute_fov
from game_states import GameStates


def main():
    screen_width = 80
    screen_height = 50
    # map vars
    map_width = 80
    map_height = 45
    room_min_size = 6
    room_max_size = 10
    max_rooms = 30
    max_monsters_per_room = 3
    # fov vars
    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    fov_recompute = True
    # game vars
    game_state = GameStates.PLAYER_TURN

    colours = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    with tcod.console_init_root(screen_width, screen_height, 'tcod tutorial part 2', vsync=True) as root_console:
        con = tcod.console.Console(screen_width, screen_height)

        player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True)
        entities = [player]

        game_map = GameMap(map_width, map_height)
        game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height,
                          player, entities, max_monsters_per_room)
        fov_map = initialise_fov(game_map)

        key = tcod.Key()
        mouse = tcod.Mouse()

        while True:
            tcod.console_flush()

            # handle inputs
            tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
            action = handle_keys(key)

            if action.get('exit'):
                break
            elif action.get('fullscreen'):
                tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
            elif action.get('move') and game_state == GameStates.PLAYER_TURN:
                dx, dy = action.get('move')
                to_x, to_y = player.x + dx, player.y + dy
                if not game_map.is_blocked(to_x, to_y):
                    target = get_blocking_entities_at_location(entities, to_x, to_y)
                    if target:
                        print('You kick the ' + target.name + ' in the shins, much to its chagrin!')
                    else:
                        player.move(dx, dy)
                        fov_recompute = True
                    # end our turn
                    game_state = GameStates.ENEMIES_TURN
            elif game_state == GameStates.ENEMIES_TURN:
                for entity in entities:
                    if entity == player:
                        continue
                    print('The ' + entity.name + ' ponders... why are we here?')
                game_state = GameStates.PLAYER_TURN

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
