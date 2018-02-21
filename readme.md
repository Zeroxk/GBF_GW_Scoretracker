# Dependencies
Selenium
Pytz
Google-api-python-client

# Linux install
1. Symlink chromium with chrome, ln -s /usr/bin/chromium-browser /etc/alternatives/google-chrome
2. If on raspberry pi, install chromedriver from https://launchpad.net/ubuntu/trusty/+package/chromium-chromedriver (armhf builds)
copy from /usr/lib/chromium-browser/chromedriver to /usr/local/bin or export to PATH if necessary

# Using existing/creating new profile
Put chrome profile full path in config.json under key "profile_dir", login to your account if necessary.\
Steps to create a new profile with account credentials:
1. Run program once with "profile_dir" = ""
2. Login with your account
3. Type "chrome://version" in address bar
4. Copy "Profile Path" without "Default" at the end
5. Paste path into "profile_dir" in config.json
6. Remember to escape separators if needed

# TODO
- [ ] Better error handling
- [ ] Autogenerate sheets for each day with formatting (Not sure if API supports this)
- [ ] Better Logging
- [ ] Create setup.py
- [ ] Fetch final score
- [ ] Find a way to set values in discontinous cells per row? i.e A,B,C uploaded vals, D,E formulas, F,G uploaded vals again
- [ ] More accurate timer
- [ ] Accept configfilename as cmdline argument