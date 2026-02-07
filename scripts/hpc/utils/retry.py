"""
Retry utilities with exponential backoff for robust HPC pipeline execution

Provides decorators and helpers for automatic retry logic with configurable
backoff strategies, exception handling, and logging.
"""

import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 300.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable] = None
):
    """
    Decorator for automatic retry with exponential backoff

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        initial_delay: Initial delay in seconds before first retry (default: 1.0)
        backoff_factor: Multiplier for delay after each retry (default: 2.0)
        max_delay: Maximum delay in seconds (caps exponential growth) (default: 300.0)
        exceptions: Tuple of exceptions to catch and retry (default: all exceptions)
        on_retry: Optional callback function called on each retry with signature:
                  on_retry(attempt: int, exception: Exception, delay: float)

    Returns:
        Decorated function with automatic retry logic

    Example:
        @retry_with_backoff(
            max_retries=5,
            initial_delay=5.0,
            backoff_factor=2.0,
            exceptions=(requests.exceptions.RequestException, TimeoutError)
        )
        def fetch_data(url):
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                        # Calculate delay with exponential backoff, capped at max_delay
                        current_delay = min(delay, max_delay)

                        logging.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}"
                        )
                        logging.info(f"Retrying in {current_delay:.1f} seconds...")

                        # Call retry callback if provided
                        if on_retry:
                            try:
                                on_retry(attempt + 1, e, current_delay)
                            except Exception as callback_error:
                                logging.error(f"Retry callback failed: {callback_error}")

                        time.sleep(current_delay)
                        delay *= backoff_factor
                    else:
                        logging.error(
                            f"{func.__name__} failed after {max_retries + 1} attempts: {last_exception}"
                        )

            # Re-raise the last exception if all retries failed
            raise last_exception

        return wrapper
    return decorator


def retry_on_rate_limit(
    max_retries: int = 5,
    initial_delay: float = 60.0,
    backoff_factor: float = 2.0
):
    """
    Specialized retry decorator for API rate limiting (HTTP 429)

    Implements more aggressive backoff strategy suitable for rate limits.
    Starts with 1 minute delay and doubles each time.

    Args:
        max_retries: Maximum number of retry attempts (default: 5)
        initial_delay: Initial delay in seconds (default: 60.0 = 1 minute)
        backoff_factor: Multiplier for delay after each retry (default: 2.0)

    Example:
        @retry_on_rate_limit(max_retries=3, initial_delay=30.0)
        def fetch_gdelt_data(date):
            response = requests.get(gdelt_url, params={'date': date})
            if response.status_code == 429:
                raise requests.exceptions.HTTPError("Rate limited")
            response.raise_for_status()
            return response.json()
    """
    import requests

    def on_rate_limit_retry(attempt: int, exception: Exception, delay: float):
        """Custom callback for rate limit retries"""
        logging.warning(f"Rate limit hit, backing off for {delay:.0f} seconds")

    return retry_with_backoff(
        max_retries=max_retries,
        initial_delay=initial_delay,
        backoff_factor=backoff_factor,
        max_delay=600.0,  # Cap at 10 minutes
        exceptions=(requests.exceptions.HTTPError, requests.exceptions.RequestException),
        on_retry=on_rate_limit_retry
    )


def retry_on_network_error(
    max_retries: int = 3,
    initial_delay: float = 5.0,
    backoff_factor: float = 2.0
):
    """
    Specialized retry decorator for network errors (timeouts, connection errors)

    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        initial_delay: Initial delay in seconds (default: 5.0)
        backoff_factor: Multiplier for delay after each retry (default: 2.0)

    Example:
        @retry_on_network_error()
        def download_file(url, output_path):
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
    """
    import requests

    return retry_with_backoff(
        max_retries=max_retries,
        initial_delay=initial_delay,
        backoff_factor=backoff_factor,
        exceptions=(
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            TimeoutError,
            ConnectionError
        )
    )


class RetryableError(Exception):
    """
    Custom exception for explicitly retryable errors

    Raise this exception when you want to trigger a retry without
    catching all exceptions.

    Example:
        @retry_with_backoff(exceptions=(RetryableError,))
        def process_batch(batch_id):
            result = api_call(batch_id)
            if result is None:
                raise RetryableError("API returned None, retrying...")
            return result
    """
    pass


def get_robust_session():
    """
    Create a requests session with built-in retry logic

    Returns a requests.Session object configured with automatic retries
    for common transient HTTP errors.

    Returns:
        requests.Session with automatic retry adapter

    Example:
        session = get_robust_session()
        response = session.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
    """
    import requests
    from requests.adapters import HTTPAdapter
    try:
        from requests.packages.urllib3.util.retry import Retry
    except ImportError:
        from urllib3.util.retry import Retry

    session = requests.Session()

    # Configure retry strategy
    retry_strategy = Retry(
        total=5,  # Total number of retries
        backoff_factor=1,  # Wait 1, 2, 4, 8, 16 seconds between retries
        status_forcelist=[408, 429, 500, 502, 503, 504],  # HTTP status codes to retry
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],  # HTTP methods to retry
        raise_on_status=False  # Don't raise exception, let caller handle
    )

    # Mount adapter for both HTTP and HTTPS
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


# Example usage demonstrations
if __name__ == "__main__":
    import requests

    # Example 1: Basic retry with backoff
    @retry_with_backoff(max_retries=3, initial_delay=1.0)
    def flaky_function():
        """Simulated flaky function that fails sometimes"""
        import random
        if random.random() < 0.7:  # 70% failure rate
            raise ValueError("Simulated failure")
        return "Success!"

    # Example 2: API call with rate limit handling
    @retry_on_rate_limit(max_retries=3, initial_delay=30.0)
    def fetch_api_data(endpoint):
        """Fetch data from API with rate limit handling"""
        session = get_robust_session()
        response = session.get(endpoint, timeout=30)
        if response.status_code == 429:
            raise requests.exceptions.HTTPError("Rate limited")
        response.raise_for_status()
        return response.json()

    # Example 3: Network operation with timeout retry
    @retry_on_network_error(max_retries=3)
    def download_data(url):
        """Download data with automatic retry on network errors"""
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content

    print("Retry utilities loaded successfully")
    print("\nExample usage:")
    print("  from scripts.hpc.utils.retry import retry_with_backoff")
    print("  from scripts.hpc.utils.retry import retry_on_rate_limit")
    print("  from scripts.hpc.utils.retry import get_robust_session")
