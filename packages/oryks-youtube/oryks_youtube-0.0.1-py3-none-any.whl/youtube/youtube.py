from pydantic import BaseModel
from typing import Any


class YouTube(BaseModel):
    """This is the youtube object that is used to interact with the youtube API."""

    def authenticate(self) -> Any:
        """Authenticates the requests made to youtube."""
        print('authenticated')
