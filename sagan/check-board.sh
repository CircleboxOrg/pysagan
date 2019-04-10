sudo rm /usr/local/lib/python3.5/dist-packages/sagan/imu.py
sudo rm /usr/local/lib/python3.5/dist-packages/sagan/__init__.py

if i2cdetect -y 1 | grep -i 1e
then
  sudo ln -sf /usr/local/lib/python3.5/dist-packages/sagan/imu4.py /usr/local/lib/python3.5/dist-packages/sagan/imu.py
  sudo ln -sf /usr/local/lib/python3.5/dist-packages/sagan/__init__4.py /usr/local/lib/python3.5/dist-packages/sagan/__init__.py
elif i2cdetect -y 1|grep -i 1d
then
  sudo ln -sf /usr/local/lib/python3.5/dist-packages/sagan/imu3.py /usr/local/lib/python3.5/dist-packages/sagan/imu.py
  sudo ln -sf /usr/local/lib/python3.5/dist-packages/sagan/__init__3.py /usr/local/lib/python3.5/dist-packages/sagan/__init__.py
fi
