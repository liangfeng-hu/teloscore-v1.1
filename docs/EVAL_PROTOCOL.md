# Evaluation Protocol

This repository distinguishes between two evidence classes:

## A. Reproducible evidence
These artifacts are directly reproducible from the repository:
- `python demo_script.py`
- `python auto_make_figs.py`
- `assets/00_triptych.png`
- two-session memory persistence and correction logs
- `docs/TelosCore_v1.1.pdf`

## B. Internal / non-official evaluation
Any simulated or internal metric must be treated as non-official unless it is reproduced with a public benchmark protocol.

Examples:
- internal sanity checks
- local ablation tests
- custom evaluation scripts

## Repository claim policy
The repository should only claim:
- what is implemented in code
- what is reproducible from the public repository
- what is directly shown in the demo video

The repository should not claim:
- official benchmark superiority unless publicly reproduced
- complete production sealing of audit / digest / commit layers unless fully implemented
- unsupported competition scores

## Minimal acceptable competition evidence
A valid minimal evidence chain includes:
1. memory persistence
2. memory retrieval
3. memory-aware U correction
4. action shift caused by memory
