# Day 3: Attack Scenarios II — Full Kill Chain Lab

## Materials Overview

### Handouts (Lecture Material)

Handouts are in `handout/` and meant to be distributed to participants as reference material (convert to PDF).

| File | Topic |
|---|---|
| [`01_debugging_cheatsheet.md`](handout/01_debugging_cheatsheet.md) | Diagnosing network, service, and AttackMate issues |
| [`02_cyber_kill_chain.md`](handout/02_cyber_kill_chain.md) | Lockheed Martin Kill Chain phases, mapped to AttackMate commands |
| [`03_mitre_attack.md`](handout/03_mitre_attack.md) | MITRE ATT&CK tactics, techniques, and mappings for today's lab |
| [`04_attacks_in_logs.md`](handout/04_attacks_in_logs.md) | Where attacks appear in logs — the defender's view |
| [`05_attack_path.md`](handout/05_attack_path.md) | Menu of modular options for each kill chain phase |

### Exercises (Interactive)

The main exercise is `exercises/attack_chain.yml`. Participants pick options from the attack path menu and assemble their own full-chain playbook using the provided include modules.

| File | Purpose |
|---|---|
| [`exercises/attack_chain.yml`](exercises/attack_chain.yml) | Top-level skeleton: wire together your chosen include files |
| **Initial Access** | |
| [`exercises/includes/recon_nmap.yml`](exercises/includes/recon_nmap.yml) | Reconnaissance: nmap scan + parse results (TODOs) |
| [`exercises/includes/entry_vsftpd.yml`](exercises/includes/entry_vsftpd.yml) | Initial Access: vsftpd 2.3.4 backdoor, root shell (TODOs)|
| [`exercises/includes/entry_samba.yml`](exercises/includes/entry_samba.yml) | Initial Access: Samba usermap_script, root shell (TODOs) |
| [`exercises/includes/entry_ssh.yml`](exercises/includes/entry_ssh.yml) | Initial Access: SSH weak credentials, msfadmin user (TODOs) |
| [`exercises/includes/entry_unreal_ircd.yml`](exercises/includes/entry_unreal_ircd.yml) | Initial Access: UnrealIRCd backdoor CVE-2010-2075, daemon user (TODOs) |
| [`exercises/includes/entry_distcc.yml`](exercises/includes/entry_distcc.yml) | Initial Access: distcc daemon RCE CVE-2004-2687, daemon user (TODOs) |
| **Privilege Escalation** | |
| [`exercises/includes/privesc_suid_nmap.yml`](exercises/includes/privesc_suid_nmap.yml) | Priv Esc: SUID nmap abuse, any user to root (TODOs) |
| [`exercises/includes/privesc_sudo.yml`](exercises/includes/privesc_sudo.yml) | Priv Esc: passwordless sudo, msfadmin to root (pre-written) |
| **Post-Exploitation** | |
| [`exercises/includes/post_basic_info.yml`](exercises/includes/post_basic_info.yml) | Discovery: system info via session (pre-written) |
| [`exercises/includes/post_meterpreter_upgrade.yml`](exercises/includes/post_meterpreter_upgrade.yml) | Upgrade shell session to Meterpreter (TODOs) |
| **Persistence** | |
| [`exercises/includes/persist_ssh_key.yml`](exercises/includes/persist_ssh_key.yml) | Persistence: SSH authorized key injection (TODOs) |
| [`exercises/includes/persist_cron.yml`](exercises/includes/persist_cron.yml) | Persistence: cron backdoor reverse shell (TODOs) |
| [`exercises/includes/persist_new_user.yml`](exercises/includes/persist_new_user.yml) | Persistence: create backdoor user account (TODOs) |
| **Actions** | |
| [`exercises/includes/collect_shadow.yml`](exercises/includes/collect_shadow.yml) | Credential Access: read /etc/shadow (TODOs) |
| [`exercises/includes/exfil_sftp.yml`](exercises/includes/exfil_sftp.yml) | Exfiltration: SFTP download of collected files (TODOs) |

---



## Prerequisites

Day 3 requires the same setup as Day 2: Metasploit RPC daemon running and a config file.

```bash
# Start the Metasploit RPC daemon
msfrpcd -P msf -a 127.0.0.1

# Verify it is listening
ss -tlnp | grep 55553
```

Run all playbooks with `--config`:

```bash
attackmate --config ../day3/config.yml exercises/attack_chain.yml
```

---

## Instructor Notes

- **No new AttackMate syntax today.** Every command type used already appeared in days 1-2. The challenge is planning and assembly, not learning new features.
- **Debugging cheatsheet (handout 01)** should be distributed before the interactive exercies
- **Privilege escalation is the key new concept.** distcc exploit gives non non-root shells. Encourage participants to use these as their entry point, so they actually have to practice privilege escalation. It is a much more realistic and instructive scenario than starting as root.
- **vsftpd timing issues.** vsftpd backdoor can be timing-sensitive, or succeeds once but needs metasploit reboot after backdoor is exploited once
- **SUID nmap cleanup.**  `privesc_suid_nmap.yml` sets the SUID bit on `/bin/bash`. This must can be cleaned up after the exercise with `chmod u-s /bin/bash`
- **Cron persistence cleanup.** `persist_cron.yml` writes to `/etc/cron.d/backdoor`. Remove this file (`rm /etc/cron.d/backdoor`) at the end, otherwise the cron job keeps firing every minute.
- **Target IP and Attacker IP.** Remind participants to replace `CHANGE_ME` and `CHANGE_ME_ATTACKER` with their actual IPs before running anything.
