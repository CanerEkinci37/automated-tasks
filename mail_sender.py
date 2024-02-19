import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

SMTP_PORT = 587
SMTP_SERVER = "smtp.gmail.com"


class GmailUser:
    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password

    def send_mail(self, email_list, body, subject, filename):
        for person in email_list:
            msg = MIMEMultipart()
            msg["From"] = self.email
            msg["To"] = person
            msg["Subject"] = subject
            # Body of the message
            msg.attach(MIMEText(body, "plain"))

            # Attachment
            attachment = open(filename, "rb")
            attachment_package = MIMEBase("application", "octet-stream")
            attachment_package.set_payload((attachment).read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header(
                "Content-Disposition", "attachment; filename= " + filename
            )
            msg.attach(attachment_package)
            text = msg.as_string()

            print("Connecting to server...")
            TIE_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            TIE_server.starttls()
            TIE_server.login(self.email, self.password)
            print("Successfully connected to server\n")

            print(f"Sending email to {person}...")
            TIE_server.sendmail(self.email, person, text)
            print(f"Email sent to: {person}")

        TIE_server.close()


if __name__ == "__main__":
    body = """
    Sayın Yetkili,
    
    Düzce Üniversitesi Bilgisayar Mühendisliği Bölümü 4.sınıf öğrencisiyim. Eğitim hayatımda kendime katmış olduğum yazılımsal ve donanımsal birikimlerle şirketinizde stajyer
    pozisyonunda çalışma isteğimi iletmek istiyorum. Şirketinizde yapacağım çalışmalar ile kazanacağım deneyim gelecekte ilerlemek istediğim yazılım sektöründe bana büyük
    bir katkısı olacağını düşünmekteyim.
    
    Web geliştirme ve Veri Bilimi alanında yaklaşık 1 senedir ilgilenmekteyim. Problem çözme ve sıkı çalışma koşullarına uygun olduğumu düşünmekteyim.
    
    Sonuç olarak; size iletmiş olduğum özgeçmişimin hem şirketinize hem de kendime değer katabileceğinizi düşünerek yaz stajı programı kapsamında değerlendirilmesini rica
    ediyorum.

    Güncel CV' im ektedir.

    İlginiz için şimdiden teşekkür ederim.

    Saygılarımla,

    Caner EKİNCİ
    """
    load_dotenv(".env")
    user = GmailUser("canereknc37@gmail.com", os.environ.get("EMAIL_KEY"))
    subject = "Stajyer"
    filename = "CanerEkinciCV.pdf"
    with open("emails.txt") as f:
        email_list = list(map(str.strip, f.readlines()))
    user.send_mail(email_list=email_list, body=body, subject=subject, filename=filename)
