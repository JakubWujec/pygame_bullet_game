from core.state import World
from core.constants import LayerValue
from ui import UserInterface
from ui.Theme import Theme
from ui.mode import EditGameMode

# Create a basic game state
world = World(16, 10)
ground = world.ground
for y in range(3, 7):
    for x in range(4, 12):
        ground.setValue(x, y, LayerValue.GROUND_EARTH)

# Create a user interface and run it
theme = Theme()
gameMode = EditGameMode(theme, world)
userInterface = UserInterface(theme)
userInterface.run()
userInterface.quit()
