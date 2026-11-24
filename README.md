# robotics-baby-steps

Sandbox for learning robotics with zero global pollution — a project-local
MuJoCo physics lab and a ROS 2 + Gazebo container you can drive from a browser.

```bash
git clone https://github.com/allentv/robotics-baby-steps.git && cd robotics-baby-steps

# Path A — MuJoCo, headless sim in a project-local venv
mise install && mise run demo

# Path B — ROS 2 + Gazebo desktop in your browser
mise run sim-up   # then open http://localhost:6080
```

## Docs

- [docs/path-a-mujoco.md](docs/path-a-mujoco.md) — viewer mode, extending the sim, ROS 2 bridge
- [docs/path-b-ros-gazebo.md](docs/path-b-ros-gazebo.md) — container desktop, ROS/Gazebo commands, design notes
