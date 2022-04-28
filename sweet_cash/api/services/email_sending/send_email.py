
import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_jwt_extended import create_access_token
from datetime import timedelta

from sweet_cash.config import Config

logger = logging.getLogger(name="email sending")


class SendEmail(object):

    def __call__(self, email: str):
        try:
            server = smtplib.SMTP_SSL(host=Config.SMTP_HOST)
            # server.starttls(context=ssl.create_default_context())
            server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)

            msg = MIMEMultipart()

            msg['From'] = Config.EMAIL_ADDRESS
            msg['To'] = email
            msg['Subject'] = 'Подтверждение регистрации Sweet Cash'

            expire_delta = timedelta(24)
            confirmation_code = create_access_token(identity=email, expires_delta=expire_delta)

            content = f"""\
                    <html>
                      <body>
                        <p>Привет!<br>
                           Для завершения регистрации на Sweet Cash перейдите по
                           <a href="{Config.SWEET_CASH_URL}/api/v1/auth/confirm?email={email}&code={confirmation_code}">ссылке</a>.
                        </p>
                      </body>
                    </html>
                    """

            msg.attach(MIMEText(content, 'html'))

            server.send_message(msg)

        except Exception as e:
            print(e)

        logger.info(f'Email sent to address {email}')

        del msg

        return "Ok"
