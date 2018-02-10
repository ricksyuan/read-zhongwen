import time

class TicToc:
    """Simple class to measure elapsed time."""   
    def __init__(self):
        self._tic = time.time()
    
    def tic(self):
        self._tic = time.time()

    def toc(self, message):
        elapsed_seconds = time.time() - self._tic
        formatted_time = '{0:.2f} seconds'.format(elapsed_seconds)
        print(message + ' (' + formatted_time + ')')
        return formatted_time