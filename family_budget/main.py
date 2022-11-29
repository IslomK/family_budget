import os

import click
import uvicorn

from family_budget.core import const
from family_budget.core.config import get_settings

settings = get_settings()


@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
@click.option(
    "--gunicorn-workers",
    help="number of gunicorn workers to spawn",
    type=int,
    default=const.DEFAULT_GUNICORN_WORKERS,
)
def main(env: str, debug: bool, gunicorn_workers: int):
    os.environ["ENVIRONMENT"] = env
    os.environ["DEBUG"] = str(debug)

    if env == "local":
        gunicorn_workers = 1

    uvicorn.run(
        app="family_budget.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True if settings.ENVIRONMENT != "production" else False,
        workers=gunicorn_workers,
        log_level=settings.LOG_LEVEL,
    )


if __name__ == "__main__":
    main()
