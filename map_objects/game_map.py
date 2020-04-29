import tcod
import tcod.map
import tcod.path
import numpy
from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from map_objects.rectangle import Rectangle
from entity import Entity, get_walkable_map_from_blocking_entities
from render_functions import RenderOrder
from item_functions import heal


# Container class for a tcod.map.Map and extras
class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = tcod.map.Map(width, height)
        self.initialise_map()
        self.explored_tiles = numpy.zeros((height, width), dtype=bool, order='F')
        self.astar = tcod.path.AStar(self.map.walkable)

    # initialise map to be filled in
    def initialise_map(self):
        self.map.transparent[:] = False
        self.map.walkable[:] = False

    # recalculate player's fov and update explored tiles
    def recompute_fov(self, x, y, radius, light_walls=True, algorithm=tcod.FOV_RESTRICTIVE):
        self.map.compute_fov(x, y, radius, light_walls, algorithm)
        self.explored_tiles |= self.map.fov

    # find the next cell to move to
    def next_move(self, entity, target, entities):
        result = None, None

        ents = get_walkable_map_from_blocking_entities(entities, self.width, self.height)
        ents[entity.y, entity.x] = True
        ents[target.y, target.x] = True
        walkable_map = self.map.walkable & ents
        astar = tcod.path.AStar(walkable_map)

        # set own and target's cells to walkable to allow path to work
        path = astar.get_path(entity.x, entity.y, target.x, target.y)
        if path:
            result = path[0]
        return result

    def get_fov_map(self, x, y, radius, light_walls=True, algorithm=tcod.FOV_RESTRICTIVE):
        return tcod.map.compute_fov(self.map.transparent, (x, y), radius, light_walls, algorithm)

    # is tile at (x, y) walkable?
    def walkable(self, x, y):
        return self.map.walkable[y, x]

    # is tile at (x, y) transparent?
    def transparent(self, x, y):
        return self.map.transparent[y, x]

    # is tile at (x, y) visible for player?
    def fov(self, x, y):
        return self.map.fov[y, x]

    # has tile at (x, y) been explored?
    def explored(self, x, y):
        return self.explored_tiles[y, x]

    # Create rooms for map
    def make_map(self, max_rooms: int, room_min_size: int, room_max_size: int, map_width: int, map_height: int,
                 player: Entity, entities: list, max_monsters_per_room: int, max_items_per_room: int):
        self.initialise_map()
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)
            new_room = Rectangle(x, y, w, h)

            # if this intersects another room, then don't fill it in
            for other_room in rooms:
                if new_room.intersects(other_room):
                    break
            else:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()
                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                rooms.append(new_room)
                num_rooms += 1
                self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

        # update the pathfinding to match the new map
        self.astar = tcod.path.AStar(self.map.walkable)

    # Carve the `room` rectangle out of the map
    def create_room(self, room):
        for y in range(room.y1 + 1, room.y2):
            for x in range(room.x1 + 1, room.x2):
                self.open_tile(x, y)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.open_tile(x, y)

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.open_tile(x, y)

    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(10, 0, 3)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', render_order=RenderOrder.ACTOR,
                                     blocks=True, fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(16, 1, 4)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', render_order=RenderOrder.ACTOR, blocks=True,
                                     fighter=fighter_component, ai=ai_component)
                entities.append(monster)

        for i in range(number_of_items):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_component = Item(heal, amount=4)
                item = Entity(x, y, 'p', tcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM, item=item_component)
                entities.append(item)

    def open_tile(self, x, y):
        self.map.walkable[y, x] = True
        self.map.transparent[y, x] = True
