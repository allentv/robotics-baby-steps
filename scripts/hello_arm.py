"""Headless two-link arm demo: steps the sim and prints joint/tip state.

Run from the project root:

    uv run scripts/hello_arm.py
"""

from pathlib import Path

import mujoco
import numpy as np

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "two_link_arm.xml"


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    tip_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SITE, "tip")
    if tip_id < 0:
        raise SystemExit("site 'tip' not found in model")

    dt = model.opt.timestep
    print(f"model: {model.nq} DoF, {model.nu} actuators, dt={dt}s")

    for step in range(4001):  # 8 simulated seconds
        t = step * dt
        data.ctrl[0] = 1.5 * np.sin(2 * np.pi * 0.25 * t)
        data.ctrl[1] = 1.0 * np.sin(2 * np.pi * 0.40 * t + 1.0)
        mujoco.mj_step(model, data)
        if step % 1000 == 0:
            tip = data.site_xpos[tip_id]
            print(
                f"t={t:4.1f}s  q=[{data.qpos[0]:+.3f} {data.qpos[1]:+.3f}]"
                f"  tip=({tip[0]:+.3f}, {tip[1]:+.3f}, {tip[2]:+.3f})"
            )

    print(f"done: {data.time:.1f}s simulated, {round(data.time / dt)} steps")


if __name__ == "__main__":
    main()
