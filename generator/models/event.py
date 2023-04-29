from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    user_id: UUID | str
    ntf_id: UUID | str
    msg_type: str | None
    email: str | None
    destination: str | None
    subject: str | None
    template: str
