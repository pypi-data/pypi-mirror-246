from __future__ import annotations

import os
import json
import toml
from pathlib import Path
from typing import Optional, Union
from pydantic import BaseModel, Field, model_validator
from datetime import datetime, timedelta
from result import Result, Ok, Err
from ci.api import endpoint
from ci import ext, env


class TokenHeader(BaseModel):
    """
    kid (str): Key ID. An identifier for the cryptographic key used to sign the token. It is used to select the correct key for verifying the token's signature.
    alg (str): Algorithm. Indicates the cryptographic algorithm used to secure the token. EG: RS256 implies RSA signature with SHA-256.
    """

    kid: str
    alg: str

    def __repr__(self) -> str:
        return f"TokenHeader(alg={self.alg})"

    def __str__(self) -> str:
        return self.__repr__()


class TokenPayload(BaseModel):
    """
    sub (str): Subject. A unique identifier for the user. It's intended to be used to identify the principal (the user in this context).
    iss (str): Issuer. Identifies the principal that issued the JWT. Here, it's an Amazon Cognito User Pool.
    aud (str): Audience. Intended recipients of the token. Here, it's the Cognito App Client ID (this is public information).
    iat (int): Issued At. The time at which the token was issued as a unix timestamp.
    exp (int): Expiry. The time at which the token expires as a unix timestamp.
    auth_time (int): Authorization Timestamp. The time when authentication occurred.
    jti (str): JWT ID. A unique identifier for this token. It can be used to prevent the token from being replayed.
    origin_jti (str): A unique identifier for the token from which this token was generated.
    event_id (str):  A unique identifier for the authentication event that generated this token.
    token_use (str): Indicates the intended use of the token. Here, it's an ID token.
    given_name (str): The first name of the user.
    family_name (str): The last name of the user.
    email (str): The email address of the user.
    cognito_username (str): Automatically generated cognito username.
    custom_domain (str): The domain name of the users email (eg: 'gmail.com').
    """

    sub: str
    iss: str
    aud: str
    iat: int
    exp: int
    auth_time: int
    jti: str
    origin_jti: str
    event_id: str
    token_use: str
    given_name: str
    family_name: str
    email: str
    cognito_username: str
    custom_domain: str

    @model_validator(mode="before")
    @classmethod
    def __preprocess(cls, data: dict) -> dict:
        if "cognito:username" in data.keys():
            data["cognito_username"] = data.pop("cognito:username")
        if "custom:domain" in data.keys():
            data["custom_domain"] = data.pop("custom:domain")
        return data

    @property
    def remaining(self) -> timedelta:
        raise

    @property
    def expiry(self) -> datetime:
        return datetime.fromtimestamp(self.exp)

    def __repr__(self) -> str:
        return f"TokenPayload(exp={str(self.expiry)[:19]})"

    def __str__(self) -> str:
        return self.__repr__()


class CognitoIdentificationToken(BaseModel):
    """AWS Cognito ID JWT (JSON Web Token) Class"""

    header: TokenHeader
    payload: TokenPayload
    jwt: str

    def __repr__(self) -> str:
        return f"CognitoIdentificationToken(email='{str(self.payload.email)}', expires={self.payload.expiry})"

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def load(path: Path) -> Union[CognitoIdentificationToken, None]:
        """Load a CognitoIdentificationToken from a toml file"""
        if not path.exists():
            return None
        else:
            with open(path, "r") as f:
                return CognitoIdentificationToken.model_validate(toml.load(f))
            # try:
            #     with open(path, "r") as f:
            #         return CognitoIdentificationToken.model_validate(toml.load(f))
            # except:
            #     CognitoIdentificationToken.delete(path)
            #     return None

    @staticmethod
    def delete(path: Path) -> None:
        """Delete a CognitoIdentificationToken to a toml file"""
        if path.exists():
            os.remove(path)

    @staticmethod
    def parse(jwt: str) -> CognitoIdentificationToken:
        header, payload, signature = jwt.split(".")
        return CognitoIdentificationToken.model_validate(
            {
                "header": json.loads(ext.base64_url_decode(header)),
                "payload": json.loads(ext.base64_url_decode(payload)),
                "jwt": jwt,
            }
        )

    def save(self, path: Path) -> None:
        """Save a CognitoIdentificationToken to a toml file"""
        with open(path, "w") as f:
            f.write(toml.dumps(self.model_dump()))


