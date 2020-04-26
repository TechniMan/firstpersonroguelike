import tcod
from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


# Draw all entities in the list
def render_all(con, entities, player, game_map, fov_recompute, screen_width, screen_height, colours):
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

    tcod.console_set_default_foreground(con, tcod.white)
    tcod.console_print_ex(con, 1, screen_height - 2, tcod.BKGND_NONE, tcod.LEFT,
                          'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, game_map):
    if game_map.fov(entity.x, entity.y):
        tcod.console_set_default_foreground(con, entity.colour)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


# erase the character that represents this object
def clear_entity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
