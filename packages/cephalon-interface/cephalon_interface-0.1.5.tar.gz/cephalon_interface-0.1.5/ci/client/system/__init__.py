from __future__ import annotations

from pydantic import BaseModel
from ci.client.account import AccountInterface
from ci.client.system.hercules import HerculesInterface


class SystemInterface(BaseModel):
    hercules: HerculesInterface

    @staticmethod
    def build(account: AccountInterface) -> SystemInterface:
        return SystemInterface(
            hercules=HerculesInterface(account=account),
        )
