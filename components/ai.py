class BasicMonster:
    def take_turn(self, target, game_map, entities):
        results = []
        # owner is Entity
        monster = self.owner

        if game_map.fov(monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)
                # monster.move_astar(target, game_map, entities)
            elif target.fighter.hp > 0:
                results.extend(monster.fighter.attack(target))

        return results
