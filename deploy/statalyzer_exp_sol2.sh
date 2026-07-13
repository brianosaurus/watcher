#!/bin/bash
# Launcher for statalyzer exp_sol2 (LIVE). Installed to ~/statalyzer/exp_sol2_run.sh.
# Idempotent-ish: if a process with exp_sol2.db is already running, does nothing.
set -e
cd /home/ubuntu/statalyzer

if pgrep -af "statalyzer\.py.* --db exp_sol2\.db" | grep -v grep | grep -v bash >/dev/null; then
  echo "[$(date -u)] exp_sol2 already running" >> logs/exp_sol2.log
  exit 0
fi

mkdir -p logs
echo "[$(date -u)] starting exp_sol2" >> logs/exp_sol2.log
source ~/venv/bin/activate
nohup python3 -u statalyzer.py --monitor --live --confirm-live \
    --scanner-db ../arbitrage_tracker/arb_tracker.db \
    --slippage-bps 3 --min-spread-bps 15 --max-basket-size 2 \
    --exit-z 0.1 --stop-z 4.0 \
    --max-positions 5 --max-per-token 2 --max-per-hour 30 \
    --candle-interval 30 --max-hl 7200 \
    --direction both \
    --entry-z 1.1 --max-entry-z 1.25 \
    --short-entry-z 1.0 --short-max-entry-z 1.4 \
    --min-correlation 0.90 --short-min-correlation 0.50 --long-min-correlation 0.90 \
    --long-exclude-tokens stSOL,RAY,BONK \
    --short-exclude-tokens JUP,ETH \
    --blocked-hours 14,15,20 \
    --token-whitelist SOL,bSOL,jitoSOL,mSOL,jupSOL,stSOL,JUP,ETH,RAY,BONK,ORCA,MEW,INF,PENGU,KMNO \
    --no-lunar-lander \
    --fixed-fraction 0.25 --max-exposure 2.0 \
    --db exp_sol2.db \
    >> logs/exp_sol2.log 2>&1 </dev/null &
disown
