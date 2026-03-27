# Day 2: Attack Scenarios I — Payloads, Metasploit, and C2 Frameworks

## Materials Overview

### Handouts (Lecture Material)

Handouts are in `handout/` and meant to be given to participants as reference material (convert to PDF).

| File | Topic |
|---|---|
| [`01_c2_architecture.md`](handout/01_c2_architecture.md) | C2 concepts, reverse shells, staged payloads, AttackMate's role |
| [`02_metasploit_integration.md`](handout/02_metasploit_integration.md) | msfrpcd setup, msf-module, msf-session, msf-payload, LAST_MSF_SESSION |
| [`03_payload_delivery.md`](handout/03_payload_delivery.md) | msf-payload formats, webserv, background mode, PHP RCE demo |
| [`04_shell_upgrades_post_exploitation.md`](handout/04_shell_upgrades_post_exploitation.md) | Shell limitations, shell-to-meterpreter, Meterpreter stdapi commands |
| [`05_modular_playbooks.md`](handout/05_modular_playbooks.md) | include command, reusable sub-playbooks, variable passing |
| [`06_sliver_c2.md`](handout/06_sliver_c2.md) | Sliver concepts, sliver and sliver-session command types |
| [`07_command_reference.md`](handout/07_command_reference.md) | Quick reference card for all Day 2 commands |

### Walkthroughs (Guided)

Walkthroughs are in `walkthroughs/` and are run together with the instructor. Each is a complete, runnable playbook with detailed comments.

| File | Topic | Requires Target |
|---|---|---|
| [`01_vsftpd_backdoor.yml`](walkthroughs/01_vsftpd_backdoor.yml) | vsftpd exploit, shell session, post-exploitation commands | Yes |
| [`02_php_rce_payload.yml`](walkthroughs/02_php_rce_payload.yml) | Generate payload, serve via webserv, PHP RCE, catch reverse shell | Yes |
| [`03_samba_meterpreter.yml`](walkthroughs/03_samba_meterpreter.yml) | Samba usermap_script exploit, upgrade to Meterpreter, post-exploitation | Yes |
| [`04_modular_include.yml`](walkthroughs/04_modular_include.yml) | Refactored modular playbook using include files | Yes |

### Exercises (Interactive)

Exercises are in `exercises/` and have `# TODO` comments that participants fill in. Corresponding solutions are in `exercises/solutions/`.

| File | Topic |
|---|---|
| [`exercise_01_msf_exploit.yml`](exercises/exercise_01_msf_exploit.yml) | Exploit a Metasploitable2 service via msf-module, run post-exploitation via msf-session |
| [`exercise_02_payload_webserv.yml`](exercises/exercise_02_payload_webserv.yml) | Generate a payload, serve it with webserv, catch a reverse shell |
| [`exercise_03_meterpreter_upgrade.yml`](exercises/exercise_03_meterpreter_upgrade.yml) | Upgrade a shell session to Meterpreter, extract system information |
| [`exercise_04_include_refactor.yml`](exercises/exercise_04_include_refactor.yml) | (Stretch) Refactor post-exploitation commands into a reusable include file |

## Prerequisites

Day 2 requires the Metasploit RPC daemon (`msfrpcd`) to be running. Have participants start it at the beginning of the session:

```bash
# Start the Metasploit RPC daemon on the attacker machine
msfrpcd -P msf -a 127.0.0.1

# Verify it is listening
ss -tlnp | grep 55553
```

All Day 2 playbooks require a config file with the RPC connection settings. Use the provided `config.yml`:

```bash
attackmate --config config.yml walkthrough.yml
```

## Instructor Notes

- **Metasploit RPC**: `msfrpcd` must be started before any `msf-*` command works. Start it at the beginning of the day and verify the port is open.
- **Config file**: All walkthrough and exercise playbooks assume `config.yml` is passed with `--config`.
- **Target IP and Attacker IP**: Remind participants to replace `CHANGE_ME` / `172.17.0.106` (target) and `CHANGE_ME_ATTACKER` / `172.17.0.127` (attacker) with their actual IPs.
- **Walkthrough 01 (vsftpd)**: The vsftpd 2.3.4 backdoor is timing-sensitive and can fail on first attempt. If it times out, run it again.
- **Walkthrough 03 (Samba)**: Requires Samba on port 139 to be reachable. Verify with `nc -zvw3 <TARGET> 139` before starting. The `username map script` configuration is present on Metasploitable2 by default.
- **Walkthrough 02 (PHP RCE)**: Uses PHP-CGI argument injection (CVE-2012-1823) on Metasploitable2's Apache. Requires curl and verifying the endpoint is reachable.
- **Walkthrough 04 (Modular)**: Builds directly on walkthrough 01. Participants must understand walkthrough 01 before moving on.
- **Module 6 (Sliver)**: Demo only. No participant walkthrough is provided. A running Sliver server is required for the demo.
