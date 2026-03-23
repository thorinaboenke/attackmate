#!/bin/bash
# Helper script for the "loop until a condition" walkthrough.
# Randomly prints "done" or "pending" so the loop
# runs a non-deterministic number of iterations.

if (( RANDOM % 3 == 0 )); then
    echo "done"
else
    echo "pending"
fi
