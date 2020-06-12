#!/bin/bash
set -x
cd /etc/systemd/system
sudo ln -sf /home/pi/TweliteEnvMonitor/service/env_monitor.service
sudo ln -sf /home/pi/TweliteEnvMonitor/service/http_server.service
sudo ln -sf /home/pi/TweliteEnvMonitor/service/shutdown_button.service
sudo systemctl enable env_monitor.service
sudo systemctl enable http_server.service
sudo systemctl enable shutdown_button.service
