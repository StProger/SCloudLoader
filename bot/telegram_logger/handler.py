import logging
import time

import requests


logger = logging.getLogger('telegramLogger')
logger.setLevel(logging.INFO)


class LogMessageDispatcher(logging.Handler):
    """
    Handles dispatching log messages to Telegram.
    """

    TIMEOUT = 13
    API_CALL_INTERVAL = 1 / 30

    def __init__(
        self,
        token: str,
        mode: str = 'markdown',
        disable_notifications: bool = False,
        disable_preview: bool = False,
    ):
        """
        :param token: Telegram bot API token
        :param chat_ids: List of chat IDs to send messages to
        :param mode: Parse mode for the message (markdown, html)
        :param disable_notifications: Disable notifications for messages
        :param disable_preview: Disable web page preview in the message
        """
        self.token = token
        self.mode = mode  # New mode parameter
        self.disable_notifications = disable_notifications
        self.disable_preview = disable_preview
        self.session = requests.Session()
        super().__init__()

    @property
    def url(self):
        """
        The Telegram bot API URL for sending messages.
        """
        return (
            "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode={mode}&"
            "disable_web_page_preview={disable_web_page_preview}&disable_notifications={disable_notifications}"
        )

    def emit(self, record):
        """
        Send the log record to the Telegram chat(s).
        """

        if record.__dict__.get('flag') != 'tg':
            return
        # Format the log message
        log_message = self.format(record)

        url = self.url.format(
            token=self.token,
            chat_id=-4833573640,
            mode=self.mode,
            text=log_message,
            disable_web_page_preview=self.disable_preview,
            disable_notifications=self.disable_notifications,
        )

        response = self.session.get(url, timeout=self.TIMEOUT)
        if not response.ok:
            logger.warning(f"Telegram log dispatching failed with status code {response.status_code}")
            logger.warning(f"Response is: {response.text}")

        # To avoid hitting the Telegram API rate limit
        time.sleep(self.API_CALL_INTERVAL)

    def __del__(self):
        """
        Close the session when the handler is destroyed.
        """
        self.session.close()
