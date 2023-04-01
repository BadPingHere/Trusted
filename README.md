
<h1 align="center">
  <br>
  <a href="https://github.com/BadPingHere/Trusted"><img src="https://cdn.discordapp.com/icons/673234977948827720/ae4a5e6d30634c97db71b8708f6377f2.webp" alt="Trusted" width="200"></a>
  <br>
  Trusted
  <br>
</h1>

<h4 align="center">A easy-to-use Scraper and Web UI  built on top of <a href="https://www.python.org/" target="_blank">Python</a> and <a href="https://www.php.net/" target="_blank">PHP</a> for the game <a href="https://www.playuntrusted.com/" target="_blank">Untrusted</a>.</h4>

This may not work on all opsec logs, as they have changed in the past and Knu has told me may change in the future. However this should be usuable on present logs.



<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#download">Download</a> •
  <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

![screenshot](https://cdn.upload.systems/uploads/pWkPA6n9.gif)

## Key Features

* Web Scraper
  - In seconds download an entire log.
  - Works for most types of logs
  - Includes an automatic feature, just in case you dont know when a log was created.
  - Simple, easy to use.
* Web UI
  - A 1 to 1 recreation of the Untrusted UI, in a browser.
  - Admin mode, to see what most cant see.
  - Easily change days and users.
* Multi-Browser use
  - Works on both Chromium based browser like Chrome and Edge, along with Quantum based browsers like Firefox and Tor. 
* Cross platform
  - Windows, macOS and Linux ready.

## How To Use

To clone and run this application, you'll need [Git](https://git-scm.com), [Python 3.9](https://www.python.org/) (which comes with [pip](https://pypi.org/project/pip/))  and [PHP](https://www.php.net/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/BadPingHere/Trusted

# Go into the repository
$ cd Trusted

# Install dependencies
$ pip install -r requirements.txt
$ py installassets.py

# Run the app
$ py scraper.py
```
> **Note:**
> If you intend to use the web ui, go into the file called 'settings.ini', and change the value of 'use_php' from 0 to 1. You should also configure and use any choice of local web hosting, for example, xaamp, using this [tutorial](https://www.geeksforgeeks.org/how-to-run-php-programs). To add, I made this around my default zoom on browser, 90%, so for the true ui experince, please use fullscreen and 90% zoom.

## Download

You can [download](https://github.com/BadPingHere/Trusted/releases/tag/v1.1) the latest installable version of Trusted for Windows, macOS and Linux.

## Credits

This software uses the following open source packages:

- [Python](https://www.python.org/)
- [Node.js](https://www.php.net/)
- [ConfigParser](https://github.com/jaraco/configparser/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://github.com/psf/requests)
- [Ascii-Magic](https://github.com/LeandroBarone/python-ascii_magic)

This software also uses the following assets from these people:
- Andrea Alessi

## License

MIT

---
> [badpinghere.live](https://badpinghere.live) &nbsp;&middot;&nbsp;
> GitHub [@BadPingHere](https://github.com/BadPingHere)&nbsp;&middot;&nbsp;
> Discord [Ping#6175](https://discordlookup.com/user/736028271153512489)

