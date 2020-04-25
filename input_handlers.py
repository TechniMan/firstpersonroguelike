import tcod as libtcod


def handle_keys(key):
    # Exit the game
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    # Alt+Enter: toggle full screen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # Movement keys
    if key.vk == libtcod.KEY_UP or key.vk == 'W':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key.vk == 's':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key.vk == 'a':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key.vk == 'd':
        return {'move': (1, 0)}

    # No key was pressed
    return {}
