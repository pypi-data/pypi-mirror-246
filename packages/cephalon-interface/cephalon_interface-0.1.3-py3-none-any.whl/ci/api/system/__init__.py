from __future__ import annotations

from pydantic import BaseModel
from ci.api.account import AccountInterface
from ci.api.system.aemeth import AemethInterface
from ci.api.system.hercules import HerculesInterface


class SystemInterface(BaseModel):
    aemeth: AemethInterface
    hercules: HerculesInterface

    @staticmethod
    def build(account: AccountInterface) -> SystemInterface:
        return SystemInterface(
            aemeth=AemethInterface(account=account),
            hercules=HerculesInterface(account=account),
        )