class AccountInterface(BaseModel):
    token: Optional[CognitoIdentificationToken] = None

    @staticmethod
    def load() -> AccountInterface:
        return AccountInterface(token=CognitoIdentificationToken.load(env.TOKEN))

    def __repr__(self) -> str:
        if self.token is None:
            return f"Account(NA)"
        else:
            return f"Account(email={self.token.payload.email})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def authenticated(self) -> bool:
        # todo: check expiry, call endpoint to check, refresh if necessary, call logout if expired
        return self.token is not None

    @property
    def email(self) -> Optional[str]:
        if self.authenticated:
            return self.token.payload.email
        else:
            return None

    @property
    def first_name(self) -> Optional[str]:
        if self.authenticated:
            return self.token.payload.given_name
        else:
            return None

    @property
    def last_name(self) -> Optional[str]:
        if self.authenticated:
            return self.token.payload.family_name
        else:
            return None

    def __handle_response_failure(self, response: dict) -> Result[bool, str]:
        if "errorMessage" in response.keys():
            if "timed out" in response["errorMessage"]:
                raise TimeoutError("Timeout Error: Please try again.")
            else:
                raise Exception("Unexpected Error: Please submit a GitHub issue.")
        else:
            if "message" in response.keys():
                return Err(response["message"])
            else:
                raise Exception("Unexpected Error: Please submit a GitHub issue.")

    def register(
        self,
        email: str,
        first_name: str,
        last_name: str,
    ) -> Result[str, str]:
        """_summary_

        Args:
            email (str): _description_
            first_name (str): _description_
            last_name (str): _description_

        Returns:
            Result[bool, str]: _description_
        """
        if self.authenticated:
            # todo: add logout warning
            self.token.delete(env.TOKEN)
        response = endpoint.account_register.post(
            data={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            }
        )
        if response["message"] == "Request Received":
            return Ok("Registration Request Received")
        else:
            return self.__handle_response_failure(response)

    def confirm(
        self,
        email: str,
        temporary_password: str,
        new_password: str,
    ) -> Result[bool, str]:
        response = endpoint.account_confirm.post(
            data={
                "email": email,
                "temporary_password": temporary_password,
                "new_password": new_password,
            }
        )
        if response["message"] == "Request Received":
            return Ok(True)
        else:
            return self.__handle_response_failure(response)

    def login(self, email: str, password: str) -> Result[bool, str]:
        if self.authenticated:
            self.token.delete(env.TOKEN)
        response = endpoint.account_login.post(
            data={"email": email, "password": password}
        )

        if response["authenticated"]:
            self.token = CognitoIdentificationToken.parse(response["token"])
            self.token.save(env.TOKEN)
            return Ok("Login Successful")
        else:
            return self.__handle_response_failure(response)

    # todo: refactor
    def logout(self) -> Result[bool, str]:
        if not self.authenticated:
            return Err("You are not logged in.")
        else:
            self.token.delete(env.TOKEN)
            self.token = None
            return Ok("Logout Successful")

    # todo: refactor
    def info(self) -> Result[dict, str]:
        if not self.authenticated:
            return Err("You are not logged in.")
        else:
            response = endpoint.account_info.get(data={"email": self.email})
            return Ok(response)

    # todo: refactor
    def access(self) -> Result[dict, str]:
        if not self.authenticated:
            return Err("You are not logged in.")
        else:
            response = endpoint.account_access.get(data={"email": self.email})
            return Ok(response)

    # todo: refactor
    def enable(self) -> Result[dict, str]:
        if not self.authenticated:
            return Err("You are not logged in.")
        else:
            response = endpoint.account_enable.get(data={"email": self.email})
            return Ok(response)

    # todo: refactor
    def password(self) -> Result[dict, str]:
        "reset password"
        if not self.authenticated:
            return Err("You are not logged in.")
        else:
            response = endpoint.account_password.get(data={"email": self.email})
            return Ok(response)


# @field_validator("email")
# def __validate_email(cls, email: str) -> str:
#     if not validation.check_email_format(email=email):
#         raise ValueError("Invalid email address.")
#     return email

# @staticmethod
# def _reset() -> ResetResult:

# @staticmethod
# def create() -> CreateResult:
#     if ACCOUNT.exists():
#         return CreateResult(created=False, message="An account file already exists.")
#     else:
#         with open(ACCOUNT, "w") as fa:
#             fa.write(toml.dumps(dict()))
#         fa.close()
#         return CreateResult()

# @staticmethod
# def _load_email() -> Union[str, None]:
#     if ACCOUNT.exists():
#         with open(ACCOUNT) as fa:
#             account_info = toml.loads(fa.read())
#         fa.close()
#         try:
#             return account_info["email"]
#         except:
#             return None
#     else:
#         return None

