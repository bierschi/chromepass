# chromepass
- Fetching saved passwords from chrome database file
- Supports Windows and Linux Platform

<br>

![Alt Text](chromepass.gif)


## Installation

install [chromepass]() with pip
<pre><code>
pip3 install chromepass
</code></pre>

or from source
<pre><code>
git clone https://github.com/bierschi/chromepass
cd chromepass
sudo python3 setup.py install
</code></pre>


## Usage and Examples
Print the available arguments
<pre><code>
chromepass --help
</code></pre>
use it without any arguments
<pre><code>
chromepass
</code></pre>
or save the results to a file
<pre><code>
chromepass --file /home/christian/chromepass.txt
</code></pre>

## Executables

Install pyinstaller with

<pre><code>
pip3 install pyinstaller
</code></pre>

create exe file
<pre><code>
pyinstaller --onefile --name chromepass chromepass/main.py
</code></pre>

## Changelog
All changes and versioning information can be found in the [CHANGELOG](https://github.com/bierschi/chromepass/blob/master/CHANGELOG.rst)

## License
Copyright (c) 2020 Bierschneider Christian. See [LICENSE](https://github.com/bierschi/chromepass/blob/master/LICENSE)
for details
