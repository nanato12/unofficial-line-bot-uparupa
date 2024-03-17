from CHRLINE import CHRLINE
from CHRLINE.hooks import HooksTracer
from CHRLINE.services.thrift.ttypes import (
    ChatRoomAnnouncement,
    Operation,
    OpType,
)

from database.models.operation import Operation as OperationModel
from linebot.line import LINEBot
from linebot.logger import get_file_path_logger

logger = get_file_path_logger(__name__)

line = LINEBot()
tracer = line.tracer


class Op30Hook(HooksTracer):
    @tracer.Operation(OpType.RECEIVE_ANNOUNCEMENT)
    def receive_announcement(self, op: Operation, bot: CHRLINE) -> None:
        logger.info(op)

        to = str(op.param1)
        index = str(op.param2)

        announcements: list[ChatRoomAnnouncement] = (
            bot.getChatRoomAnnouncements(to)
        )
        announcement: ChatRoomAnnouncement = next(
            filter(lambda a: a.announcementSeq == int(index), announcements)
        )
        if announcement.contents is None:
            return

        bot.sendMention(
            to,
            f"[アナウンス]\n追加した人: @!\nテキスト: {announcement.contents.text}",
            mids=[announcement.creatorMid],
        )

        o = OperationModel.from_line_operation(op)
        o.create()
