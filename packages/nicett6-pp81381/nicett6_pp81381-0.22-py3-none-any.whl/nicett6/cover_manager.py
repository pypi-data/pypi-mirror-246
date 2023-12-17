import logging
from typing import Dict, Optional
from nicett6.connection import open as open_tt6, TT6Connection, TT6Writer, TT6Reader
from nicett6.cover import Cover, TT6Cover
from nicett6.decode import (
    AckResponse,
    HexPosResponse,
    PctAckResponse,
    PctPosResponse,
    ResponseMessageType,
)
from nicett6.emulator.line_handler import (
    CMD_MOVE_DOWN,
    CMD_MOVE_DOWN_STEP,
    CMD_MOVE_POS,
    CMD_MOVE_POS_1,
    CMD_MOVE_POS_2,
    CMD_MOVE_POS_3,
    CMD_MOVE_POS_4,
    CMD_MOVE_POS_5,
    CMD_MOVE_POS_6,
    CMD_MOVE_UP,
    CMD_MOVE_UP_STEP,
    CMD_STOP,
)
from nicett6.multiplexer import MultiplexerSerialConnection
from nicett6.ttbus_device import TTBusDeviceAddress

_LOGGER = logging.getLogger(__name__)


class CoverManager:
    def __init__(self, serial_port: str):
        self._conn: Optional[MultiplexerSerialConnection] = None
        self._serial_port: str = serial_port
        self._message_tracker_reader: Optional[TT6Reader] = None
        self._writer: Optional[TT6Writer] = None
        self._tt6_covers_dict: Dict[TTBusDeviceAddress, TT6Cover] = {}

    @property
    def serial_port(self):
        return self._serial_port

    @property
    def tt6_covers(self):
        return self._tt6_covers_dict.values()

    @property
    def conn(self) -> TT6Connection:
        if self._conn is None:
            raise RuntimeError(
                "connection property accessed when there is no connection"
            )
        return self._conn

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exception_type, exception_value, traceback):
        await self.close()

    async def open(self) -> None:
        self._conn = await open_tt6(self._serial_port)

        # NOTE: reader is created here rather than in self.message_tracker
        # to ensure that all messages from this moment on are captured
        reader = self._conn.add_reader()
        assert isinstance(reader, TT6Reader)
        self._message_tracker_reader = reader

        writer = self._conn.get_writer()
        assert isinstance(writer, TT6Writer)
        self._writer = writer

        await self._writer.send_web_on()

    async def close(self) -> None:
        await self.remove_covers()
        if self._conn is not None:
            if self._message_tracker_reader is not None:
                self._conn.remove_reader(self._message_tracker_reader)
                self._message_tracker_reader = None
            self._writer = None
            self._conn.close()
            self._conn = None

    async def _handle_response_message_for_cover(
        self, msg: ResponseMessageType, cover: Cover
    ) -> None:
        if isinstance(msg, PctPosResponse):
            await cover.set_drop_pct(msg.pct_pos / 1000.0)
        elif isinstance(msg, PctAckResponse):
            await cover.set_target_drop_pct_hint(msg.pct_pos / 1000.0)
        elif isinstance(msg, AckResponse):
            if msg.cmd_code == CMD_MOVE_UP or msg.cmd_code == CMD_MOVE_UP_STEP:
                await cover.set_closing()
            elif msg.cmd_code == CMD_MOVE_DOWN or msg.cmd_code == CMD_MOVE_DOWN_STEP:
                await cover.set_opening()
            elif msg.cmd_code == CMD_STOP:
                # Can't call set_idle() here as a final pos
                # response will come from the controller up to
                # 2.5 secs after the Ack, which will call moved()
                # again and initiate another idle delay check
                pass
            elif msg.cmd_code in {
                CMD_MOVE_POS_1,
                CMD_MOVE_POS_2,
                CMD_MOVE_POS_3,
                CMD_MOVE_POS_4,
                CMD_MOVE_POS_5,
                CMD_MOVE_POS_6,
            }:
                # We can't know the direction until we've received a PctPosResponse
                await cover.moved()
        elif isinstance(msg, HexPosResponse):
            if msg.cmd_code == CMD_MOVE_POS:
                await cover.set_target_drop_pct_hint(msg.hex_pos / 255.0)

    async def _handle_response_message(self, msg: ResponseMessageType) -> None:
        if isinstance(
            msg, (AckResponse, HexPosResponse, PctPosResponse, PctAckResponse)
        ):
            try:
                tt6_cover: TT6Cover = self._tt6_covers_dict[msg.tt_addr]
            except KeyError:
                _LOGGER.warning("response message addressed to unknown device: %s", msg)
                return
            await self._handle_response_message_for_cover(msg, tt6_cover.cover)

    async def message_tracker(self) -> None:
        _LOGGER.debug("message_tracker started")
        if self._message_tracker_reader is not None:
            async for msg in self._message_tracker_reader:
                _LOGGER.debug("msg:%s", msg)
                await self._handle_response_message(msg)
        _LOGGER.debug("message tracker finished")

    async def add_cover(self, tt_addr: TTBusDeviceAddress, cover: Cover) -> TT6Cover:
        if self._writer is None:
            raise RuntimeError("add_cover called when writer not initialised")
        tt6_cover = TT6Cover(tt_addr, cover, self._writer)
        tt6_cover.enable_notifier()
        self._tt6_covers_dict[tt_addr] = tt6_cover
        await tt6_cover.send_pos_request()
        return tt6_cover

    async def remove_covers(self) -> None:
        for tt6_cover in self._tt6_covers_dict.values():
            await tt6_cover.disable_notifier()
        self._tt6_covers_dict = {}
