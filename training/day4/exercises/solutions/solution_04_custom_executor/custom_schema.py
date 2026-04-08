# Solution for Exercise 4: HelloCommand schema
#
# Copy to: src/attackmate/schemas/hello.py

from typing import Literal
from attackmate.schemas.base import BaseCommand
from attackmate.command import CommandRegistry


@CommandRegistry.register('hello')
class HelloCommand(BaseCommand):
    type: Literal['hello']
    message: str = 'Hello, AttackMate!'
