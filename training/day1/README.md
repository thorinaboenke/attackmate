# Day 1: AttackMate Fundamentals

## Materials Overview

### Handouts (Lecture Material)

Handouts are in `handout/` and meant to be given to participants as reference material (convert to PDF).

| File | Topic |
|---|---|
| `01_introduction.md` | What is AttackMate, lab environment, playbook structure |
| `02_variables_and_builtins.md` | Variables, builtin variables, setvar, debug |
| `03_shell_and_regex.md` | Shell commands, regex modes, mktemp |
| `04_conditionals_loops_errors.md` | only_if, error handling, loop command, sleep |
| `05_ssh_and_sftp.md` | SSH connections, sessions, interactive mode, SFTP |
| `06_command_reference.md` | Quick reference card for all Day 1 commands |

### Walkthroughs (Guided)

Walkthroughs are in `walkthroughs/` and are run together with the instructor. Each is a complete, runnable playbook with detailed comments explaining every step.

| File | Topic | Requires Target |
|---|---|---|
| `01_hello_world.yml` | Variables, shell, debug, setvar, varstore | No |
| `02_regex_modes.yml` | findall, split, search, sub | No |
| `03_conditionals_and_loops.yml` | only_if, loop with range() | No |
| `04_ssh_attack_chain.yml` | Full SSH attack (nmap, hydra, ssh, sftp, priv esc) | Yes |

### Exercises (Interactive)

Exercises are in `exercises/` and have `# TODO` comments that participants fill in. Corresponding solutions are in `exercises/solutions/`.

| File | Topic |
|---|---|
| `exercise_01_basics.yml` | Variables, shell, debug, setvar |
| `exercise_02_recon_and_parse.yml` | nmap scanning, regex parsing, conditionals |
| `exercise_03_ssh_foothold.yml` | Credential bruteforce, SSH sessions, SFTP |
| `exercise_04_multi_port_scanner.yml` | Loops, conditionals, adaptive scanning |

## Instructor Notes

- **Lab Setup**: Participants need access to a machine with attackmate installed and a Metasploitable2 image as target.
- **Walkthroughs 01-03**: These do not require a live target and can be run locally.
- **Walkthrough 04**: Needs a Metasploitable2 machine as target.
- **Target IP**: Remind participants to change `CHANGE_ME` / `172.17.0.106` to their *actual Metasploitable2 IP* in every playbook.
