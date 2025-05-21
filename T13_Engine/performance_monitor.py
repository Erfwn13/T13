import time
import logging

class PerformanceMonitor:
    def __init__(self, log_file="performance.log"):
        logging.basicConfig(filename=log_file, level=logging.INFO, 
                            format="%(asctime)s - %(levelname)s - %(message)s")
        self.start_time = time.time()
    
    def log_performance(self, metrics):
        logging.info("Performance Metrics: %s", metrics)
        print("Logged performance:", metrics)
    
    def report_elapsed_time(self):
        elapsed = time.time() - self.start_time
        logging.info("Elapsed Time: %.2f seconds", elapsed)
        print(f"Elapsed Time: {elapsed:.2f} seconds")
        return elapsed

if __name__ == "__main__":
    monitor = PerformanceMonitor()
    # نمونه‌ای از ثبت معیارهای عملکرد
    monitor.log_performance({"avg_emotion": 6.5, "decision_latency": 0.45})
    time.sleep(1)
    monitor.report_elapsed_time()