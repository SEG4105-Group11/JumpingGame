import time


class Timer:
    def __init__(self):
        self.paused = False
        self.stopped = False

    def start(self):
        self.start_time = time.time()

    def pause(self):
        self.pause_time = time.time()
        self.paused = True

    def resume(self):
        time_paused = time.time() - self.pause_time
        self.start_time += time_paused
        self.paused = False

    def stop(self):
        self.end_time = time.time()
        self.stopped = True

    def get_time(self):
        if self.stopped:
            return self.end_time - self.start_time

        if self.paused:
            return self.pause_time - self.start_time

        return time.time() - self.start_time
