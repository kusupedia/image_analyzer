# beforesetup
ubuntu
```
sudo apt-get update
sudo apt-get cmake
sudo apt install python-dev
pip install -r requirements.txt
```

```
sudo vi /etc/apt/sources.list

# Copy the first line "deb http://archive.ubuntu.com/ubuntu bionic main" and paste it as shown below on the next line.
# If you are using a different release of ubuntu, then replace bionic with the respective release name.

deb http://archive.ubuntu.com/ubuntu bionic universe
```

```
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
sudo apt install tesseract-ocr-jpn
sudo apt install tesseract-ocr-script-jpan
```

centos
```
sudo yum install cmake
yum install python-devel
pip install -r requirements.txt

yum-config-manager --add-repo https://download.opensuse.org/repositories/home:/Alexander_Pozdnyakov/CentOS_7/
sudo rpm --import https://build.opensuse.org/projects/home:Alexander_Pozdnyakov/public_key
yum update
yum install tesseract 
yum install tesseract-langpack-jpn
```

# unittest
```
python -m unittest discover
```
