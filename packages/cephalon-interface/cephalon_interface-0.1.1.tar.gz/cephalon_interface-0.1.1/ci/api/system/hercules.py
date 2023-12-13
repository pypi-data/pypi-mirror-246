from pydantic import BaseModel
from ci.api.account import AccountInterface


class HerculesInterface(BaseModel):
    account: AccountInterface
