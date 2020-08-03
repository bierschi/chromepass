# chromepass
-


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



## Logs

logs can be found in `/var/log/chromepass`

## Troubleshooting
- add your current user to group `syslog`, this allows the application to create a folder in
`/var/log`. Replace `<user>` with your current user
<pre><code>
sudo adduser &lt;user&gt; syslog
</code></pre>
to apply this change, log out and log in again and check with the command `groups` <br>


## Changelog
All changes and versioning information can be found in the [CHANGELOG](https://github.com/bierschi/chromepass/blob/master/CHANGELOG.rst)

## License
Copyright (c) 2020 Bierschneider Christian. See [LICENSE](https://github.com/bierschi/chromepass/blob/master/LICENSE)
for details
