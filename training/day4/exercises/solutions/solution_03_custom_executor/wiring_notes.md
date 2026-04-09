# Wiring Notes for Solution 4

After copying the two Python files, make these three edits to wire the new command in.

## 1. `src/attackmate/executors/__init__.py`

Add the import and list entry:

```python
from .common.helloexecutor import HelloExecutor

__all__ = [
    # ... existing entries ...
    'HelloExecutor',
]
```

## 2. `src/attackmate/schemas/loop.py`

Add `HelloCommand` to the `Command` union:

```python
from attackmate.schemas.hello import HelloCommand

Command = Union[
    ShellCommand,
    HelloCommand,   # add this line
    # ... other commands ...
]
```

## 3. `src/attackmate/schemas/command_subtypes.py`

Add `HelloCommand` to `RemotelyExecutableCommand`:

```python
from attackmate.schemas.hello import HelloCommand

RemotelyExecutableCommand: TypeAlias = Annotated[
    Union[
        HelloCommand,   # add this line
        # ... other commands ...
    ],
    Field(discriminator='type'),
]
```

## Verify

Run the test playbook:

```bash
uv run attackmate training/day4/exercises/exercise_04_custom_executor/test_playbook.yml
```
