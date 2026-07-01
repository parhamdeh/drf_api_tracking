from .base_mixins import BaseLoggingMixin
from .models import APIRquestLog


class LoggingMixin(BaseLoggingMixin):
    def handle_log(self):
        # APIRquestLog(**self.log()).save()
        print(self.log)