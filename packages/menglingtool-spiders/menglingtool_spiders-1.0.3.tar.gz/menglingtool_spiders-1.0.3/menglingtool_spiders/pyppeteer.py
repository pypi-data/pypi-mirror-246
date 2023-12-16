import asyncio
from .__pyppeteer__.action import Body, Act
from .__pyppeteer__.request import Req


def _run(task):
    asyncio.get_event_loop().run_until_complete(asyncio.gather(task))


class PyppTool(Body, Act, Req):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _run(self.initBrowser())

    def close(self):
        _run(self.browser.close())


# 每个任务对应一个page
def tasksRun(*tasks):
    async def main():
        for i, task in enumerate(tasks):
            async_task = asyncio.create_task(task, name=f'task-{i}')
            await async_task

    asyncio.run(main())
