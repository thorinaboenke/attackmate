# Exercise 4: Build a Custom Executor

In this exercise you will add a brand-new command type to AttackMate from scratch.

## What you will build

A `hello` command that:
- Accepts a `message` field (string, default: `"Hello, AttackMate!"`)
- Logs the message at INFO level when executed
- Returns the message as `$RESULT_STDOUT`

After completing the exercise, this playbook should run successfully:

```yaml
commands:
  - type: hello
    message: "My first custom executor works!"

  - type: debug
    cmd: "Executor said: $RESULT_STDOUT"
```

## Files in this directory

| File | Your task |
|---|---|
| `custom_schema.py` | Define the `HelloCommand` schema — fill in the TODOs |
| `custom_executor.py` | Implement the `HelloExecutor` — fill in the TODOs |
| `test_playbook.yml` | Playbook to test your implementation (no changes needed) |

## Steps

Follow the steps in handout `04_custom_executors.md` and fill in the `# TODO` sections in the two Python files.

After completing both files, copy them into the AttackMate source tree:

```bash
cp custom_schema.py   src/attackmate/schemas/hello.py
cp custom_executor.py src/attackmate/executors/common/helloexecutor.py
```

Then make the three wiring changes (also described in the handout):

1. **`src/attackmate/executors/__init__.py`** — import `HelloExecutor` and add it to `__all__`
2. **`src/attackmate/schemas/loop.py`** — add `HelloCommand` to the `Command` union
3. **`src/attackmate/schemas/command_subtypes.py`** — add `HelloCommand` to `RemotelyExecutableCommand`

Finally, run the test playbook:

```bash
uv run attackmate training/day4/exercises/exercise_04_custom_executor/test_playbook.yml
```

You should see your log message and a debug line showing the executor's output.
