from ci.api.account import AccountInterface
from ci.api.system import SystemInterface


class System:
    def __init__(self) -> None:
        self.reload()

    def reload(self) -> None:
        self.account = AccountInterface.load()
        self.use = SystemInterface.build(self.account)


system = System()
