cd ~
rm -rf ~/r1_ws
git clone https://github.com/SamnangKong426/r1_ws.git
cd ~/r1_ws
rm -rf build/ log/ install/

colcon build
source ~/r1_ws/install/setup.bash