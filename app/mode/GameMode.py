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

    def processInput(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def render(self):
        raise NotImplementedError()
