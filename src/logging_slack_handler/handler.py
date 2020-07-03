import logging 
from requests import Session


class SlackHandler(logging.Handler):

    def __init__(self, channels_ids, bearer, level=logging.NOTSET):
        logging.Handler.__init__(self)
        self.level = level
        self.channels_ids = (
            channels_ids
            if isinstance(channels_ids, (list, tuple, set))
            else [channels_ids]
        )
        self.session = Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer}"
        })

    def emit(self, record):
        try:
            for channel in self.channels_ids:
                self.session.post(
                    "https://slack.com/api/chat.postMessage",
                    json = {
                        "channel": channel,
                        "text": self.format(record)
                    }
                )
        except Exception:
            self.handleError(record)

    def close(self):
        self.session.close()
        super().close()
