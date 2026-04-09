# Day 4: Advanced Capabilities and Extending AttackMate

## Materials Overview

### Handouts (Lecture Material)

Handouts are in `handout/` and meant to be distributed to participants as reference material (convert to PDF).

| File | Topic |
|---|---|
| [`01_browser_automation.md`](handout/01_browser_automation.md) | Driving a real browser from a playbook with the `browser` command |
| [`02_bettercap_integration.md`](handout/02_bettercap_integration.md) | Network-layer attacks via the Bettercap REST API |
| [`03_remote_execution.md`](handout/03_remote_execution.md) | Orchestrating commands across multiple AttackMate instances |
| [`04_custom_executors.md`](handout/04_custom_executors.md) | Adding new command types and executors to the AttackMate codebase |

### Exercises (Interactive)

Exercises are in `exercises/` and have `# TODO` comments for participants to fill in.

| File | Topic | Requires |
|---|---|---|
| [`exercise_01_browser.yml`](exercises/exercise_01_browser.yml) | Automate a DVWA web login and take a screenshot | Metasploitable2, Playwright |
| [`exercise_02_bettercap.yml`](exercises/exercise_02_bettercap.yml) | Discover LAN hosts via Bettercap passive probing | Bettercap running with REST API |
| [`exercise_03_custom_executor/`](exercises/exercise_03_custom_executor/) | Build a `hello` command type and executor from scratch | Python, AttackMate source |

### Solutions

| File | Description |
|---|---|
| [`solutions/solution_01_browser.yml`](exercises/solutions/solution_01_browser.yml) | Complete browser login automation |
| [`solutions/solution_02_bettercap.yml`](exercises/solutions/solution_02_bettercap.yml) | Complete Bettercap discovery workflow |
| [`solutions/solution_03_custom_executor/`](exercises/solutions/solution_03_custom_executor/) | Complete `HelloCommand` schema, executor, and wiring notes |

---

## Prerequisites

### Browser (Exercise 1)

Playwright must be installed. It is included in the `attackmate` dev dependencies:

```bash
uv sync --dev
uv run playwright install chromium
```

Metasploitable2 must be reachable. DVWA is available at `http://<TARGET>/dvwa/`.

### Bettercap (Exercise 2)

Bettercap must be installed and running with the REST API enabled:

```bash
sudo bettercap -eval "set api.rest.username btrcp; set api.rest.password secret; api.rest on"
```

Add a `bettercap_config` section to the AttackMate config file:

```yaml
bettercap_config:
  default:
    url: "http://localhost:8081"
    username: btrcp
    password: secret
```

### Custom Executor (Exercise 3)

Participants need the AttackMate source tree checked out and the dev environment set up:

```bash
uv sync --dev
```

---

## Instructor Notes

- **Browser exercise**: The DVWA login page selectors (`input[name='username']`, `input[name='password']`, `input[type='submit']`) are stable across DVWA versions. Encourage participants to use browser DevTools to verify selectors before coding them into the playbook.
- **Browser headless mode**: If the lab machines have no graphical display, add `headless: true` to all browser commands. The screenshots will still be saved.
- **Bettercap exercise**: `net.probe on` requires root or the `CAP_NET_RAW` capability. Run `sudo attackmate ...` for this exercise if needed.
- **Custom executor exercise**: Participants who finish early can add more fields to their schema (e.g., a `repeat` count that logs the message multiple times) or implement a more interesting executor that calls an external tool.
- **Target IP**: Remind participants to replace `CHANGE_ME` with their actual Metasploitable2 IP in exercises 1 and 2.
