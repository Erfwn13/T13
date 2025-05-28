import logging
import time
import os
from typing import Dict, Union, Any


class PerformanceMonitor:
    """A class for monitoring and logging performance metrics and execution time.

    This class provides functionality to track performance metrics and elapsed time,
    logging them both to a file and console output.
    """

    def __init__(self, log_file: str = "performance.log") -> None:
        """Initialize the performance monitor with a specified log file.

        Args:
            log_file (str): Path to the log file. Defaults to "performance.log"
        """
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.start_time = time.time()

    def log_performance(self, metrics: Dict[str, Union[float, int, str]]) -> None:
        """Log performance metrics to both file and console.

        Args:
            metrics (Dict[str, Union[float, int, str]]): Dictionary containing performance metrics
        """
        logging.info("Performance Metrics: %s", metrics)
        print("Logged performance:", metrics)

    def report_elapsed_time(self) -> float:
        """Calculate and report the elapsed time since initialization.

        Returns:
            float: Elapsed time in seconds
        """
        elapsed = time.time() - self.start_time
        logging.info("Elapsed Time: %.2f seconds", elapsed)
        print(f"Elapsed Time: {elapsed:.2f} seconds")
        return elapsed


if __name__ == "__main__":
    # Example usage of the PerformanceMonitor
    monitor = PerformanceMonitor()

    # Log some sample performance metrics
    monitor.log_performance(
        {
            "cpu_usage": 45.2,
            "memory_usage_mb": 128,
            "response_time_ms": 250,
        }
    )

    # Simulate some work
    time.sleep(1)

    # Report the total elapsed time
    monitor.report_elapsed_time()
