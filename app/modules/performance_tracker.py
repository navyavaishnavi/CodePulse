import time
import tracemalloc


class PerformanceTracker:

    def __init__(self, code):
        self.code = code

    def measure_execution_time(self):

        start_time = time.time()

        try:
            exec(self.code)

        except Exception:
            pass

        end_time = time.time()

        execution_time = end_time - start_time

        return round(execution_time, 6)

    def measure_memory_usage(self):

        tracemalloc.start()

        try:
            exec(self.code)

        except Exception:
            pass

        current, peak = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        peak_memory_kb = peak / 1024

        return round(peak_memory_kb, 2)

    def analyze_performance(self):

        result = {
            "execution_time": self.measure_execution_time(),
            "memory_usage_kb": self.measure_memory_usage()
        }

        return result