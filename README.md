# ESP32-Imu-Bridge
ROS2 package to bridge ESP32 IMU orientation data and visualize a 3D airplane model in RViz2

1) Install ROS2 Dependencies and Plugins
Terminal

Open your terminal and install all required ROS2 packages, visualization tools, and filters. Replace <ros-distro> with your actual ROS2 distribution name (e.g., humble, iron, or jazzy)
(I have used Jazzy for my Project)

Bash:

sudo apt update
sudo apt install ros-<ros-distro>-rclpy 
sudo apt install ros-<ros-distro>-sensor-msgs 
sudo apt install ros-<ros-distro>-xacro 
sudo apt install ros-<ros-distro>-imu-filter-madgwick 
sudo apt install ros-<ros-distro>-robot-state-publisher 
sudo apt install ros-<ros-distro>-rviz2 
sudo apt install ros-<ros-distro>-rviz-imu-plugin 
pip install python3-serial

2) Create Workspace and Source Folder

Bash:

mkdir -p ~/esp32_ws/src
cd ~/esp32_ws/src


3) Clone Your Repository

Bash

git clone https://github.com/kesavan0101/esp32_imu_bridge.git

4) Connect ESP32 and Verify Serial Port

Plug your ESP32 into your computer via USB. Check which serial port has been assigned to it by running:

Bash:

ls /dev/ttyUSB* /dev/ttyACM*

4) Update the Port Parameter in the Launch File

Open your cloned package's launch file (located in esp32_imu_bridge/launch/) and update the serial port parameter to match the port you found in the previous step (e.g., /dev/ttyUSB0).
(For me it was /dev/ttyUSB2)
   
Verification: Check that the port parameter in your launch file matches your active device path.

5)Build with Symlink, Source, and Launch

Bash

cd ~/esp32_ws
colcon build --packages-select esp32_imu_bridge --symlink-install
source install/setup.bash
ros2 launch esp32_imu_bridge gyro.launch.xml

Finally you will have a screen like this:
<img width="800" height="516" alt="ezgif-6ee2474ad3f03a70" src="https://github.com/user-attachments/assets/f1b77770-0302-4980-9117-574e3687a068" />

