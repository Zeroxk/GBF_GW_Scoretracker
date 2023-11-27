# Setup virtualenv and install dependencies
```
pip install virtualenv
virtualenv scoretracker
scoretracker\Scripts\activate
pip install -r requirements.txt
```

# How to run
`python main.py -c <configFile>`

# Linux install
1. Symlink chromium with chrome, ln -s /usr/bin/chromium-browser /etc/alternatives/google-chrome
2. Install package(might not be available depending on distro)
```
sudo apt-get install chromium-chromedriver
```
3. Copy from /usr/lib/chromium-browser/chromedriver to /usr/local/bin or export to PATH if necessary

# Using existing/creating new profile
Put chrome profile full path in config.json under key "profile_dir", login to your account if necessary.\
Steps to create a new profile with account credentials:
1. Run program once with "profile_dir" = ""
2. Login with your account
3. Type "chrome://version" in address bar
4. Copy "Profile Path" without "Default" at the end
5. Paste path into "profile_dir" in config.json
6. Remember to escape separators if needed
