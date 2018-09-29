import smtplib
import yaml
import argparse
import sys
import os
import pdb
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

    # Attache email body
    msg.attach(MIMEText('Want to write a customized email boddy? Then put it here.'))

    # Attach the .mobi file
    fp = open(file_path, "rb")
    mobi_file = MIMEApplication(fp.read())
    fp.close()
    encoders.encode_base64(mobi_file)
    mobi_file.add_header('Content-Disposition', 'attachment; filename="%s"' % file_name )
    msg.attach(mobi_file)

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
