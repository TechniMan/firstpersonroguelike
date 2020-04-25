import tcod


# Draw all entities in the list
def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colours):
    # Draw all the tiles in the game map
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                # if tile can be seen now, light it up
                if visible:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colours.get('light_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colours.get('light_ground'), tcod.BKGND_SET)
                    # remember we've seen this tile
                    game_map.tiles[x][y].explored = True

                # if we've previously seen this tile
                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(con, x, y, colours.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, colours.get('dark_ground'), tcod.BKGND_SET)

    for entity in entities:
        draw_entity(con, entity, fov_map)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        tcod.console_set_default_foreground(con, entity.colour)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)


# erase the character that represents this object
def clear_entity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
