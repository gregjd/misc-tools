# ride-schools

There are a number of steps in this process, some automated and some manual.


## Getting the master directory HTML

Go to the [RIDE master directory table](http://www2.ride.ri.gov/Applications/MasterDirectory/Organization_List.aspx). You should see a long list with hundreds of entries. If you don't, then go [here](http://www2.ride.ri.gov/Applications/MasterDirectory/) and click `Search`.



## Getting Python set up properly

You're going to need to make sure you have [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/) installed. It's a Python library used for parsing web pages.

Open up a terminal window. You can do this on a Windows machine by clicking on the Start button and searching for `cmd`.

Try typing `python` in the terminal window. If you get this message:

```
'python' is not recognized as an internal or external command, operable program or batch file.
```

then you will need to add Python to your PATH. Because of the way Python is installed on our computers, you will probably need to type `set PATH=%PATH%;C:\Python27\ArcGIS10.2\` in the terminal window; the correct folder path should lead to a folder with contents like these:

![Python folder](/images/python_folder.png)

You will know it's working properly if typing `python` no longer gives you an error message and instead gives a Python version number and command prompt. Get out of this prompt by typing `exit()`.

![Python prompt](/images/python_prompt.png)

Now, we need to install the Beautiful Soup 4 module on your machine, if it isn't already installed. The easiest way to do this is by using `pip`, [the recommended tool](https://pypi.python.org/pypi/pip) for installing Python packages.

First, you'll need to be sure `pip` is installed. You can do this by typing `python -m pip` on the command line. If you get a bunch of usage instructions returned, then you're good to go. If you get an error message, then you'll need to install `pip`. Instructions on how to do that can be found [here](https://pip.pypa.io/en/stable/installing/) or [here](http://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows/12476379#12476379)

For Beautiful Soup 4, you can see if you have it installed by typing `python -m pip show beautifulsoup4`. If it doesn't return metadata like the version number, then type `python -m pip install beautifulsoup4`. Voila!






Once you get to the point where you're making manual edits, pretty much everything will be manual, since making any automated changes would require merging those with your manual edits, and while that's certainly possible, you need to be really careful with it.