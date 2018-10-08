import smtplib
import yaml
import argparse
import sys
import os
import pdb
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

with open('config.yaml') as f:
    config = yaml.load(f.read())

def makeMail(file_path):
    # Send the document as email attachment
    file_name = os.path.basename(file_path)
    msg = MIMEMultipart()
    msg['From'] = config['sender']
    msg['To'] = config['kindle'] # Can be 'Send to Kindle' email
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = file_name

    # Attach the .mobi file
    if file_path.endswith('.html'):
        fp = open(file_path, "r")
    elif any(map(lambda x:file_path.endswith(x), ['.mobi', '.zip', '.pdf'])):
        fp = open(file_path, "rb")

    #mobi_file = MIMEApplication(fp.read())
    msg_file = MIMEBase('application', 'octet-stream')
    msg_file.set_payload(fp.read())
    fp.close()
    #encoders.encode_base64(mobi_file)
    msg_file.add_header('Content-Disposition', 'attachment', filename=(Header(file_name, 'utf-8').encode()))
    msg.attach(msg_file)

    return msg

def sendMail(msg):
    # Send the email
    smtp = smtplib.SMTP_SSL(config["smtp"], config["port"])
    #smtp.starttls()
    smtp.login(config['username'], config['password'])
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()

def main(args):
    msg = makeMail(args.file)
    sendMail(msg)

if __name__ == '__main__':
    parsers = argparse.ArgumentParser(
        description = "send local file to kindle",
        formatter_class=argparse.RawTextHelpFormatter)

    parsers.add_argument('--file', help = "file path to the document.")
    parsers.set_defaults(func=main)

    argslist = sys.argv[1:]
    if len(argslist) > 0:
        args = parsers.parse_args(argslist)
        args.func(args)
    else:
        parsers.print_help()
        os._exit(0)
