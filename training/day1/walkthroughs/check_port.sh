#!/bin/bash
# Helper script for the "break out of a loop" walkthrough.
# Simulates checking whether a port is open.
# Prints "yes" for port 22, "no" for everything else.

PORT="${1:-0}"

if [ "$PORT" -eq 22 ]; then
    echo "yes"
else
    echo "no"
fi
