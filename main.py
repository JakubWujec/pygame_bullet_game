from state import World
from state.constants import LAYER_GROUND_EARTH
from ui import UserInterface
from ui.Theme import Theme
from ui.mode import EditGameMode

# Create a basic game state
world = World(16, 10)
for y in range(3, 7):
    for x in range(4, 12):
        world.setValue(x, y, LAYER_GROUND_EARTH)

# Create a user interface and run it
theme = Theme()
gameMode = EditGameMode(theme, world)
userInterface = UserInterface(theme)
userInterface.run()
userInterface.quit()
