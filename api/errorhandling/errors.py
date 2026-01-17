from dataclasses import asdict, dataclass
from typing import Optional

from fastapi import HTTPException


@dataclass(frozen=True)
class ErrorResponse:
    status_code: int
    text: str
    solution: Optional[str] = None
    additional_info: Optional[str] = None

    def json(self) -> dict[str, str | int]:
        """Generate a JSON instance from the error content.

        Returns:
            dict[str, str | int]: JSON representation of the error
        """
        return asdict(self)

    def as_http_exception(self) -> HTTPException:
        """Convert the error response into an HTTPException.

        Returns:
            HTTPException: Raisable HTTP exception with details
        """
        return HTTPException(status_code=self.status_code, detail=self.json())
