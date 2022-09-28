from tasks.template_task import Task
import time

class task(Task):
    priority = 4
    frequency = 1/30 # once every 30s
    name = 'test'
    color = 'green'

    async def main_task(self):
        self.debug(f'test start: {time.monotonic():.3f}')
        await self.mock_sat.obc.sleep(5)
        self.debug(f'test stop: {time.monotonic():.3f}')