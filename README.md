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