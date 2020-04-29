import tcod
import textwrap


class Message:
    def __init__(self, text, colour=tcod.white):
        self.text = text
        self.colour = colour


class MessageLog:
    def __init__(self, x, width, height):
        self.x = x
        self.width = width
        self.height = height
        self.messages = []

    def add_message(self, message):
        # split the message across lines if necessary
        new_msg_lines = textwrap.wrap(message.text, self.width)
        for line in new_msg_lines:
            # if full of messages, remove the oldest (the rest will shift up positions)
            if len(self.messages) == self.height:
                del self.messages[0]
            # finally, add message to the end
            self.messages.append(Message(line, message.colour))
