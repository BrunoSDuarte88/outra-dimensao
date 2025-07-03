import ssl
import smtplib
import logging
from django.core.mail.backends.smtp import EmailBackend

logger = logging.getLogger(__name__)

class CustomEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)

            # Usa contexto SSL padrão, com verificação correta do certificado
            context = ssl.create_default_context()

            self.connection.starttls(context=context)

            if self.username and self.password:
                self.connection.login(self.username, self.password)

            return True
        except Exception as e:
            logger.error(f'Erro ao abrir conexão SMTP: {e}')
            if not self.fail_silently:
                raise
            return False
