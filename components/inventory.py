import tcod
from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('Inventory is full!', tcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You picked up a {0}!'.format(item.name), tcod.blue)
            })
            self.items.append(item)
        return results

    def use_item(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item
        if item_component.use_function is None:
            results.append({'message': Message('Cannot use ' + item_component.name, tcod.yellow)})
        else:
            kwargs = {**item_component.use_function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity)

            results.extend(item_use_results)
        return results

    def drop_item(self, item_entity):
        results = []
        item_entity.x = self.owner.x
        item_entity.y = self.owner.y
        self.remove_item(item_entity)
        results.append({'item_dropped': item_entity, 'message': Message('Dropped ' + item_entity.name)})
        return results

    def remove_item(self, item_entity):
        self.items.remove(item_entity)
        return
