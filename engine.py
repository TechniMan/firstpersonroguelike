import tcod as libtcod
from input_handlers import handle_keys


def main():
    screen_width = 80
    screen_height = 50

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False)
    con = libtcod.console_new(screen_width, screen_height)

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        # handle inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if exit:
            break
        elif fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        elif move:
            dx, dy = move
            player_x += dx
            player_y += dy

        # exit
        if key.vk == libtcod.KEY_ESCAPE:
            return True

        # move the player *character*! geddit?
        if key.vk == libtcod.KEY_UP:
            player_y -= 1
        if key.vk == libtcod.KEY_DOWN:
            player_y += 1
        if key.vk == libtcod.KEY_LEFT:
            player_x -= 1
        if key.vk == libtcod.KEY_RIGHT:
            player_x += 1

        # draw to screen
        libtcod.console_clear(con)
        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_flush()


if __name__ == '__main__':
    main()
