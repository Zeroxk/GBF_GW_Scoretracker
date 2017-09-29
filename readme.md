# Linux install
1. Symlink chromium with chrome, ln -s /usr/bin/chromium-browser /etc/alternatives/google-chrome
2. If on raspberry pi, install chromedriver from https://launchpad.net/ubuntu/trusty/+package/chromium-chromedriver (armhf builds)
copy from /usr/lib/chromium-browser/chromedriver to /usr/local/bin or export to PATH if necessary

# TODO
1. Find number of recently online guildmembers
2. Config
3. Chrome profile
4. Error handling
5. Autogenerate sheets for each day with formatting
6. Logging