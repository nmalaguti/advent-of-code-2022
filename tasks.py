from pathlib import Path
from shutil import copyfile

from invoke import task


@task
def new_day(c):
    curr_dir = Path(__file__).parent
    last_day = next(reversed(sorted(list(curr_dir.glob("day-*")))), None)
    if last_day is None:
        next_day = 1
    else:
        next_day = int(last_day.name[4:]) + 1
    next_day_dir = curr_dir / f"day-{next_day:02d}"
    next_day_dir.mkdir()
    copyfile(curr_dir / "template.py", next_day_dir / f"day_{next_day:02d}.py")
    (next_day_dir / "input").touch()
