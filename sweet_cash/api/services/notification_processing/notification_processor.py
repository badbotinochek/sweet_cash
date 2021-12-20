
import threading
import time


class NotificationProcessor(threading.Thread):
    time_to_wait = 10  # TODO в сonfig

    def __init__(self, name: str, q):
        threading.Thread.__init__(self, name=name, daemon=True)
        self.q = q

    def run(self):
        print("Starting {}".format(self.name))
        while True:  # циклически получать задачи в потоке
            if not self.q.empty():
                data = self.q.get(timeout=2)  # ожидать задачу в течение 2 сек
                if data is not None:
                    self.process(data)  # выполнение задачи
            time.sleep(self.time_to_wait)

    @staticmethod
    def process(data):
        print(data)
