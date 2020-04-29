import math
import numpy
from enum import Enum


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


# returns an array of all True with False in place of entities
def get_walkable_map_from_blocking_entities(entities, width, height):
    map = numpy.ones((height, width), dtype=bool)
    for entity in entities:
        if entity.blocks and entity.ai:
            map[entity.y, entity.x] = False
    return map


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None


# A generic object to represent players, enemies, items, etc.
class Entity:
    def __init__(self, x, y, char, colour, name, render_order=RenderOrder.CORPSE, blocks=False, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai
        self.render_order = render_order
        if fighter:
            self.fighter.owner = self
        if ai:
            self.ai.owner = self

    # Move the entity by a given amount
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round((dx / distance) * 1.2))
        dy = int(round((dy / distance) * 1.2))

        if game_map.walkable(self.x + dx, self.y + dy) and not get_blocking_entities_at_location(entities, self.x + dx, self.y + dy):
            self.move(dx, dy)

    def move_astar(self, target, game_map, entities):
        next_x, next_y = game_map.next_move(self, target, entities)
        if next_x and next_y:
            self.move_to(next_x, next_y)
        else:
            self.move_towards(target.x, target.y, game_map, entities)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
