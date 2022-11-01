# /bin/sh

rsync -anp --exclude 'venv' --exclude '.git' . pi@192.168.1.38:/home/pi/teleinfo 