# A generic object to represent players, enemies, items, etc.
class Entity:
    def __init__(self, x, y, char, colour, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.name = name
        self.blocks = blocks

    # Move the entity by a given amount
    def move(self, dx, dy):
        self.x += dx
        self.y += dy


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
