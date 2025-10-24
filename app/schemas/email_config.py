from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi_mail import ConnectionConfig

class EmailSettings(BaseSettings):
    MAIL_USERNAME: str = 'apikey'
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.sendgrid.net"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    # class Config:
    #     env_file = '.env'
    #     extra = 'ignore'

    model_config = SettingsConfigDict(
        env_file="/Users/oleg/PycharmProjects/mini-blog_fastAPI/.env",
        extra='ignore'
    )

email_settings = EmailSettings()

conf = ConnectionConfig(
    MAIL_USERNAME=email_settings.MAIL_USERNAME,
    MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
    MAIL_FROM=email_settings.MAIL_FROM,
    MAIL_PORT=email_settings.MAIL_PORT,
    MAIL_SERVER=email_settings.MAIL_SERVER,
    MAIL_STARTTLS=email_settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=email_settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False
)