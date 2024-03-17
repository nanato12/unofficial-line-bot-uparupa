from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer
from CHRLINE.services.thrift.ttypes import Operation, OpType

from database.models.operation import Operation as OperationModel
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class Op60Hook(HooksTracer):
    @tracer.Operation(OpType.NOTIFIED_JOIN_CHAT)
    def notified_join_chat(self, op: Operation, bot: CHRLINE) -> None:
        logger.info(op)

        o = OperationModel.from_line_operation(op)
        o.create()
