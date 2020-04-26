import tcod


def handle_keys(key):
    # Exit the game
    if key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    # Alt+Enter: toggle full screen
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    key_char = chr(key.c)
    # Movement keys
    if key.vk == tcod.KEY_UP or key_char == 'w' or key.vk == tcod.KEY_KP8:
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN or key_char == 's' or key.vk == tcod.KEY_KP2:
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT or key_char == 'a' or key.vk == tcod.KEY_KP4:
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT or key_char == 'd' or key.vk == tcod.KEY_KP6:
        return {'move': (1, 0)}
    elif key_char == 'q' or key.vk == tcod.KEY_KP7:
        return {'move': (-1, -1)}
    elif key_char == 'e' or key.vk == tcod.KEY_KP9:
        return {'move': (1, -1)}
    elif key_char == 'z' or key.vk == tcod.KEY_KP1:
        return {'move': (-1, 1)}
    elif key_char == 'c' or key.vk == tcod.KEY_KP3:
        return {'move': (1, 1)}

    # No key was pressed
    return {}
