import asyncio
from telos_core_v1.2 import TelosCore


async def run():
    core = TelosCore()

    print("=== Session 1: 你这方案根本不行！ ===")
    r1 = await core.process("你这方案根本不行！")
    print(r1)

    print("\n=== Session 2: 我还是觉得不太对劲。 ===")
    r2 = await core.process("我还是觉得不太对劲。")
    print(r2)

    print("\n=== Session 3: 还是按原计划，画个能量分布图看看。 ===")
    r3 = await core.process("还是按原计划，画个能量分布图看看。")
    print(r3)

    # 给抢跑渲染一点点时间，确保文件真正落盘
    await asyncio.sleep(1.0)
    print("\n✅ 记忆修正 + 意图抢跑绘图演示全部完成！请查看 assets/ 目录。")


if __name__ == "__main__":
    asyncio.run(run())
