from typing import Literal, Optional
from .base import BaseCommand, StringNumber
from attackmate.command import CommandRegistry


@CommandRegistry.register('c2url')
class C2urlCommand(BaseCommand):
    type: Literal['c2url']
    cmd: Literal['listen', 'wait_for_session', 'stop']
    host: str = '0.0.0.0'  # nosec
    port: StringNumber = '8080'
    timeout: StringNumber = '30'
    connection: Optional[str] = None


@CommandRegistry.register('c2url-session')
class C2urlSessionCommand(BaseCommand):
    # cmd holds the shell command to run on the target.
    type: Literal['c2url-session']
    session: Optional[str] = None
    timeout: StringNumber = '30'
    connection: Optional[str] = None
