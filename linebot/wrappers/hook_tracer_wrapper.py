from datetime import datetime

from CHRLINE.hooks import HooksTracer


class HooksTracerWrapper(HooksTracer):
    setup_timestamp: datetime = datetime.now()
