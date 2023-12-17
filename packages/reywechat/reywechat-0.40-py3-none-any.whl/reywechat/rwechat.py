# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : WeChat methods.
"""


from typing import Final
from reytool.ros import create_folder as reytool_create_folder
from reytool.rsystem import get_idle_port
from reytool.rtime import sleep


__all__ = (
    "RWeChat",
)


class RWeChat(object):
    """
    Rey's `WeChat` type.
    Only applicable to WeChat clients with version `3.9.5.81`.
    Will start client API service with port `19088` and message callback service with port '19089'.
    """

    # Environment.
    client_version: Final[str] = "3.9.5.81"
    client_api_port: Final[int] = 19088
    message_callback_port: Final[int] = 19089


    def __init__(
        self,
        max_receiver: int = 2,
        keep : bool = True
    ) -> None:
        """
        Build `WeChat` instance.

        Parameters
        ----------
        max_receiver : Maximum number of receivers.
        keep : Whether blocking the main thread to keep running.
        """

        # Import.
        from .rclient import RClient
        from .rreceive import RReceiver

        # Create folder.
        self._create_folder()

        # Set attribute.

        ## Instance.
        self.rclient = RClient(self)
        self.rreceiver = RReceiver(self, max_receiver)

        ## Receive.
        self.receive_add_handler = self.rreceiver.add_handler
        self.receive_start = self.rreceiver.start
        self.receive_stop = self.rreceiver.stop
        self.receive_end = self.rreceiver.end

        # Keep.
        if keep:
            self.keep()


    def _create_folder(self) -> None:
        """
        Create project standard folders.
        """

        # Set parameter.
        paths = [
            ".\cache",
            ".\logs"
        ]

        # Create.
        reytool_create_folder(*paths)


    def keep(self) -> None:
        """
        Blocking the main thread to keep running.
        """

        # Blocking.
        while True:
            sleep(1)