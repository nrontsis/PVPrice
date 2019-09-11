# PVPrice
Log prices from pvinsights

# Get historical prices for PVInsights
Install [`wayback-machine-downloader`](https://github.com/hartator/wayback-machine-downloader) with 
```
gem install wayback_machine_downloader
```
Then, run 
```
EXECUTABLE_DIRECTORY/wayback_machine_downloader -e -s http://pvinsights.com/
EXECUTABLE_DIRECTORY/wayback_machine_downloader -e -s http://pvinsights.com/index.php
```
where `EXECUTABLE_DIRECTORY` is obtained by running `gem env`.

The above will save all the main pages stored in [Wayback Machine](http://web.archive.org) for `http://pvinsights.com/`. For some (unknown) reason, some of them are cached by the Wayback Machine in `.html` files and some of them in `.php` files which are actually `html` files. For convenience we will  convert all of them to `.html` extension via running:
```
find . -name "*.php" -exec rename 's/\.php$/.html/' '{}' \;
```
At that point you should have all the past versions of the website in the folder `websites`.

# Automatic price download on a weekly basis
The prices from `pvinsights.com` and `energytrends.com` can be downloaded automatically simply by running the python script `download.py`.

In MacOS `launchd` can be used to run this script on a weekly basis as following.
Save the following file in `~/Library/LaunchAgents/com.price_download.app.plist`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>Label</key>
		<string>com.price_download.app</string>
		<key>RunAtLoad</key>
		<true/>
		<key>StandardErrorPath</key>
		<string>/Users/nrontsis/PVPrice/stderr.log</string>
		<key>StandardOutPath</key>
		<string>/Users/nrontsis/PVPrice/stdout.log</string>
		<key>ProgramArguments</key>
		<array>
			<string>/Users/nrontsis/anaconda/bin/python</string>
			<string>/Users/nrontsis/PVPrice/download.py</string>
		</array>
		<!-- Run every Saturday (weekday 6) at 10:00AM -->
		<key>StartCalendarInterval</key>
		<dict>
			<key>Weekday</key>
			<integer>6</integer>
			<key>Hour</key>
			<integer>10</integer>
			<key>Minute</key>
			<integer>00</integer>
		</dict>
	</dict>
</plist>
```
Then, run in the terminal the following commands:
```shell
launchctl load ~/Library/LaunchAgents/com.price_download.app.plist
```
If this launchd service has been loaded/started before you might need to execute the following commands first to stop/unload it:
```shell
launchctl unload ~/Library/LaunchAgents/com.price_download.app.plist
```
See [this](https://medium.com/@chetcorcos/a-simple-launchd-tutorial-9fecfcf2dbb3) tutorial for more details. Note that the paths in the launchd xml must be absolute.