# custom_schema.py
#
# Exercise 4: Define the HelloCommand schema.
#
# When finished, copy this file to:
#   src/attackmate/schemas/hello.py

from attackmate.schemas.base import BaseCommand      # TODO: check this import matches the real path


# TODO: Register this command class with the registry using the decorator.
#       The type string must be 'hello'.
class HelloCommand(BaseCommand):
    # TODO: Add the type discriminator field.
    #       It must be a Literal with the value 'hello'.
    type: ...  # TODO

    # TODO: Add the message field.
    #       It should be a str with a default value of "Hello, AttackMate!"
    message: ...  # TODO
