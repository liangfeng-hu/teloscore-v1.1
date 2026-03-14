from telos_core import TelosState, telos_step
import time

print("\n=== Session 1: write conflict into EverMemOS ===")
state1 = TelosState()
res1, _ = telos_step("你这方案根本不行，完全是错的！", state1, component_history_override=[])
print(res1)

time.sleep(2)

print("\n=== Session 2: restore memory and bias decision ===")
state2 = TelosState()
res2, _ = telos_step("我还是觉得不太对劲。", state2, component_history_override=[])
print(res2)
