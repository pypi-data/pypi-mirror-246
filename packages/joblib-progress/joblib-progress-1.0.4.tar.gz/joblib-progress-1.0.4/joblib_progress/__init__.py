import contextlib
from typing import Optional

import joblib
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

__version__ = "1.0.4"


@contextlib.contextmanager
def joblib_progress(description: Optional[str] = None, total: Optional[int] = None):
    if description is None:
        description = "Processing..."

    progress = Progress(
        SpinnerColumn(),
        TaskProgressColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        "<",
        TimeRemainingColumn(),
    )
    task_id = progress.add_task(f"[cyan]{description}", total=total)

    class BatchCompletionCallback(joblib.parallel.BatchCompletionCallBack):
        def __call__(self, *args, **kwargs):
            progress.update(task_id, advance=self.batch_size, refresh=True)
            return super().__call__(*args, **kwargs)

    old_callback = joblib.parallel.BatchCompletionCallBack

    try:
        joblib.parallel.BatchCompletionCallBack = BatchCompletionCallback
        progress.start()

        yield progress
    finally:
        progress.stop()
        joblib.parallel.BatchCompletionCallBack = old_callback
