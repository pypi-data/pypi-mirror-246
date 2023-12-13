from pydantic import BaseModel
from ci.api.account import AccountInterface


class AemethInterface(BaseModel):
    account: AccountInterface
