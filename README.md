# Raspberry Pi MIC

Activate venv

```bash
.venv/bin/activate
```
```windows
.venv/Scripts/activate
```
Install Raspberry PI dependencies

```bash
sudo apt-get update 
sudo apt-get upgrade 
sudo apt-get install libhdf5-dev -y
sudo apt-get install libhdf5-serial-dev -y
sudo apt-get install libatlas-base-dev -y
sudo apt-get install libjasper-dev -y
sudo apt-get install libqtgui4 -y
sudo apt-get install libqt4-test -y
sudo apt-get install libsdl2-image-2.0-0 -y
sudo apt-get install libsdl2-ttf-2.0-0 -y
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev -y
```

Install requirements

```bash
pip install -r requirements.txt
```
