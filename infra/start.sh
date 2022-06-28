#!/bin/bash

echo -ne "[\x1b[94m+\x1b[0m] Starting challenges deploy\n"
/bin/bash /challenges/._run.sh
echo -ne "[\x1b[94m+\x1b[0m] Starting tournament\n"
python3 /app/app.py