# Path A: MuJoCo physics lab

Everything lives in a project-local `uv` virtualenv — no Docker, no apt, no `/opt`.

## Workflow

Tool versions and tasks are managed by [mise](https://mise.jdx.dev) (`mise.toml`):

```bash
mise install             # fetches the pinned uv toolchain
mise run setup           # uv sync → ./.venv (project-local, nothing global)
mise run demo            # headless 8 s simulation of the two-link arm
```

Without mise, plain [`uv`](https://docs.astral.sh/uv/) works identically:

```bash
uv sync && uv run scripts/hello_arm.py
```

`scripts/hello_arm.py` steps a simulation of `models/two_link_arm.xml`
(a 2-DOF planar arm) and prints joint angles + end-effector position. Headless
by default: no display needed, deterministic, runs in well under a second.

## Viewer mode

Watch it live instead (interactive viewer, real-time playback):

```bash
uv run scripts/hello_arm.py --viewer               # native window
uv run scripts/hello_arm.py --viewer --seconds 30  # longer playback
```

...or watch it on the [Path B](path-b-ros-gazebo.md) browser desktop — the
project folder is mounted at `/workspace` inside the container:

```bash
python3 -m venv /tmp/mj && /tmp/mj/bin/pip install mujoco   # once per container
DISPLAY=:99 /tmp/mj/bin/python scripts/hello_arm.py --viewer
```

## Extending

- `uv add <package>` — dependencies stay in this folder's `.venv`
- robot models: drop MJCF files from
  [mujoco_mjcf menagerie](https://github.com/google-deepmind/mujoco_menagerie) into `models/`
- later ROS 2 bridge: [`mujoco_ros2_control`](https://github.com/ros-controls/mujoco_ros2_control)
  (ros-controls org, supports Lyrical) runs standard `ros2_control` controllers against MuJoCo
