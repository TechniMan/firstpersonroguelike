import tcod
import tcod.color
import tcod.console

from entity import Entity, RenderOrder
from map_objects.game_map import GameMap
from game_messages import MessageLog
from game_states import GameStates
from menus import inventory_menu


# Draw all entities in the list
def render_all(root: tcod.console.Console, con: tcod.console.Console, panel: tcod.console.Console, entities: list,
               player: Entity, game_map: GameMap, fov_recompute: bool, message_log: MessageLog, screen_width: int,
               screen_height: int, bar_width: int, panel_height: int, panel_y: int, mouse, colours: dict,
               game_state: GameStates):
    # Draw all the tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = game_map.fov(x, y)
                wall = not game_map.walkable(x, y)

                # if tile can be seen now, light it up
                if visible:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colours.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colours.get('light_ground'), tcod.BKGND_SET)
                # if we've previously seen this tile
                elif game_map.explored(x, y):
                    if wall:
                        tcod.console_set_char_background(con, x, y, colours.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colours.get('dark_ground'), tcod.BKGND_SET)

    entities_in_render_order = sorted(entities, key=lambda e: e.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map)

    con.blit(root, 0, 0, 0, 0, screen_width, screen_height)

    # PANEL #
    panel.default_bg = tcod.black
    panel.clear()

    # print message log
    y = 1
    for message in message_log.messages:
        panel.default_fg = message.colour
        panel.print_(message_log.x, y, message.text, tcod.BKGND_NONE, tcod.LEFT)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp, tcod.red, tcod.darkest_red)

    panel.default_fg = tcod.light_grey
    panel.print_(1, 0, get_names_under_mouse(mouse, entities, game_map), tcod.BKGND_NONE, tcod.LEFT)

    panel.blit(root, 0, panel_y, 0, 0, screen_width, panel_height)

    if game_state == GameStates.SHOW_INVENTORY:
        inventory_menu(root, con, 'Select an item to use', player.inventory, 50, screen_width, screen_height)
    elif game_state is GameStates.DROP_INVENTORY:
        inventory_menu(root, con, 'Select an item to drop', player.inventory, 50, screen_width, screen_height)


def clear_all(con: tcod.console.Console, entities: list):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con: tcod.console.Console, entity: Entity, game_map: GameMap):
    if game_map.fov(entity.x, entity.y):
        con.default_fg = entity.colour
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


def get_names_under_mouse(mouse, entities, game_map):
    (x, y) = mouse

    names = [entity.name for entity in entities if entity.x == x and entity.y == y and game_map.fov(entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


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


# erase the character that represents this object
def clear_entity(con: tcod.console.Console, entity: Entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
