echo 'Welcome to catbot instller'
echo 'Now installing update...'
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install python3.5-dev -y
sudo apt-get install python3-pip -y
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo pip3 install numpy
sudo pip3 install scipy
sudo pip3 install sklearn
sudo pip3 install pyfirmata
sudo pip3 install matplotlib
sudo pip3 install imutils
sudo pip3 install argparse
echo 'Speech recognition installation'
sudo pip3 --no-cache-dir install SpeechRecognition
sudo apt-get install portaudio19-dev python3-all-dev python3-all-dev -y && sudo pip3 install pyaudio
echo 'Vision system installation....'
sudo apt-get install opencv-python3 -y
sudo pip3 install picamera
echo 'Pydrive installation'
sudo pip install Pydrive
sudo pip install google-api-python-client
sudo pip install googletrans
sudo pip3 install nltk
echo 'Complete installation'
