import asyncio
from telos_core_v1.2 import TelosCore

async def run():
    core = TelosCore()

    print("=== Session 1: 你这方案根本不行！ ===")
    await core.process("你这方案根本不行！")

    print("\n=== Session 2: 我还是觉得不太对劲。 ===")
    await core.process("我还是觉得不太对劲。")

    print("\n=== Session 3: 还是按原计划，画个能量分布图看看 ===")
    await core.process("还是按原计划，画个能量分布图看看")

    await asyncio.sleep(1)
    print("\n✅ 记忆修正 + 跨模态抢跑全部完成！请查看 assets/ 目录。")

asyncio.run(run())
