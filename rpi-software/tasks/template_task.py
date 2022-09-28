"""
Task Template
~~~~~~~~~~~~

All task files follow a pattern inherited from this template task.
Review this template file for specifics on the default class
definitions; however, to paraphrase: 
    - The `task` class we create in each task file inherits default
        methods and attributes from the template class.
    - By redefining an attribute such as `frequency` or `priority`
         we are overwriting the default values.
"""

from colorama import Fore

class Task:
    """
    The Task Object.

    Attributes:
        - priority:    The priority level assigned to the task.
        - frequency:   Number of times the task must be executed in 1 second (Hz).
        - name:        Name of the task object for future reference
        - color:       Debug color for serial terminal
    """

    priority = 10
    frequency = 1
    name = 'temp'
    color = 'blue'

    def __init__(self, mock_sat):
        """
        Initialize the Task using the mock_sat object.
        
        :type mock_sat: Satellite
        :param mock_sat: The cubesat to be registered
        """
        self.mock_sat = mock_sat

    def debug(self,msg,level=1):
        """
        Print a debug message formatted with the task name and color

        :param `msg`: Debug message to print
        :param `level`: > 1 will print as a sub-level
        """
        if level==1:
            color_map = {
                'blue': Fore.BLUE,
                'green': Fore.GREEN,
                'yellow': Fore.YELLOW,
                'red': Fore.RED,
                'cyan': Fore.CYAN,
                'magenta': Fore.MAGENTA,
                'white': Fore.WHITE,
            }
            print('{:>30} {}'.format(color_map[self.color] + '[' + self.name + ']' + Fore.WHITE ,msg))
        else:
            print('{}{}'.format('\t   └── ',msg))

    def main_task(self, *args, **kwargs):
        """
        Contains the code for the user defined task. 

        :param `*args`: Variable number of arguments used for task execution.
        :param `**kwargs`: Variable number of keyword arguments used for task execution. 
        """
        pass