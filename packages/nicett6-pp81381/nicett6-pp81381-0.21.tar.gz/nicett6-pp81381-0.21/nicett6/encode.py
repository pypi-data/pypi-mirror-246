import logging

from nicett6.ttbus_device import TTBusDeviceAddress

_LOGGER = logging.getLogger(__name__)


class Encode:
    """Helper class to encode commands"""

    EOL = b"\r"

    SIMPLE_COMMANDS = {
        "STOP": 0x03,
        "MOVE_DOWN": 0x04,
        "MOVE_UP": 0x05,
        "MOVE_POS_1": 0x06,
        "MOVE_POS_2": 0x07,
        "MOVE_POS_3": 0x08,
        "MOVE_POS_4": 0x09,
        "MOVE_POS_5": 0x10,
        "MOVE_POS_6": 0x11,
        "MOVE_UP_STEP": 0x12,
        "MOVE_DOWN_STEP": 0x13,
        "STORE_UPPER_LIMIT": 0x20,
        "STORE_LOWER_LIMIT": 0x21,
        "STORE_POS_1": 0x22,
        "STORE_POS_2": 0x23,
        "STORE_POS_3": 0x24,
        "STORE_POS_4": 0x25,
        "STORE_POS_5": 0x26,
        "STORE_POS_6": 0x27,
        "DEL_UPPER_LIMIT": 0x30,
        "DEL_LOWER_LIMIT": 0x31,
        "DEL_POS_1": 0x32,
        "DEL_POS_2": 0x33,
        "DEL_POS_3": 0x34,
        "DEL_POS_4": 0x35,
        "DEL_POS_5": 0x36,
        "DEL_POS_6": 0x37,
        "READ_POS": 0x45,
    }

    COMMANDS_WITH_DATA = {
        "MOVE_POS": 0x40,
    }

    @classmethod
    def fmt_msg(cls, msg: str) -> bytes:
        return msg.encode("utf-8") + cls.EOL

    @classmethod
    def web_on(cls) -> bytes:
        return cls.fmt_msg("WEB_ON")

    @classmethod
    def web_off(cls) -> bytes:
        return cls.fmt_msg("WEB_OFF")

    @classmethod
    def simple_command(cls, tt_addr: TTBusDeviceAddress, cmd_code: str) -> bytes:
        return cls.fmt_msg(
            f"CMD {tt_addr.address:02X} {tt_addr.node:02X} "
            f"{cls.SIMPLE_COMMANDS[cmd_code]:02X}"
        )

    @classmethod
    def simple_command_with_data(
        cls, tt_addr: TTBusDeviceAddress, cmd_code: str, data: int
    ) -> bytes:
        """
        Encode a command that takes an integer data parameter

        data should be between 0x00 and 0xFF
        """
        if data < 0x00 or data > 0xFF:
            raise ValueError(f"data out of range 0x00 to 0xFF: {data}")
        return cls.fmt_msg(
            f"CMD {tt_addr.address:02X} {tt_addr.node:02X} "
            f"{cls.COMMANDS_WITH_DATA[cmd_code]:02X} {data:02X}"
        )

    @classmethod
    def web_move_command(cls, tt_addr: TTBusDeviceAddress, pct: float) -> bytes:
        """Set position to the percentage given"""
        thousandths: int = round(pct * 1000.0)
        if thousandths < 0:
            _LOGGER.info(
                f"Requested percentage position for {tt_addr} of {pct}% floored at 0%"
            )
            thousandths = 0
        elif thousandths > 1000:
            _LOGGER.info(
                f"Requested percentage position for {tt_addr} of {pct}% capped at 100%"
            )
            thousandths = 1000
        return cls.fmt_msg(
            f"POS > {tt_addr.address:02X} {tt_addr.node:02X} "
            f"{thousandths:04d} FFFF FF"
        )

    @classmethod
    def web_pos_request(cls, tt_addr: TTBusDeviceAddress) -> bytes:
        """Request the position"""
        return cls.fmt_msg(
            f"POS < {tt_addr.address:02X} {tt_addr.node:02X} " "FFFF FFFF FF"
        )
