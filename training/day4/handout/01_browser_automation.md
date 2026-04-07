# Browser Automation with AttackMate

AttackMate includes a `browser` command type backed by [Playwright](https://playwright.dev/), a browser automation library. It lets you drive a real Chromium browser from a playbook, navigating pages, clicking elements, filling forms, and taking screenshots.


## The `browser` Command

```yaml
- type: browser
  cmd: <action>
  # action-specific fields follow
```

### Actions

| `cmd` value | What it does | Required fields |
|---|---|---|
| `visit` | Navigate to a URL | `url` |
| `click` | Click a DOM element | `selector` |
| `type` | Type text into a field | `selector`, `text` |
| `screenshot` | Save a PNG screenshot | `screenshot_path` |

### Selectors

`selector` uses standard CSS selector syntax, the same syntax used in browser DevTools:

```yaml
selector: "input[name='username']"   # by attribute
selector: "button[type='submit']"    # submit button
selector: "#login-btn"               # by ID
selector: ".btn-primary"             # by class
```

## Sessions

By default each `browser` command opens a fresh browser context (no cookies, no state) and destroys it when done. To keep state across multiple commands, for example to log in and then navigate to a protected page, use named sessions.

```yaml
# Open a browser, visit the login page, keep the session open
- type: browser
  cmd: visit
  url: http://192.168.1.100/login
  creates_session: my_browser

# Still in the same browser window: fill username
- type: browser
  cmd: type
  selector: "input[name='username']"
  text: "admin"
  session: my_browser

# Fill password
- type: browser
  cmd: type
  selector: "input[name='password']"
  text: "password123"
  session: my_browser

# Click submit
- type: browser
  cmd: click
  selector: "button[type='submit']"
  session: my_browser

# Screenshot the result
- type: browser
  cmd: screenshot
  screenshot_path: /tmp/after_login.png
  session: my_browser
```

If a session named in `creates_session` already exists, it is automatically closed and replaced.

## Headless Mode

By default the browser window is visible (`headless: false`). On servers or CI without a display, set `headless: true`:

```yaml
- type: browser
  cmd: visit
  url: http://10.0.0.1
  headless: true
  creates_session: ci_session
```

## Background Mode

Background mode (`background: true`) is **not supported** for browser commands.



## Key Fields Reference

| Field | Type | Default | Description |
|---|---|---|---|
| `cmd` | str | `visit` | Action to perform |
| `url` | str | | Target URL (required for `visit`) |
| `selector` | str | | CSS selector (required for `click`/`type`) |
| `text` | str | | Text to enter (required for `type`) |
| `screenshot_path` | str | | Output path (required for `screenshot`) |
| `creates_session` | str | | Name for a new persistent browser session |
| `session` | str | | Name of an existing session to reuse |
| `headless` | bool | `false` | Run without visible window |
