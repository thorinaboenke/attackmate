# Remote Command Execution

AttackMate can orchestrate commands on other AttackMate instances running as API servers. The `remote` command type lets a local playbook trigger commands or entire sub-playbooks on a remote machine, useful for distributed attack scenarios, multi-host labs, or separating attacker infrastructure across network segments.

## Architecture

```
Attacker machine (local)                Remote machine
┌─────────────────────────┐            ┌──────────────────────────┐
│  attackmate playbook.yml │  HTTPS     │  attackmate --serve      │
│                         │ ─────────► │  (REST API on port 8443) │
│  type: remote           │            │                          │
│    cmd: execute_command │            │  Executes the command    │
│    remote_command:      │ ◄───────── │  Returns result          │
│      type: shell        │            └──────────────────────────┘
│      cmd: whoami        │
└─────────────────────────┘
```

## Configuration

Remote instances are defined in the AttackMate config file under `remote_config`. Each entry specifies a URL, credentials, and a TLS certificate for verification:

```yaml
# attackmate.yml
remote_config:
  pivot-node:
    url: https://192.168.1.50:8443
    username: admin
    password: secret
    cafile: /path/to/ca.pem
  dmz-sensor:
    url: https://10.0.0.254:8443
    username: sensor
    password: topsecret
    cafile: /path/to/ca.pem
```

When `connection` is omitted from a `remote` command, the first entry in `remote_config` is used as the default.

## The `remote` Command

### `execute_command` - Run a single command remotely

Sends one AttackMate command to the remote instance and waits for the result:

```yaml
- type: remote
  cmd: execute_command
  connection: pivot-node
  remote_command:
    type: shell
    cmd: whoami
```

`remote_command` accepts any command type that the remote instance supports — `shell`, `ssh`, `msf-module`, `debug`, etc. The one exception is `type: remote` itself (no recursive remoting).

### `execute_playbook` - Run a full playbook on a remote instance

Uploads a local playbook file and executes it on the remote instance:

```yaml
- type: remote
  cmd: execute_playbook
  connection: pivot-node
  playbook_path: /home/user/playbooks/lateral_move.yml
```

This is useful for offloading a complex sequence of commands to a machine that has the right network access or tooling.

## Important Behavior Notes

- Options like `background`, `only_if`, and `error_if` on the `remote` command itself control **local** execution, not the remote side.
- The remote instance must be running attackmate as a server and be reachable over HTTPS.
- The `cafile` must match the certificate used by the remote instance.


## Example: Using Variables in Remote Commands

Variable substitution happens **locally** before the command is sent. So `$TARGET` in a `remote_command` is resolved on the local machine using the local variable store:

```yaml
vars:
  TARGET: "10.10.10.5"

commands:
  - type: remote
    cmd: execute_command
    connection: pivot-node
    remote_command:
      type: shell
      cmd: ping -c 1 $TARGET   # $TARGET is substituted locally to "10.10.10.5"
```

## Key Fields Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `cmd` | str | Yes | `execute_command` or `execute_playbook` |
| `connection` | str | No | Named connection from `remote_config` (default: first entry) |
| `remote_command` | command | When `cmd: execute_command` | Any AttackMate command except `type: remote` |
| `playbook_path` | str | When `cmd: execute_playbook` | Path to a local playbook file to upload and run |
