apt-get update && \
apt-get install -y libglib2.0 libnss3 libgconf-2-4 libfontconfig1 && \
apt-get update && \
apt-get install -y gnupg wget curl unzip --no-install-recommends && \
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
apt-get update -y && \
apt-get install -y google-chrome-stable && \
wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
ln -fs /usr/local/bin/chromedriver /usr/bin/chromedriver
