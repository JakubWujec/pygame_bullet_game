from .Command import Command


class ExplodeCommand(Command):
    def __init__(self, state, explosion) -> None:
        super().__init__()
        self.state = state
        self.explosion = explosion

    def run(self):
        # if explosion touch unit destroy it
        unitsAtPosition = self.state.findUnitsAt(self.explosion.position)
        for unit in unitsAtPosition:
            unit.status = "destroyed"

        if self.explosion.isTimeToDelete():
            self.explosion.status = "destroyed"
