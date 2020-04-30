import tcod
import tcod.console

from components.inventory import Inventory


def menu(root: tcod.console.Console, header: str, options: list, width: int,
         screen_width: int, screen_height: int):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options')

    # calculate total height for header (after auto-wrap) and one line per option
    header_height = root.get_height_rect(0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tcod.console.Console(width, height)
    window.default_bg = tcod.black

    # print the header, with auto-wrap
    window.default_fg = tcod.white
    window.print_rect(0, 0, width, height, header, tcod.BKGND_NONE, tcod.LEFT)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option in options:
        text = '(' + chr(letter_index) + ') ' + option
        window.print_(0, y, text, tcod.BKGND_NONE, tcod.LEFT)
        y += 1
        letter_index += 1

    # blit the contents of 'window' to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    window.blit(root, x, y, 0, 0, width, height, 1.0, 0.7)


def inventory_menu(root: tcod.console.Console, header: str, inventory: Inventory,
                   inventory_width: int, screen_width: int, screen_height: int) -> None:
    """
    Show a menu with each item of the inventory as an option
    :param root: The root console
    :param con: The main console
    :param header: The header text
    :param inventory: The inventory to show
    :param inventory_width: How wide to show the menu
    :param screen_width: Width of the screen
    :param screen_height: Height of the screen
    :return None
    """
    if len(inventory.items) == 0:
        options = ['Inventory is empty']
    else:
        options = [item.name for item in inventory.items]
    menu(root, header, options, inventory_width, screen_width, screen_height)
