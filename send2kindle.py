from flask import Flask, request, render_template, redirect
from file2mail import makeMail, sendMail
from url2html import saveHTML, html2mobi, download_pdf

def url2mail(url, img, mobi):
    if '.pdf' in url:
        attached_file = download_pdf(url, 'cache')
    else:
        attached_file = saveHTML(url, img, 'cache')

    if mobi:
        html2mobi(attached_file)
        attached_file = attached_file.rstrip('.html') + '.mobi'

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
        mobi = request.form.get('mobi')
        img = request.form.get('img')
        url2mail(url, img, mobi)
        return 'done'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

