import math
from PIL import Image
import tcod
import tcod.console
import tcod.event
from time import perf_counter

from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import clear_all, render_viewport, render_map, render_panel, render_menu
from map_objects.game_map import GameMap, RenderOrder
from game_states import GameStates
from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from game_messages import Message, MessageLog
from components.inventory import Inventory


def main():
    # map vars
    map_width = 40
    map_height = 60
    room_min_size = 6
    room_max_size = 10
    max_rooms = 50
    max_monsters_per_room = 3
    max_items_per_room = 2

    # screen vars
    viewport_width = 80
    viewport_height = 60
    rerender_viewport = True
    map_x = viewport_width
    map_y = 0

    screen_width = viewport_width + map_width

    # stats panel vars
    bar_width = 20
    panel_width = screen_width
    panel_height = 8
    panel_x = 0
    panel_y = viewport_height
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    screen_height = viewport_height + panel_height

    # fov vars
    fov_algorithm = 12
    fov_light_walls = True
    fov_radius = 10
    fov_recompute = True

    # game vars
    game_state = GameStates.PLAYER_TURN
    previous_game_state = game_state
    colours = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    # init player
    fighter_component = Fighter(30, 2, 5)
    inventory_component = Inventory(26)
    player = Entity(0, 0, '@', tcod.white, 'Player', render_order=RenderOrder.ACTOR, blocks=True,
                    fighter=fighter_component, inventory=inventory_component)
    player_rot = 0.0
    entities = [player]

    # load assets
    wall_texture = Image.open('assets/wall_vines0.png')
    orc_texture = Image.open('assets/orc.png')
    troll_texture = Image.open('assets/troll.png')
    potion_texture = Image.open('assets/ruby.png')

    # init game map
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
                      max_monsters_per_room, max_items_per_room, orc_texture, troll_texture, potion_texture)
    game_map.recompute_fov(player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

    # init message log
    message_log = MessageLog(message_x, message_width, message_height)

    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    with tcod.console_init_root(screen_width, screen_height, 'firstpersonroguelike', vsync=True) as root_console:
        viewport_console = tcod.console.Console(viewport_width, viewport_height)
        map_console = tcod.console.Console(map_width, map_height)
        panel_console = tcod.console.Console(panel_width, panel_height)

        mouse = (0, 0)
        time_start = perf_counter()

        # game loop begin
        while True:
            for event in tcod.event.wait():
                tcod.console_flush()

                player_turn_results = []

                # handle inputs
                if event.type == "QUIT":
                    raise SystemExit()
                elif event.type == "MOUSEMOTION":
                    # record the new mouse position, render_all will take care of the rest
                    mouse = event.tile
                # player keyboard interaction
                elif event.type == "KEYDOWN":
                    action = handle_keys(event, game_state)

                    if len(action) == 0:
                        continue

                    elif action.get('exit'):
                        if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                            game_state = previous_game_state
                        else:
                            raise SystemExit()

                    elif action.get('pickup') and game_state is GameStates.PLAYER_TURN:
                        for entity in entities:
                            if entity.item and entity.x == player.x and entity.y == player.y:
                                pickup_results = player.inventory.add_item(entity)
                                player_turn_results.extend(pickup_results)
                                break
                        else:
                            message_log.add_message(Message('You inspect the empty ground below you. Looks pretty dirty', tcod.yellow))
                        game_state = GameStates.ENEMIES_TURN

                    elif action.get('show_inventory') and game_state is GameStates.PLAYER_TURN:
                        previous_game_state = game_state
                        game_state = GameStates.SHOW_INVENTORY

                    elif action.get('drop_inventory') and game_state is GameStates.PLAYER_TURN:
                        previous_game_state = game_state
                        game_state = GameStates.DROP_INVENTORY

                    elif action.get('inventory_index') is not None and previous_game_state is not GameStates.PLAYER_DEAD:
                        inventory_index = action.get('inventory_index')
                        if inventory_index < len(player.inventory.items):
                            item = player.inventory.items[inventory_index]
                            if game_state is GameStates.SHOW_INVENTORY:
                                message_log.add_message(Message('Used ' + item.name))
                                player_turn_results.extend(player.inventory.use_item(item))
                            elif game_state is GameStates.DROP_INVENTORY:
                                message_log.add_message(Message('Dropped ' + item.name))
                                player_turn_results.extend(player.inventory.drop_item(item))
                            game_state = GameStates.ENEMIES_TURN

                    elif action.get('move') and game_state is GameStates.PLAYER_TURN:
                        dx, dy = action.get('move')
                        to_x, to_y = player.x + dx, player.y + dy
                        if game_map.walkable(to_x, to_y):
                            target = get_blocking_entities_at_location(entities, to_x, to_y)
                            if target:
                                player_turn_results.extend(player.fighter.attack(target))
                            else:
                                player.move(dx, dy)
                                fov_recompute = True
                            # end our turn
                            game_state = GameStates.ENEMIES_TURN

                    elif action.get('move2') and game_state is GameStates.PLAYER_TURN:
                        to_x = player.x
                        to_y = player.y
                        if action.get('move2') == 'forward':
                            to_x += int(math.sin(player_rot) * 1.5)
                            to_y += int(math.cos(player_rot) * 1.5)
                        elif action.get('move2') == 'rearward':
                            to_x -= int(math.sin(player_rot) * 1.5)
                            to_y -= int(math.cos(player_rot) * 1.5)

                        if game_map.walkable(to_x, to_y):
                            target = get_blocking_entities_at_location(entities, to_x, to_y)
                            if target:
                                player_turn_results.extend(player.fighter.attack(target))
                            else:
                                player.x = to_x
                                player.y = to_y
                                fov_recompute = True
                            # end our turn
                            game_state = GameStates.ENEMIES_TURN

                    elif action.get('turn') and game_state is GameStates.PLAYER_TURN:
                        dir = action.get('turn')
                        if dir == 'left':
                            player_rot += math.pi / 4.0
                        elif dir == 'right':
                            player_rot -= math.pi / 4.0
                        rerender_viewport = True
                # end_switch event.type

                # process player's turn results
                for ptr in player_turn_results:
                    message = ptr.get('message')
                    dead_entity = ptr.get('dead')

                    if message:
                        message_log.add_message(message)
                    if dead_entity:
                        if dead_entity == player:
                            message, game_state = kill_player(player)
                        else:
                            message = kill_monster(dead_entity)
                        message_log.add_message(message)
                    if ptr.get('item_added'):
                        entities.remove(ptr.get('item_added'))
                    if ptr.get('item_dropped'):
                        entities.append(ptr.get('item_dropped'))
                # end_for player_turn_results

                # run the enemy turn
                if game_state is GameStates.ENEMIES_TURN:
                    for entity in entities:
                        if entity.ai:
                            enemy_turn_results = entity.ai.take_turn(player, game_map, entities)

                            for etr in enemy_turn_results:
                                message = etr.get('message')
                                dead_entity = etr.get('dead')

                                if message:
                                    message_log.add_message(message)
                                if dead_entity:
                                    if dead_entity is player:
                                        message, game_state = kill_player(player)
                                    else:
                                        message = kill_monster(dead_entity)
                                    message_log.add_message(message)
                                    if game_state is GameStates.PLAYER_DEAD:
                                        break
                            if game_state is GameStates.PLAYER_DEAD:
                                break
                    else:
                        game_state = GameStates.PLAYER_TURN
                # endif enemy turn

                if fov_recompute:
                    game_map.recompute_fov(player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

                # draw each part of the screen
                render_viewport(root_console, viewport_console, 0, 0, viewport_width, viewport_height, game_map,
                                entities, colours, player.x, player.y, player_rot, fov_radius,
                                rerender_viewport or game_state is GameStates.ENEMIES_TURN,
                                wall_texture)
                render_map(root_console, map_console, game_map, entities, map_x, map_y, colours, fov_recompute)
                # TODO: extend render_menu to accept a top-left co-ordinate (start_x, start_y)
                render_menu(root_console, player, screen_width, screen_height, game_state)

                fps = 1.0 / (perf_counter() - time_start)
                render_panel(root_console, panel_console, entities, player, game_map, message_log, bar_width,
                             panel_width, panel_height, panel_x, panel_y, mouse, fps)
                time_start = perf_counter()

                tcod.console_flush()
                clear_all(map_console, entities)
                fov_recompute = False


if __name__ == '__main__':
    main()
