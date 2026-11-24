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
        openbox \
        xterm \
        x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

# Ubuntu's novnc package ships no index.html, so http://localhost:6080/ would
# show a bare directory listing instead of the noVNC client.
RUN ln -s vnc.html /usr/share/novnc/index.html

COPY supervisord.conf /etc/supervisor/conf.d/novnc.conf

EXPOSE 6080
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
