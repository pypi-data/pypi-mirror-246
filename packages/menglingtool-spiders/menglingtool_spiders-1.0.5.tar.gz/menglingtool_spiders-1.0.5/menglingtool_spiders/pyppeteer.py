import asyncio
from .__pyppeteer__.action import Act
from .__pyppeteer__.request import Req

_loop = None


def tasksRun(*tasks):
    global _loop
    if _loop is None: _loop = asyncio.get_event_loop()
    tasks = [_loop.create_task(task, name=f'task-{i}') for i, task in enumerate(tasks)]
    _loop.run_until_complete(asyncio.wait(tasks))


class PyppTool(Act, Req):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        tasksRun(self.initBrowser())

    def close(self):
        tasksRun(self.browser.close())
