class GameMode:
    def __init__(self) -> None:
        self.__observers = []

    def addObserver(self, observer):
        self.__observers.append(observer)

    def removeObserver(self, observer):
        self.__observers.remove(observer)

    def notifyQuitRequested(self):
        for observer in self.__observers:
            observer.quitRequested()

    def notifyGameStarted(self):
        for observer in self.__observers:
            observer.gameStarted()

    def notifyShowMenuRequested(self):
        for observer in self.__observers:
            observer.showMenuRequested()

    def notifyShowGameRequested(self):
        for observer in self.__observers:
            observer.showGameRequested()

    def notifyLoadLevelRequested(self, fileName="app/assets/levels/level_1.tmx"):
        for observer in self.__observers:
            observer.loadLevelRequested(fileName)

    def notifyGameLost(self):
        for observer in self.__observers:
            observer.gameLost()

    def notifyResizeRequested(self, worldSize):
        for observer in self.__observers:
            observer.resizeRequested(worldSize)

    def processInput(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def render(self, window):
        raise NotImplementedError()
