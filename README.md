# install
```bash
git clone https://github.com/gahoo/send2kindle
cd send2kindle
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
wget -i links.txt
tar -xf kindlegen_linux_2.6_i386_v2_9.tar.gz
vim config.yaml
```

# usage
```bash
# get web page and convert
python url2html.py --url https://zh.wikipedia.org/wiki/Kindle --prefix cache --mobi
# send via email
python file2mail.py --file cache/Kindle\ -\ Wikipedia.mobi
python file2mail.py --file cache/Kindle\ -\ Wikipedia.html
# host send2kindle api on http://IP:5000/s2k
python send2kindle.py
```

# bookmarklet
Open bookmarklet.js then edit host and port. Copy and create bookmarklet with https://mrcoles.com/bookmarklet/. Then you can save web pages with one click.

# reference
https://github.com/moshfiqur/html2mobi

https://mrcoles.com/bookmarklet/
