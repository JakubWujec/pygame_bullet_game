from .Unit import Unit


class Block(Unit):
    def move(self, moveVector):
        return self.position
