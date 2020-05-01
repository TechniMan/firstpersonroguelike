import math
# from PIL import Image
import tcod
import tcod.color
import tcod.console

from entity import Entity, get_first_entity_at_location
from map_objects.game_map import GameMap
from game_messages import MessageLog
from game_states import GameStates
from menus import inventory_menu


def old_lerp(a: float, b: float, t: float) -> float:
    return (t - a) / (b - a)


def slerp_float(a: float, b: float, t: float) -> float:
    """
    Returns curved value of how far t is from a relative to b
    """
    x = a + t * (b - a)
    return x / b


# render the 3D viewport
def render_viewport(root_console: tcod.console.Console, viewport_console: tcod.console.Console, viewport_x: int,
                    viewport_y: int, viewport_width: int, viewport_height: int, game_map: GameMap, entities: list,
                    colours: dict, player_x: float, player_y: float, player_rot: float, fov_radius: int,
                    rerender: bool, wall_texture):
    """
    Raycasting algorithm based on javidx9's excellent YouTube video, 'Code-It-Yourself! First Person Shooter (Quick and Simple C++)'

    """
    if rerender:
        texture_width = 32
        # pi/4 rad = 45 deg (pi/3=60, pi/2=90, pi=180)
        fov = math.pi / 3.0
        cam_x = player_x + 0.5
        cam_y = player_y + 0.5
        ground_colour = colours.get('light_ground')
        wall_colour = colours.get('light_wall')
        viewport_console.clear()

        for x in range(viewport_width):
            # render a column based on raycasting
            ray_angle = (player_rot - fov / 2.0) + (x / float(viewport_width)) * fov
            eye_x = math.sin(ray_angle)
            eye_y = math.cos(ray_angle)

            distance_to_wall = 0.0
            hit_wall = False
            hit_wall_corner = False
            distance_to_entity = 0.0
            hit_entity = False
            entity = None
            wall_x = 0.0

            while not hit_wall and distance_to_wall < fov_radius:
                distance_to_wall += 0.1
                if not hit_entity:
                    distance_to_entity += 0.1
                test_x = int(cam_x + eye_x * distance_to_wall)
                test_y = int(cam_y + eye_y * distance_to_wall)

                # if outside of game map
                if test_x < 0 or test_x >= game_map.width or test_y < 0 or test_y >= game_map.height:
                    hit_wall = True
                    distance_to_wall = fov_radius
                # else
                else:
                    # can we see an entity
                    if not hit_entity:
                        entities_in_render_order = sorted(entities, key=lambda e: 4 - e.render_order.value)
                        e = get_first_entity_at_location(entities_in_render_order, test_x, test_y)
                        if e is not None:
                            hit_entity = True
                            entity = e
                    # have we hit a wall yet
                    if not game_map.walkable(test_x, test_y):
                        hit_wall = True

                        # where on the wall have we hit?
                        #vy = float(test_y - cam_y)
                        #vx = float(test_x - cam_x)
                        #mag = math.sqrt(vx**2 + vy**2)
                        #dot = (eye_x * vx / mag) + (eye_y * vy / mag)
                        #wall_x = math.acos(dot)
            # end_while

            ceiling = float(viewport_height / 2.0) - viewport_height / float(distance_to_wall)
            floor = viewport_height - ceiling
            wall_brightness = 1.0 - slerp_float(0, fov_radius, distance_to_wall / fov_radius)
            out_of_view = distance_to_wall >= fov_radius
            x_cell = viewport_width - x - 1
            half_viewport_height = viewport_height / 2
            for y in range(viewport_height):
                if y < ceiling:
                    brightness = 1.0 - slerp_float(0, half_viewport_height, y / half_viewport_height)
                    tcod.console_set_char_background(viewport_console, x_cell, y,
                                                     wall_colour * brightness, tcod.BKGND_SET)
                elif y < floor:
                    if out_of_view:
                        tcod.console_set_char_background(viewport_console, x_cell, y, tcod.black, tcod.BKGND_SET)
                    else:
                        #u = int(wall_x * texture_width)
                        #v = int(((y - ceiling) / (floor - ceiling)) * texture_width)
                        #pixel = wall_texture.getpixel((u, v))
                        #tex_col = (int(pixel[0] * wall_brightness), int(pixel[1] * wall_brightness),
                                   #int(pixel[2] * wall_brightness))
                        #tcod.console_set_char_background(viewport_console, x_cell, y, tex_col, tcod.BKGND_SET)
                        tcod.console_set_char_background(viewport_console, x_cell, y, wall_colour * wall_brightness, tcod.BKGND_SET)
                else:
                    brightness = slerp_float(half_viewport_height, viewport_height, (y - half_viewport_height) / half_viewport_height)
                    tcod.console_set_char_background(viewport_console, x_cell, y, ground_colour * brightness, tcod.BKGND_SET)

            # did we find an entity
            if False and entity:
                start = int(float(viewport_height / 2.0) - viewport_height / float(distance_to_entity))
                height = viewport_height - start - start
                viewport_console.draw_rect(x_cell, start, 1, height, ord(entity.char), entity.colour)
        # end_for x
    viewport_console.blit(root_console, viewport_x, viewport_y, 0, 0, viewport_width, viewport_height)
    return


