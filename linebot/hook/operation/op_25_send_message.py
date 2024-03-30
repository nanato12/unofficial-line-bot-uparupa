from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer
from CHRLINE.services.thrift.ttypes import Operation, OpType

from database.models.operation import Operation as OperationModel
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class Op25Hook(HooksTracer):
    @tracer.Operation(OpType.SEND_MESSAGE)
    def receive_message(self, op: Operation, _: CHRLINE) -> None:
        o = OperationModel.from_line_operation(op)
        o.create()
