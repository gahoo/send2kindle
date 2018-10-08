from flask import Flask, request, render_template, redirect
from file2mail import makeMail, sendMail
from url2html import saveHTML, html2mobi

def url2mail(url, img, mobi):
    if pdf in url:
        attached_file = download_pdf(url)
    else:
        attached_file = saveHTML(url, img, 'cache')
    if mobi:
        html2mobi(attached_file)
        attached_file = attached_file.rstrip('.html') + '.mobi'

    msg = makeMail(attached_file)
    sendMail(msg)

def download_pdf(url):
    pdf_file = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(pdf_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return pdf_file

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

