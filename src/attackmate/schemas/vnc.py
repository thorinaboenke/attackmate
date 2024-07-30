from typing import Literal, Optional
from attackmate.schemas.base import BaseCommand, StringNumber


class VncCommand(BaseCommand):
    type: Literal['vnc']
    cmd: str = 'connect'
    hostname: Optional[str] = None
    port: StringNumber = '5900'
    password: Optional[str] = None
    key_filename: Optional[str] = None
    creates_session: Optional[str] = None
    session: Optional[str] = None
