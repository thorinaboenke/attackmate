#!/bin/bash
# Simple privilege escalation enumeration script for training exercises.
# A lightweight alternative to linpeas that runs quickly and offline.

echo "========== SYSTEM INFO =========="
id
hostname
uname -a
cat /etc/issue

echo ""
echo "========== SUID BINARIES =========="
find / -perm -4000 -type f 2>/dev/null

echo ""
echo "========== WRITABLE DIRECTORIES =========="
find / -writable -type d 2>/dev/null | head -20

echo ""
echo "========== INTERESTING FILES =========="
ls -la /etc/shadow 2>/dev/null
ls -la /etc/sudoers 2>/dev/null
ls -la /root 2>/dev/null

echo ""
echo "========== RUNNING SERVICES =========="
ps aux 2>/dev/null | head -30

echo ""
echo "========== NETWORK CONNECTIONS =========="
netstat -tlnp 2>/dev/null || ss -tlnp 2>/dev/null

echo ""
echo "========== ENUMERATION COMPLETE =========="
