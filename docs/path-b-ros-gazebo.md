# Path B: ROS 2 + Gazebo in a container

One container — ROS 2 Lyrical, Gazebo, and a browser-accessible desktop (noVNC) —
so the GUI never touches your host session.

## Commands

```bash
mise run sim-up          # first build pulls the image (~3 GB)
                         # (or: docker compose -f docker/compose.yaml up --build -d)
open http://localhost:6080   # noVNC: desktop in your browser
mise run sim-shell       # shell inside the container
mise run sim-down        # stop it again
```

The browser view opens a real desktop — openbox + an xterm over Xvfb, all
managed by supervisord — with no dependency on your host display server. The
first thing you see is a terminal ready for `ros2` commands, and Path A's
`--viewer` runs there too ([how](path-a-mujoco.md#viewer-mode)).

## Inside the container

```bash
source /opt/ros/lyrical/setup.bash
ros2 run turtlesim turtlesim_node                                              # smoke test
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="empty.sdf -r"                # Gazebo (-r: start unpaused)
```

Notes on arguments:

- launch files take their own arguments as `name:=value` — there is no
  `--ros-args` on `ros2 launch`; that flag belongs to individual `ros2 run`
  node commands (e.g. `ros2 run turtlesim turtlesim_node --ros-args -p background_r:=255`).
- `empty.sdf` resolves from Gazebo's installed worlds; pass a full path for your
  own world files.

## Design notes

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

## Files

```
docker/
├── Dockerfile          # osrf/ros:lyrical-desktop + simulation + noVNC + desktop
├── compose.yaml        # host net, DDS-friendly, ROS_DOMAIN_ID=42
└── supervisord.conf    # Xvfb :99 → openbox/xterm → x11vnc → noVNC
```
