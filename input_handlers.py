import tcod
import tcod.event

from game_states import GameStates


def handle_keys(key: tcod.event.KeyDown, game_state: GameStates):
    key_scancode = tcod.event.SCANCODE_F24
    if key.scancode:
        key_scancode = key.scancode

    key_sym = 'lol'
    if key.sym and key.sym < 0x110000:
        key_sym = chr(key.sym)

    if game_state is GameStates.PLAYER_TURN:
        return handle_player_turn_keys(key_sym, key_scancode)
    elif game_state is GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key_sym, key_scancode)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_menu_keys(key_sym, key_scancode)
    return {}


def handle_menu_keys(sym, scancode):
    if scancode is tcod.event.SCANCODE_ESCAPE:
        return {'exit': True}

    index = scancode - tcod.event.SCANCODE_A
    if 0 <= index < 26:
        return {'inventory_index': index}

    return {}


def handle_player_turn_keys(sym, scancode):
    if scancode is tcod.event.SCANCODE_ESCAPE:
        return {'exit': True}

    if scancode is tcod.event.SCANCODE_G:
        return {'pickup': True}
    elif scancode is tcod.event.SCANCODE_I:
        return {'show_inventory': True}
    elif scancode is tcod.event.SCANCODE_D:
        return {'drop_inventory': True}

    # Movement keys
    if scancode is tcod.event.SCANCODE_KP_8:
        return {'move': (0, -1)}
    elif scancode is tcod.event.SCANCODE_KP_2:
        return {'move': (0, 1)}
    elif scancode is tcod.event.SCANCODE_KP_4:
        return {'move': (-1, 0)}
    elif scancode is tcod.event.SCANCODE_KP_6:
        return {'move': (1, 0)}
    elif scancode is tcod.event.SCANCODE_KP_7:
        return {'move': (-1, -1)}
    elif scancode is tcod.event.SCANCODE_KP_9:
        return {'move': (1, -1)}
    elif scancode is tcod.event.SCANCODE_KP_1:
        return {'move': (-1, 1)}
    elif scancode is tcod.event.SCANCODE_KP_3:
        return {'move': (1, 1)}

    # No key was pressed
    return {}


def handle_player_dead_keys(sym, scancode):
    if scancode is tcod.event.SCANCODE_ESCAPE:
        return {'exit': True}

    if scancode is tcod.event.SCANCODE_I:
        return {'show_inventory': True}

    return {}
