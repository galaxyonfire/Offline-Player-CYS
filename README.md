# Offline Story Player for [chooseyourstory.com](chooseyourstory.com)

A tool to download a story from [chooseyourstory.com](http://chooseyourstory.com) (CYS) to play offline

By galaxyonfire on Github.com

### Overview

This a python script built using Python 3.7.6 and [MechanicalSoup](https://github.com/MechanicalSoup/MechanicalSoup) that searches through a story from CYS and rebuilds the story on your local device. You only need one piece of info to get the script running and that is the link to story you want to play.

As an example, consider the story *Eternal* by EndMaster. The link for that story is [http://chooseyourstory.com/story/eternal](http://chooseyourstory.com/story/eternal).

With this link in hand, if we look at line 8 of the script we'll see a `STORY_LINK` variable. Simply paste the link of the story your desire between the two single quotes and run the script to download the story offline.

So for the above example line 8 should be `STORY_LINK = 'http://chooseyourstory.com/story/eternal'`

### Installation

The script requires your machine to have python 3.x, pip and a rudimentary understanding of the CLI. If you have no idea what those are that is ok, here are some resources to get started:
* [Quick intro to CLI](https://www.w3schools.com/whatis/whatis_cli.asp)
* Might I introduce you to [Anaconda](https://www.anaconda.com/distribution/) to help manage python if you've never programmed before.
* [Window's](https://www.howtogeek.com/197947/how-to-install-python-on-windows/) specific and [macOS](https://docs.python-guide.org/starting/install3/osx/) specific guides if you want a more in-depth option

Open your CLI in some directory and type `pip install mechanicalsoup` and hit enter to install MechanicalSoup if you haven't before. Note that if you are using Anaconda you must open the Anaconda Navigator, click on Environments, then on the play button next to base(root) to access python/pip through the CLI.

Windows example:
```
C:\Users\You\Desktop> pip install mechanicalsoup
...
Successfully installed... mechanicalsoup
```

Or on Anaconda:
```
(base) C:\Users\You\Desktop> pip install mechanicalsoup
...
Successfully installed... mechanicalsoup
```

Afterwards download the story_download.py file and edit the `STORY_LINK` to your desired story.

### Usage

Open the CLI that has access to python in the directory of story_download.py. Now simply run `python story_download.py` and after a few minutes your story should be downloaded for offline viewing!

In the same directory of the story_download.py file, there should be a "Play_the_story_title.html". Simply open that file with your desired web browser and enjoy!

### Notes

* Currently the script doesn't support games with inventory or images (i.e. it won't download images or save inventory).
* Clicking 'Save' won't save your current progress locally but will instead tell you the current HTML file you are viewing in the Story_Data/the_story_title folder. Simply note that file and reopen it later to resume your progress.
