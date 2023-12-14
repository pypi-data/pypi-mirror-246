import asyncio
import select

from .types import Optional


class SimpleEventReader:
    def __init__(self, device, max_queue_size : int = 10):
        self.device = device
        self._buffer = asyncio.Queue(maxsize=max_queue_size)
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    async def __aenter__(self):
        if self.device.is_blocking:
            raise RuntimeError("Cannot use async event reader on blocking device")
        self._loop = asyncio.get_event_loop()
        self._loop.add_reader(self.device, self._on_event)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # If another event loop is running it means our device is gone from the
        # original loop readers list so nothing is done
        self._loop.remove_reader(self.device)
        self._loop = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def _on_event(self):
        task = self._loop.create_future()
        try:
            data = self.device.read()
            task.set_result(data)
        except Exception as error:
            task.set_exception(error)

        buffer = self._buffer
        if buffer.full():
            self.device.log.warn("missed event")
            buffer.get_nowait()
        buffer.put_nowait(task)

    def read(self, timeout=None):
        return self.device.read()

    async def aread(self):
        """Wait for next event or return last event"""
        task = await self._buffer.get()
        return await task


class EventReader:
    def __init__(self, device, max_queue_size=1):
        self.device = device
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._selector: Optional[select.epoll] = None
        self._buffer: Optional[asyncio.Queue] = None
        self._max_queue_size = max_queue_size

    async def __aenter__(self):
        if self.device.is_blocking:
            raise RuntimeError("Cannot use async event reader on blocking device")
        self._buffer = asyncio.Queue(maxsize=self._max_queue_size)
        self._selector = select.epoll()
        self._loop = asyncio.get_event_loop()
        self._loop.add_reader(self._selector.fileno(), self._on_event)
        self._selector.register(self.device.fileno(), select.POLLIN)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self._selector.unregister(self.device.fileno())
        self._loop.remove_reader(self._selector.fileno())
        self._selector.close()
        self._selector = None
        self._loop = None
        self._buffer = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def _on_event(self):
        task = self._loop.create_future()
        try:
            self._selector.poll(0)  # avoid blocking
            data = self.device.read()
            task.set_result(data)
        except Exception as error:
            task.set_exception(error)

        buffer = self._buffer
        if buffer.full():
            self.device.log.warn("missed event")
            buffer.get_nowait()
        buffer.put_nowait(task)

    def read(self, timeout=None):
        return self.device.read()

    async def aread(self):
        """Wait for next event or return last event"""
        task = await self._buffer.get()
        return await task
