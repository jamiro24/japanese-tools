# Installation

To use any of the tools in this repository you are required to have [Python3](https://www.python.org/downloads/)
installed on your computer. If the Python3 installer asks whether you want to add something to PATH, make sure to do so. Furthermore, since these tools make use of some Python packages you also need to install
[pip](https://bootstrap.pypa.io/get-pip.py) (right-click->save link as... and then run the file). Finally, either clone 
or download this repository. If you downloaded this repository, unzip it to where you want to. 

Now that you have the required tools on your computer, you need to install the Python packages. Open the folder that
contains the tools you just downloaded and open a command prompt in this folder. (For windows, hold shift, right-click
in the folder (not on a file) and press 'Open PowerShell window here'). Once you have the
command prompt open, enter the following command:
```
pip install -r requirements.txt
```

You are now ready to use the tool!

# Usage

This section explains what each of the tools do, and how to use them.
## Anki Kanji Scraper

Creating anki decks can be cumbersome, so this tool was created to help with this.

It takes any file and searches for all unique kanji characters and then gathers info like the character's meaning and 
reading and saves all this info in a file which can be imported into anki.

for example a file containing the character 今 will output the following:

|Kanji	| Grade	| jlpt level | strokes | meanings | on-reading	| kun-reading |
|-------|-------|------------|---------|----------|-------------|-------------|
|今	    |1	    |4           |4	       |now	      |コン, キン   	|いま

### How to run

To use this tool, simply double-click on _anki-kanji-scraper.py_. In the console window that is opened, the tool will 
guide you through the process. Finally, the tool outputs a file called _Output.tsv_, which is importable into Anki.

It is also possible to add some of your own data to the output of this tool. This is optional. To use this feature, 
you need a _.tsv_ or a _.csv_ file with at least a column that contains Kanji characters and one or more columns
containing data you want to append to the Kanji rows of this tool's output.

# Contributions

If you want to contribute to this repository, feel free to do so! You can make a pull-request and if it's good enough I will merge it into the repository. It might be smart to first make an issue, where we can discuss the functionality you want to add.
