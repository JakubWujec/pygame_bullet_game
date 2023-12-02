from .Unit import Unit


class Tank(Unit):
    def move(self, moveVector):
        newPos = self.position + moveVector

        if not self.state.isPositionInsideWorld(newPos):
            return

        for unit in self.state.units:
            if newPos == unit.position:
                return

        self.position = newPos