# @staticmethod
# def _load_name() -> Union[Name, None]:
#     if ACCOUNT.exists():
#         with open(ACCOUNT) as fa:
#             account_info = toml.loads(fa.read())
#         fa.close()
#         try:
#             return Name.model_validate(account_info["name"])
#         except:
#             return None
#     else:
#         return None

# @staticmethod
# def _load_token() -> Union[Token, None]:
#     if ACCOUNT.exists():
#         with open(ACCOUNT) as fa:
#             account_info = toml.loads(fa.read())
#         fa.close()
#         try:
#             return Token.model_validate(account_info["token"])
#         except:
#             return None
#     else:
#         return None

# def save(self) -> None:
#     with open(ACCOUNT, "w") as fa:
#         fa.write(toml.dumps(self.model_dump()))
#     fa.close()

# def register(
#     self,
#     first_name: str,
#     last_name: str,
#     email: str,
# ) -> str:
#     """
#     Submit a registration request.

#     Notes:
#         To mitigate information leakage, this will virtually always return True.

#     Raises:
#         Exception: Status code other than 200, probably network error.

#     Returns:
#         str: Whether the request has been received (this does not mean it is acted upon).
#     """
#     if self._load_email() is not None:
#         raise ValueError(
#             "It appears you are already registered. Try logging out if you want to register again."
#         )
#     email = self.__validate_email(email)
#     response = requests.post(
#         endpoint.account_register,
#         json={
#             "email": email,
#             "first_name": first_name,
#             "last_name": last_name,
#         },
#     )
#     if response.status_code != 200:
#         raise Exception("Unknown error, please submit GitHub issue.")
#     else:
#         self.email = email
#         self.name = Name(first=first_name, last=last_name)
#         self.save()
#         # todo: fix later
#         response_json = response.json()
#         if isinstance(response_json, str):
#             response_json = json.loads(response_json)
#         if "message" in response_json.keys():
#             return response_json["message"]
#         elif "errorMessage" in response_json.keys():
#             if "timed out" in response_json["errorMessage"]:
#                 raise TimeoutError("Timeout Error: Please try again.")
#             else:
#                 raise Exception("Unexpected Error: Please submit a GitHub issue.")
#         else:
#             raise Exception("Unexpected Error: Please submit a GitHub issue.")

# def confirm(
#     self, temporary_password: str, new_password: str, email: Optional[str] = None
# ) -> bool:
#     """
#     Confirm email with temporary password, while simultaneously setting a new password.

#     Notes:
#         To mitigate information leakage, this will virtually always return True.

#     Args:
#         temporary_password (str): _description_
#         new_password (str): _description_
#         email (Optional[str], optional): _description_. Defaults to None.

#     Raises:
#         ValueError: _description_
#         Exception: _description_

#     Returns:
#         bool: _description_
#     """
#     # if no email passed and class email is none
#     if email is not None:
#         self.email = email
#     # todo: refactor
#     elif self.email is not None:
#         pass
#     elif (email is None) and (self.email is None):
#         # try load email
#         email = self._load_email()
#         # if still none, raise error, no email found
#         if email is None:
#             raise ValueError(
#                 (
#                     "Email was not passed as parameter, and could not be resolved. "
#                     "If you haven't registered, doing so should fix this error."
#                 )
#             )
#         else:
#             self.email = email
#     else:
#         raise Exception("Unexpected exception, please submit a GitHub issue.")
#     if not validation.check_email_format(self.email):
#         raise ValueError("Invalid email format.")
#     new_password_valid, new_password_checks = validation.check_password(new_password)
#     if not new_password_valid:
#         failures = [key for key, val in new_password_checks.items() if not val]
#         raise ValueError(
#             f"New password does not meet requirements, failed on: {', '.join(failures)}"
#         )
#     response = requests.post(
#         endpoint.account_confirm,
#         json={
#             "email": self.email,
#             "temporary_password": temporary_password,
#             "new_password": new_password,
#         },
#     )
#     # todo: fix later
#     response_json = response.json()
#     if isinstance(response_json, str):
#         response_json = json.loads(response_json)
#     if "message" in response_json.keys():
#         return response_json["message"]
#     elif "errorMessage" in response_json.keys():
#         if "timed out" in response_json["errorMessage"]:
#             raise TimeoutError("Timeout Error: Please try again.")
#         else:
#             raise Exception("Unexpected Error: Please submit a GitHub issue.")
#     else:
#         raise Exception("Unexpected Error: Please submit a GitHub issue.")
