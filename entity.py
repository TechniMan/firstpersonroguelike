# A generic object to represent players, enemies, items, etc.
class Entity:
    def __init__(self, x, y, char, colour):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour

    # Move the entity by a given amount
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
