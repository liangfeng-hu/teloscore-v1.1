# Competition Evidence

This document summarizes the minimal reproducible evidence chain for the competition submission.

## Evidence 1: Persistent memory
The system stores state and event records into EverMemOS:

- `state_memory`
- `conflict_event`
- `clarify_event`
- `goal_event`

This enables cross-session persistence rather than in-memory-only behavior.

## Evidence 2: Memory-aware correction
On later runs, historical memory is retrieved from EverMemOS and converted into memory bias signals:

- `U_con_memory`
- `U_unc_memory`
- `U_tel_memory`

These signals modify the current cognitive state before action selection.

## Evidence 3: Decision shift
The system prints both:

- pure reactive decision
- memory-aware decision

This provides direct evidence that memory changes action selection.

## Reproduction steps
1. Start EverMemOS.
2. Start the API server.
3. Run `python demo_script.py`.
4. Observe the following runtime evidence in the console:
   - `[Memory Correction] U_con_memory=... | U_unc_memory=... | U_tel_memory=...`
   - `[EverMemOS] state persisted.`
   - `[EverMemOS] conflict_event persisted.` or `[EverMemOS] clarify_event persisted.`
   - `[Decision] Pure Reactive: ... -> Memory-Aware: ...`

## Expected interpretation
- The first session writes conflict or clarification events into EverMemOS.
- The second session retrieves historical memory and converts it into `u_memory` bias.
- The retrieved bias modifies the current U-vector before action selection.
- The final action is therefore memory-aware rather than purely reactive.

## Key files
- `evermemos_client.py`
- `telos_core.py`
- `demo_script.py`
- `assets/00_triptych.png`
- `docs/TelosCore_v1.1.pdf`
- `docs/FULL_MEMORY_ARCHITECTURE.md`
