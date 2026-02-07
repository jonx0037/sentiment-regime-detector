"""
Checkpoint Management Utilities for HPC Pipeline

Provides robust checkpoint saving and loading to allow jobs to resume
after failures without losing progress.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional, List
import hashlib

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CheckpointManager:
    """
    Manages checkpoint files for resumable job execution

    Example:
        checkpoint = CheckpointManager('logs/checkpoint_batch_0.json')

        # Load existing progress
        state = checkpoint.load()
        completed_dates = set(state.get('completed_dates', []))

        # Process remaining items
        for date in all_dates:
            if date in completed_dates:
                continue

            process(date)
            completed_dates.add(date)

            # Save progress
            checkpoint.save({
                'completed_dates': list(completed_dates),
                'last_date': date
            })
    """

    def __init__(self, checkpoint_file: str):
        """
        Initialize checkpoint manager

        Args:
            checkpoint_file: Path to checkpoint JSON file
        """
        self.checkpoint_file = Path(checkpoint_file)
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

    def save(self, state: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None):
        """
        Save checkpoint state to file

        Args:
            state: Dictionary containing checkpoint state
            metadata: Optional metadata (batch_id, phase, etc.)
        """
        checkpoint = {
            'state': state,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }

        try:
            # Write to temporary file first (atomic write)
            temp_file = self.checkpoint_file.with_suffix('.tmp')
            with open(temp_file, 'w') as f:
                json.dump(checkpoint, f, indent=2)

            # Atomic rename
            temp_file.replace(self.checkpoint_file)

            logger.info(f"Checkpoint saved: {self.checkpoint_file}")

        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")
            raise

    def load(self) -> Dict[str, Any]:
        """
        Load checkpoint state from file

        Returns:
            Dictionary containing checkpoint state, or empty dict if no checkpoint exists
        """
        if not self.checkpoint_file.exists():
            logger.info(f"No checkpoint found at {self.checkpoint_file}, starting fresh")
            return {}

        try:
            with open(self.checkpoint_file) as f:
                checkpoint = json.load(f)

            state = checkpoint.get('state', {})
            timestamp = checkpoint.get('timestamp', 'unknown')

            logger.info(f"Checkpoint loaded from {timestamp}")
            logger.info(f"Resuming from checkpoint: {self.checkpoint_file}")

            return state

        except json.JSONDecodeError as e:
            logger.error(f"Corrupted checkpoint file: {e}")
            logger.warning("Starting fresh (corrupted checkpoint ignored)")
            return {}

        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            raise

    def exists(self) -> bool:
        """Check if checkpoint file exists"""
        return self.checkpoint_file.exists()

    def delete(self):
        """Delete checkpoint file (call after successful completion)"""
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()
            logger.info(f"Checkpoint deleted: {self.checkpoint_file}")

    def get_metadata(self) -> Dict[str, Any]:
        """Get checkpoint metadata without loading full state"""
        if not self.checkpoint_file.exists():
            return {}

        try:
            with open(self.checkpoint_file) as f:
                checkpoint = json.load(f)
            return checkpoint.get('metadata', {})
        except Exception:
            return {}


class ProgressTracker:
    """
    Tracks progress for iterable jobs with automatic checkpointing

    Example:
        tracker = ProgressTracker('logs/progress_batch_0.json', total=1000)

        for item in tracker.track(items):
            process(item)
            tracker.increment()  # Auto-saves checkpoint every N items
    """

    def __init__(
        self,
        checkpoint_file: str,
        total: Optional[int] = None,
        checkpoint_interval: int = 100
    ):
        """
        Initialize progress tracker

        Args:
            checkpoint_file: Path to checkpoint file
            total: Total number of items (optional, for progress reporting)
            checkpoint_interval: Save checkpoint every N items (default: 100)
        """
        self.manager = CheckpointManager(checkpoint_file)
        self.total = total
        self.checkpoint_interval = checkpoint_interval

        # Load existing progress
        state = self.manager.load()
        self.completed = state.get('completed', 0)
        self.failed = state.get('failed', 0)
        self.completed_ids = set(state.get('completed_ids', []))
        self.failed_ids = set(state.get('failed_ids', []))

        self._items_since_checkpoint = 0

    def is_completed(self, item_id: str) -> bool:
        """Check if item has already been completed"""
        return item_id in self.completed_ids

    def mark_completed(self, item_id: str):
        """Mark item as completed and checkpoint if needed"""
        if item_id not in self.completed_ids:
            self.completed_ids.add(item_id)
            self.completed += 1
            self._items_since_checkpoint += 1

            # Auto-checkpoint at intervals
            if self._items_since_checkpoint >= self.checkpoint_interval:
                self._save_checkpoint()
                self._items_since_checkpoint = 0

    def mark_failed(self, item_id: str):
        """Mark item as failed"""
        if item_id not in self.failed_ids:
            self.failed_ids.add(item_id)
            self.failed += 1

    def _save_checkpoint(self):
        """Save current progress"""
        self.manager.save({
            'completed': self.completed,
            'failed': self.failed,
            'completed_ids': list(self.completed_ids),
            'failed_ids': list(self.failed_ids)
        })

    def track(self, items: List[Any]):
        """
        Iterator that tracks progress and skips completed items

        Args:
            items: List of items to process

        Yields:
            Items that haven't been completed yet
        """
        for item in items:
            # Generate item ID (hash if not string)
            if isinstance(item, str):
                item_id = item
            else:
                item_id = hashlib.md5(str(item).encode()).hexdigest()[:16]

            # Skip if already completed
            if self.is_completed(item_id):
                continue

            yield item

    def get_progress(self) -> Dict[str, Any]:
        """Get current progress statistics"""
        progress = {
            'completed': self.completed,
            'failed': self.failed,
            'total': self.total
        }

        if self.total:
            progress['percent'] = (self.completed / self.total) * 100

        return progress

    def finalize(self):
        """Save final checkpoint and clean up"""
        self._save_checkpoint()
        logger.info(f"Progress complete: {self.completed} completed, {self.failed} failed")


def checkpoint_function(checkpoint_file: str):
    """
    Decorator to add automatic checkpointing to a function

    The decorated function will save its return value to a checkpoint file.
    If the checkpoint exists, it will be loaded and returned instead of re-running the function.

    Args:
        checkpoint_file: Path to checkpoint file

    Example:
        @checkpoint_function('logs/expensive_computation.json')
        def expensive_computation(data):
            # This only runs once, result is cached
            return process_for_hours(data)

        result = expensive_computation(my_data)  # First call: runs function
        result = expensive_computation(my_data)  # Second call: loads from checkpoint
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            manager = CheckpointManager(checkpoint_file)

            # Check if checkpoint exists
            if manager.exists():
                logger.info(f"Loading cached result from {checkpoint_file}")
                state = manager.load()
                return state.get('result')

            # Run function and save result
            logger.info(f"Computing result (will be cached to {checkpoint_file})")
            result = func(*args, **kwargs)

            manager.save({'result': result}, metadata={
                'function': func.__name__,
                'args': str(args)[:100],  # Truncate long args
                'kwargs': str(kwargs)[:100]
            })

            return result

        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    # Example 1: Basic checkpoint manager
    print("Example 1: Basic CheckpointManager")
    checkpoint = CheckpointManager('logs/test_checkpoint.json')

    # Simulate processing with checkpoints
    completed_items = set(checkpoint.load().get('completed_items', []))

    for i in range(10):
        if i not in completed_items:
            print(f"Processing item {i}")
            completed_items.add(i)

            checkpoint.save({
                'completed_items': list(completed_items),
                'last_item': i
            }, metadata={'batch_id': 0})

    checkpoint.delete()

    # Example 2: Progress tracker
    print("\nExample 2: ProgressTracker")
    tracker = ProgressTracker('logs/test_progress.json', total=100, checkpoint_interval=10)

    items = [f"item_{i}" for i in range(100)]
    for item in tracker.track(items):
        # Process item
        tracker.mark_completed(item)

    tracker.finalize()

    # Example 3: Function checkpointing
    print("\nExample 3: Function checkpointing")

    @checkpoint_function('logs/test_function.json')
    def slow_computation(n):
        """Simulate expensive computation"""
        import time
        time.sleep(0.1)
        return sum(range(n))

    result = slow_computation(1000)  # First call: computes
    result = slow_computation(1000)  # Second call: loads from checkpoint

    print(f"Result: {result}")
