from __future__ import annotations

import contextlib
from pathlib import Path
from typing import TYPE_CHECKING, Any, MutableMapping

from anyio import create_task_group
from jinja2 import select_autoescape
from litestar.serialization import encode_json

if TYPE_CHECKING:
    from anyio.abc import Process
    from jinja2 import Environment, Template
    from litestar import Litestar

VITE_INIT_TEMPLATES_PATH = f"{Path(__file__).parent}/templates/init"
VITE_INIT_TEMPLATES: set[str] = {"package.json.j2", "tsconfig.json.j2", "vite.config.ts.j2"}

DEFAULT_DEV_DEPENDENCIES: dict[str, str] = {
    "axios": "^1.6.2",
    "typescript": "^5.3.3",
    "vite": "^5.0.6",
    "litestar-vite-plugin": "^0.3.0",
    "@types/node": "^20.10.3",
}
DEFAULT_DEPENDENCIES: dict[str, str] = {}


def to_json(value: Any) -> str:
    """Serialize JSON field values.

    Args:
        value: Any json serializable value.

    Returns:
        JSON string.
    """
    return encode_json(value).decode("utf-8")


def init_vite(
    app: Litestar,
    root_path: Path,
    resource_path: Path,
    asset_url: str,
    bundle_path: Path,
    enable_ssr: bool,
    vite_port: int,
    hot_file: Path,
    litestar_port: int,
) -> None:
    """Initialize a new vite project."""
    from jinja2 import Environment, FileSystemLoader

    entry_point: list[str] = []
    vite_template_env = Environment(
        loader=FileSystemLoader([VITE_INIT_TEMPLATES_PATH]),
        autoescape=select_autoescape(),
    )

    logger = app.get_logger()
    enabled_templates: set[str] = VITE_INIT_TEMPLATES
    dependencies: dict[str, str] = DEFAULT_DEPENDENCIES
    dev_dependencies: dict[str, str] = DEFAULT_DEV_DEPENDENCIES
    templates: dict[str, Template] = {
        template_name: get_template(environment=vite_template_env, name=template_name)
        for template_name in enabled_templates
    }
    for template_name, template in templates.items():
        target_file_name = template_name.removesuffix(".j2")
        with Path(target_file_name).open(mode="w") as file:
            logger.info("Writing %s", target_file_name)

            file.write(
                template.render(
                    entry_point=entry_point,
                    enable_ssr=enable_ssr,
                    asset_url=asset_url,
                    root_path=str(root_path),
                    resource_path=str(resource_path.relative_to(root_path)),
                    bundle_path=str(bundle_path.relative_to(root_path)),
                    hot_file=str(hot_file.relative_to(root_path)),
                    vite_port=str(vite_port),
                    litestar_port=litestar_port,
                    dependencies=to_json(dependencies),
                    dev_dependencies=to_json(dev_dependencies),
                ),
            )


def get_template(
    environment: Environment,
    name: str | Template,
    parent: str | None = None,
    globals: MutableMapping[str, Any] | None = None,  # noqa: A002
) -> Template:
    return environment.get_template(name=name, parent=parent, globals=globals)


def run_vite(command_to_run: str, app: Litestar) -> None:
    """Run Vite in a subprocess."""

    import anyio

    with contextlib.suppress(KeyboardInterrupt):
        anyio.run(_run_vite, command_to_run, app)


async def _run_vite(command_to_run: str, app: Litestar) -> None:
    """Run Vite in a subprocess."""

    from anyio import open_process
    from anyio.streams.text import TextReceiveStream

    logger = app.get_logger("vite")

    async def read_stdout(vite_process: Process) -> None:
        async for stdout in TextReceiveStream(vite_process.stdout):  # type: ignore[arg-type]
            logger.info(stdout.replace("\n", ""))

    async def read_stderr(vite_process: Process) -> None:
        async for stdout in TextReceiveStream(vite_process.stderr):  # type: ignore[arg-type]
            logger.warning(stdout.replace("\n", ""))

    async with await open_process(command_to_run) as vite_process, create_task_group() as tg:
        tg.start_soon(read_stdout, vite_process)
        tg.start_soon(read_stderr, vite_process)
