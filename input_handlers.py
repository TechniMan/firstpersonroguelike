import tcod
import tcod.event


def handle_keys(key):
    if key.scancode == tcod.event.SCANCODE_ESCAPE:
        return {'exit': True}

    # Movement keys
    if key.sym == 'w' or key.scancode == tcod.event.SCANCODE_KP_8:
        return {'move': (0, -1)}
    elif key.sym == 's' or key.scancode == tcod.event.SCANCODE_KP_2:
        return {'move': (0, 1)}
    elif key.sym == 'a' or key.scancode == tcod.event.SCANCODE_KP_4:
        return {'move': (-1, 0)}
    elif key.sym == 'd' or key.scancode == tcod.event.SCANCODE_KP_6:
        return {'move': (1, 0)}
    elif key.sym == 'q' or key.scancode == tcod.event.SCANCODE_KP_7:
        return {'move': (-1, -1)}
    elif key.sym == 'e' or key.scancode == tcod.event.SCANCODE_KP_9:
        return {'move': (1, -1)}
    elif key.sym == 'z' or key.scancode == tcod.event.SCANCODE_KP_1:
        return {'move': (-1, 1)}
    elif key.sym == 'c' or key.scancode == tcod.event.SCANCODE_KP_3:
        return {'move': (1, 1)}

    # No key was pressed
    return {}
