import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

def get_msg(maildetails):
    attachments = None
    msg = MIMEMultipart()
    # msg["From"] = 
    msg["To"] = maildetails['to']
    msg["Subject"] = maildetails['subject']
    msg.preamble = maildetails['preamble']
    if 'attachments' in maildetails:
        attachments = maildetails['attachments']
    
    for fl in attachments:
        fileToSend = fl['fileToSend']
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fl['filename'])
        msg.attach(attachment)
    return msg.as_string()



def sendmail(auth,maildetails):
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(auth['username'],auth['password'])
    server.sendmail(auth['username'], maildetails['to'],get_msg(maildetails))
    server.quit()

    
#app.py
# from send_mail import sendmail
# auth = {'username':'vinay@accio.ai','password':'vinay@123'}
# maildetails = {
#     'to':'vinay@accio.ai',
#     'subject':'New Articles',
#     'preamble':'new articles',
#     'attachments':[{'fileToSend':'./csvs/realsimple.csv','filename':'new_articles_realsimple'}]
# }
sendmail(auth,maildetails)
