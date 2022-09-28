from tasks.template_task import Task
import time

class task(Task):
    priority = 5
    frequency = 1/20 # once every 20s
    name='time'
    color = 'blue'

    async def main_task(self):
        t_since_boot = (time.time()) - self.mock_sat.boot_time
        self.debug(f'{t_since_boot:.3f}s since boot')