from flask import Flask, request, render_template, redirect
from file2mail import makeMail, sendMail
from url2html import saveHTML, html2mobi

def url2mail(url, img, mobi):
    html_file = saveHTML(url, img, 'cache')
    if mobi:
        html2mobi(html_file)
        attached_file = html_file.rstrip('.html') + '.mobi'
    else:
        attached_file = html_file
    msg = makeMail(attached_file)
    sendMail(msg)

app = Flask(__name__)

@app.route('/s2k', methods=['GET', 'POST'])
def send2kindle():
    if request.method == 'GET':
        url = request.args.get('url')
        mobi = request.args.get('mobi')
        img = request.args.get('img')
        go_back = request.referrer
        if img == 'true':
            img = True
        else:
            img = False

        if url:
            url2mail(url, img, mobi)
            if go_back:
                return redirect(request.referrer)
            else:
                return 'done'
        else:
            return render_template('send2kindle.html')
    elif request.method == 'POST':
        url = request.form['url']
        mobi = request.form['mobi']
        url2mail(url, mobi)
        return 'done'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

