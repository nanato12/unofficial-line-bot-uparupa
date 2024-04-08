from time import sleep

from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer
from CHRLINE.services.thrift.ttypes import Contact, Operation, OpType

from database.models.operation import Operation as OperationModel
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class Op124Hook(HooksTracer):
    @tracer.Operation(OpType.NOTIFIED_INVITE_INTO_CHAT)
    def notified_invite_into_chat(self, op: Operation, bot: CHRLINE) -> None:
        logger.info(op)

        gid = str(op.param1)
        inviter_mid = str(op.param2)

        if bot.mid in str(op.param3).split():
            bot.acceptChatInvitation(gid)
            contact: Contact = bot.getContact(inviter_mid)
            sleep(5)
            bot.sendMention(gid, "@! 招待ありがとう♪", mids=[contact.mid])

        o = OperationModel.from_line_operation(op)
        o.create()
