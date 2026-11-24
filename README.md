# robotics-baby-steps

Sandbox for learning robotics with zero global pollution. Two independent paths — use either or both:

- **Path A — MuJoCo physics lab** (default): everything lives in a project-local `uv` virtualenv. No Docker, no apt, no `/opt`.
- **Path B — ROS 2 + Gazebo**: one container with a browser-accessible desktop (noVNC), so the GUI never touches your host session.

## Path A: MuJoCo physics lab

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

Watch it live instead (interactive viewer, real-time playback):

```bash
uv run scripts/hello_arm.py --viewer               # native window
uv run scripts/hello_arm.py --viewer --seconds 30  # longer playback
```

...or watch it on the Path B browser desktop — the project folder is mounted at
`/workspace` inside the container:

```bash
python3 -m venv /tmp/mj && /tmp/mj/bin/pip install mujoco   # once per container
DISPLAY=:99 /tmp/mj/bin/python scripts/hello_arm.py --viewer
```

Extend from here:

- `uv add <package>` — dependencies stay in this folder's `.venv`
- robot models: drop MJCF files from
  [mujoco_mjcf menagerie](https://github.com/google-deepmind/mujoco_menagerie) into `models/`
- later ROS 2 bridge: [`mujoco_ros2_control`](https://github.com/ros-controls/mujoco_ros2_control)
  (ros-controls org, supports Lyrical) runs standard `ros2_control` controllers against MuJoCo

## Path B: ROS 2 + Gazebo in a container

```bash
mise run sim-up          # first build pulls the image (~3 GB)
                         # (or: docker compose -f docker/compose.yaml up --build -d)
open http://localhost:6080   # noVNC: full desktop in your browser
mise run sim-shell       # shell inside the container
mise run sim-down        # stop it again
```

Inside that shell:

```bash
source /opt/ros/lyrical/setup.bash
ros2 run turtlesim turtlesim_node                                              # smoke test
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf"                   # Gazebo
```

The browser view opens a real desktop — openbox + an xterm over Xvfb, all
managed by supervisord — with no dependency on your host display server. The
first thing you see is a terminal ready for `ros2` commands, and Path A's
`--viewer` runs there too.

### Design notes

- `network_mode: host` — ROS 2 DDS discovery uses UDP multicast, which Docker's
  default bridge does not pass.
- noVNC binds `127.0.0.1` only (see `docker/supervisord.conf`); it is never
  exposed off your machine.
- The virtual display is `:99`, not `:0`: with `network_mode: host` the container
  shares the host's abstract socket namespace, where the host X server already
  holds `@/tmp/.X11-unix/X0` and `X1` — Xvfb on `:0` refuses to start there.
- `ROS_DOMAIN_ID=42` isolates this container's ROS graph from anything else on
  the host.
- To talk to host-side ROS nodes later, run them with the same `ROS_DOMAIN_ID`.

## Layout

```
├── mise.toml               # tool versions (uv) + task runner
├── pyproject.toml          # uv project: mujoco + numpy, nothing global
├── scripts/hello_arm.py    # Path A entry point (headless or --viewer)
├── models/two_link_arm.xml # minimal 2-DOF arm MJCF
└── docker/                 # Path B: ROS 2 Lyrical + Gazebo + noVNC
    ├── Dockerfile
    ├── compose.yaml
    └── supervisord.conf    # Xvfb :99 → openbox/xterm → x11vnc → noVNC
```
