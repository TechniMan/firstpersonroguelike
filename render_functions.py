import tcod


# Draw all entities in the list
def render_all(con, entities, game_map, screen_width, screen_height, colours):
    # Draw all the tiles in the game map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                tcod.console_set_char_background(con, x, y, colours.get('dark_wall'), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(con, x, y, colours.get('dark_ground'), tcod.BKGND_SET)

    for entity in entities:
        draw_entity(con, entity)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    tcod.console_set_default_foreground(con, entity.colour)
    tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


# erase the character that represents this object
def clear_entity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
