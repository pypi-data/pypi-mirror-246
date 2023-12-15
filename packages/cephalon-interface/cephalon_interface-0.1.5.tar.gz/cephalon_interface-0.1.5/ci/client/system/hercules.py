from pydantic import BaseModel
from ci.client.account import AccountInterface


class HerculesInterface(BaseModel):
    account: AccountInterface
