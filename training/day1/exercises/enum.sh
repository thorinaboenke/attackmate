#!/bin/bash
# Simple privilege escalation enumeration script for training exercises.
# A lightweight alternative to linpeas that runs quickly and offline.

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: SYSTEM INFO
# Goal: Understand the target environment before attempting anything else.
# ─────────────────────────────────────────────────────────────────────────────
echo "========== SYSTEM INFO =========="

# Shows the current user's UID, GID, and group memberships.
# An attacker checks whether they're already root (uid=0), or in privileged
# groups like 'sudo', 'docker'  which can be abused for privilege escalation
id

# Prints the machine's hostname.
hostname

# Prints detailed kernel and OS information (kernel version, architecture, etc.).
# Attackers use this to search for known kernel exploits
uname -a

# Reads the OS release banner (e.g., "Ubuntu 20.04.3 LTS").
# Confirms the distribution and version to narrow down which
# CVEs and exploit paths are applicable on this specific system.
cat /etc/issue

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: SUID BINARIES
# Goal: Find executables that run as root regardless of who launches them.
# SUID (Set User ID) means the binary runs with the file *owner's* privileges
# -> usually root. If any SUID binary can be abused, an attacker can run arbitrary
# commands as root.
# ─────────────────────────────────────────────────────────────────────────────
echo "========== SUID BINARIES =========="

# Searches the entire filesystem for files with the SUID bit set (-perm -4000).
#   -type f       -> only regular files, not directories
#   2>/dev/null   -> suppresses "Permission denied" noise so output stays clean
# An attacker takes this list to for example gtfobins.github.io to find known abuse
# techniques.
find / -perm -4000 -type f 2>/dev/null

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: WRITABLE DIRECTORIES
# Goal: Find places where the attacker can drop files, scripts, or shared libs.
# Write access in sensitive locations enables multiple attack techniques:
# cron job hijacking, shared library injection, or replacing scripts called
# by privileged processes.
# ─────────────────────────────────────────────────────────────────────────────
echo "========== WRITABLE DIRECTORIES =========="

# Finds all directories the current user can write to.
#   -writable      -> current user has write permission
#   -type d        -> directories only
#   head -20       -> limits output to 20 lines (the full list can be enormous)
#   2>/dev/null    -> suppresses permission errors
# Key targets: /tmp (expected), /etc/cron.d, /opt/app, /var/www — anything
# outside /tmp is suspicious and worth investigating for escalation paths.
find / -writable -type d 2>/dev/null | head -20

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: INTERESTING FILES
# Goal: Check access to files that should be root-only.
# ─────────────────────────────────────────────────────────────────────────────
echo "========== INTERESTING FILES =========="

# Checks permissions on /etc/shadow, which stores hashed passwords for all users.
# Normally readable only by root. If a low-privilege user can read it, they can
# copy the hashes and crack them offline.
# If writable, an attacker can replace root's hash with one they know.
ls -la /etc/shadow 2>/dev/null

# Checks permissions on /etc/sudoers, which defines who can run what as root.
# If readable, an attacker can identify misconfigured sudo rules (e.g., NOPASSWD).
# If writable, they can add themselves: "attacker ALL=(ALL) NOPASSWD: ALL"-> instant root.
ls -la /etc/sudoers 2>/dev/null

# Checks whether the current user can list /root (root's home directory).
# This should always be restricted. If accessible, it may reveal SSH keys,
# scripts, credentials, or history files left by an administrator.
ls -la /root 2>/dev/null

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: RUNNING SERVICES
# Goal: Identify processes running as root or other privileged users.
# A vulnerable service running as root is a direct escalation path by exploiting
# the service and inheriting its privileges.
# ─────────────────────────────────────────────────────────────────────────────
echo "========== RUNNING SERVICES =========="

# Lists all running processes with full detail (user, PID, CPU, memory, command).
#   aux            -> all users (a), user-oriented format (u), including no-TTY (x)
#   head -30       -> limits output to the first 30 lines to avoid flooding the terminal
# Attackers look for: processes owned by root running custom/unusual binaries,
# internal services not exposed externally (see next section), outdated daemons,
# or scripts run by cron that might be hijackable.
ps aux 2>/dev/null | head -30

echo ""

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: NETWORK CONNECTIONS
# Goal: Find services listening internally that aren't exposed to the network.
# Internal services often have weaker security assumptions, they may lack
# authentication or run outdated software because "only localhost can reach it."
# ─────────────────────────────────────────────────────────────────────────────
echo "========== NETWORK CONNECTIONS =========="

# Lists all TCP ports in a listening state with the owning process.
#   -t  -> TCP only
#   -l  -> listening sockets only
#   -n  -> show numeric IPs/ports (faster, no DNS resolution)
#   -p  -> show the PID and program name (requires root for full output)
# Falls back to `ss` (the modern replacement) if `netstat` isn't installed.
# Attackers look for ports bound to 127.0.0.1 — these are internal-only services
# invisible from outside. Classic finds: databases (3306, 5432), admin panels,
# internal APIs, or custom applications running as root.
netstat -tlnp 2>/dev/null || ss -tlnp 2>/dev/null

echo ""

echo "========== ENUMERATION COMPLETE =========="