# render the map
def render_map(root_console: tcod.console.Console, map_console: tcod.console.Console, game_map: GameMap, entities: list,
               start_x: int, start_y: int, colours: dict, fov_recompute: bool):
    # render map tiles only when a change has occurred
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = game_map.fov(x, y)
                wall = not game_map.walkable(x, y)

                # if tile can be seen now, light it up
                if visible:
                    if wall:
                        tcod.console_set_char_background(map_console, x, y, colours.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(map_console, x, y, colours.get('light_ground'), tcod.BKGND_SET)
                # if we've previously seen this tile
                elif game_map.explored(x, y):
                    if wall:
                        tcod.console_set_char_background(map_console, x, y, colours.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(map_console, x, y, colours.get('dark_ground'), tcod.BKGND_SET)

    # render entities onto map
    entities_in_render_order = sorted(entities, key=lambda e: e.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(map_console, entity, game_map)

    # copy to the actual screen
    map_console.blit(root_console, start_x, start_y, 0, 0, game_map.width, game_map.height)
    return


# render panel
def render_panel(root_console: tcod.console.Console, panel_console: tcod.console.Console, entities: list,
                 player: Entity, game_map: GameMap, message_log: MessageLog, bar_width: int, panel_width: int,
                 panel_height: int, panel_x: int, panel_y: int, mouse: tuple):
    panel_console.default_bg = tcod.black
    panel_console.clear()

    # print message log
    y = 1
    for message in message_log.messages:
        panel_console.default_fg = message.colour
        panel_console.print_(message_log.x, y, message.text, tcod.BKGND_NONE, tcod.LEFT)
        panel_console.print(message_log.x, y, message.text, fg=message.colour, bg=message_log.bg,
                            bg_blend=tcod.BKGND_NONE, alignment=tcod.LEFT)
        y += 1

    render_bar(panel_console, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, tcod.red, tcod.darkest_red)

    panel_console.default_fg = tcod.light_grey
    panel_console.print_(1, 0, get_names_under_mouse(mouse, entities, game_map), tcod.BKGND_NONE, tcod.LEFT)

    panel_console.blit(root_console, panel_x, panel_y, 0, 0, panel_width, panel_height)
    return


# render a bar
def render_bar(panel: tcod.console.Console, x: int, y: int, total_width: int, name: str, value: int, maximum: int,
               bar_colour: tcod.color.Color, back_colour: tcod.color.Color):
    bar_width = int(float(value) / maximum * total_width)

    panel.default_bg = back_colour
    panel.rect(x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    panel.default_bg = bar_colour
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1, False, tcod.BKGND_SCREEN)
        panel.rect(x, y, bar_width, 1, False, tcod.BKGND_SCREEN)

    panel.default_fg = tcod.white
    panel.print_(int(x + total_width / 2), y, '{0}: {1}/{2}'.format(name, value, maximum), tcod.BKGND_NONE, tcod.CENTER)
    return


# get names of entities under the current cursor position
def get_names_under_mouse(mouse, entities, game_map):
    (x, y) = mouse

    names = [entity.name for entity in entities if entity.x == x and entity.y == y and game_map.fov(entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


# render menu
def render_menu(root: tcod.console.Console, player: Entity, screen_width: int, screen_height: int,
                game_state: GameStates):
    if game_state == GameStates.SHOW_INVENTORY:
        inventory_menu(root, 'Select an item to use', player.inventory, 50, screen_width, screen_height)
    elif game_state is GameStates.DROP_INVENTORY:
        inventory_menu(root, 'Select an item to drop', player.inventory, 50, screen_width, screen_height)
    return


# clear all entities from screen
def clear_all(con: tcod.console.Console, entities: list):
    for entity in entities:
        clear_entity(con, entity)
    return


# erase the character that represents this object
def clear_entity(con: tcod.console.Console, entity: Entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
    return


# render an entity
def draw_entity(con: tcod.console.Console, entity: Entity, game_map: GameMap):
    if game_map.fov(entity.x, entity.y):
        con.default_fg = entity.colour
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)
    return
