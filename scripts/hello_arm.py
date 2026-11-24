"""Two-link arm demo: steps the sim and prints joint/tip state.

Run from the project root:

    uv run scripts/hello_arm.py            # headless (default)
    uv run scripts/hello_arm.py --viewer   # interactive viewer window
"""

import argparse
import time
from pathlib import Path

import mujoco
import numpy as np

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "two_link_arm.xml"


def control(t: float) -> np.ndarray:
    """Sinusoidal shoulder/elbow torques."""
    return np.array(
        [
            1.5 * np.sin(2 * np.pi * 0.25 * t),
            1.0 * np.sin(2 * np.pi * 0.40 * t + 1.0),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--viewer", action="store_true", help="open the interactive MuJoCo viewer window"
    )
    parser.add_argument("--seconds", type=float, default=8.0, help="simulated duration")
    args = parser.parse_args()

    model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
    data = mujoco.MjData(model)
    tip_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SITE, "tip")
    if tip_id < 0:
        raise SystemExit("site 'tip' not found in model")

    dt = model.opt.timestep
    print(f"model: {model.nq} DoF, {model.nu} actuators, dt={dt}s")

    def step_and_report(step: int) -> None:
        t = step * dt
        data.ctrl[:] = control(t)
        mujoco.mj_step(model, data)
        if step % 1000 == 0:
            tip = data.site_xpos[tip_id]
            print(
                f"t={t:4.1f}s  q=[{data.qpos[0]:+.3f} {data.qpos[1]:+.3f}]"
                f"  tip=({tip[0]:+.3f}, {tip[1]:+.3f}, {tip[2]:+.3f})"
            )

    nsteps = int(args.seconds / dt)

    if args.viewer:
        # `from ... import` binds only mj_viewer — a plain `import mujoco.viewer`
        # here would make `mujoco` local to this function and break the lines above.
        from mujoco import viewer as mj_viewer

        # Wall-clock pacing so playback is watchable (sim itself is far faster).
        with mj_viewer.launch_passive(model, data) as view:
            for step in range(nsteps + 1):
                step_and_report(step)
                view.sync()
                time.sleep(dt)
    else:
        for step in range(nsteps + 1):
            step_and_report(step)

    print(f"done: {data.time:.1f}s simulated, {round(data.time / dt)} steps")


if __name__ == "__main__":
    main()
