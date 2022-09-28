from tasks.template_task import Task
import time

class task(Task):
    priority = 1
    frequency = 1/10 # once every 10s
    name = 'radio'
    color = 'red'

    async def main_task(self):
        self.debug(f'radio start: {time.monotonic():.3f}')
        self.debug('sending beacon')
        await self.mock_sat.obc.sleep(5)
        self.debug(f'radio stop: {time.monotonic():.3f}')