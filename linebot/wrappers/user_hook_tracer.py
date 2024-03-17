from CHRLINE.hooks import HooksTracer

from database.models.user import User


class HooksTracerWrapper(HooksTracer):
    user: User
