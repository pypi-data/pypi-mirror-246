# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-26 11:18:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Receive methods.
"""


from __future__ import annotations
from typing import Any, List, Dict, Callable, Optional
from queue import Queue
from json import loads as json_loads
from reytool.rcomm import listen_socket
from reytool.rtime import sleep
from reytool.rwrap import wrap_thread, wrap_exc
from reytool.rmultitask import RThreadPool

from .rwechat import RWeChat


__all__ = (
    "RReceiver",
)


# Message Type.
Message = Dict


class RReceiver(object):
    """
    Rey's `receiver` type.
    """


    def __init__(
        self,
        rwechat: RWeChat,
        max_receiver: int
    ) -> None:
        """
        Build `receiver` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        max_receiver : Maximum number of receivers.
        """

        # Set attribute.
        self.rwechat = rwechat
        self.queue: Queue[Message] = Queue()
        self.handlers: List[Callable[[Message], Any]] = []
        self.started: Optional[bool] = False

        # Prepare.
        self._start_callback()
        self._start_receiver(max_receiver)


    @wrap_thread
    def _start_callback(self) -> None:
        """
        Start callback socket.
        """


        # Define.
        def put_queue(data: bytes) -> None:
            """
            Put message data into receive queue.

            Parameters
            ----------
            data : Socket receive data.
            """

            # Decode.
            data: Message = json_loads(data)

            # Put.
            self.queue.put(data)


        # Listen socket.
        listen_socket(
            "127.0.0.1",
            self.rwechat.message_callback_port,
            put_queue
        )


    @wrap_thread
    def _start_receiver(
        self,
        max_receiver: int
    ) -> None:
        """
        Create receiver, that will sequentially handle message in the receive queue.

        Parameters
        ----------
        max_receiver : Maximum number of receivers.
        """


        # Define.
        def handle_message(message: Message) -> None:
            """
            Handle message.

            Parameters
            ----------
            message : Message parameters.
            """

            # Handle.
            for handler in self.handlers:
                handler(message)


        # Thread pool.
        thread_pool = RThreadPool(
            handle_message,
            _max_workers=max_receiver
        )

        # Loop.
        while True:

            ## Stop.
            if self.started is False:
                sleep(0.1)
                continue

            ## End.
            elif self.started is None:
                break

            ## Submit.
            message = self.queue.get()
            thread_pool(message)


    def add_handler(
        self,
        handler: Callable[[Message], Any]
    ) -> None:
        """
        Add message handler function.

        Parameters
        ----------
        handler : Handler method, input parameter is message parameters.
        """

        # Add.
        self.handlers.append(handler)


    def start(self) -> None:
        """
        Start receiver.
        """

        # Start.
        self.started = True


    def stop(self) -> None:
        """
        Stop receiver.
        """

        # Stop.
        self.started = False


    def end(self) -> None:
        """
        End receiver.
        """

        # End.
        self.started = None


    __del__ = end