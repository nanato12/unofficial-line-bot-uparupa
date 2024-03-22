from datetime import datetime

from CHRLINE.hooks import HooksTracer

from database.models.user import User


class HooksTracerWrapper(HooksTracer):
    user: User
    setup_timestamp: datetime = datetime.now()
