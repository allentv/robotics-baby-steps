# ROS 2 Lyrical + Gazebo + browser desktop (noVNC)
# Desktop provides RViz/turtlesim; simulation variant adds the Gazebo stack.
FROM osrf/ros:lyrical-desktop

RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-lyrical-simulation \
        novnc \
        xvfb \
        x11vnc \
        websockify \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY supervisord.conf /etc/supervisor/conf.d/novnc.conf

EXPOSE 6080
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
