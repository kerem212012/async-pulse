import asyncio
import time
from dataclasses import dataclass

import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

URLS = [
    "https://httpbin.org/get",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://google.com",
    "https://example.com",
    "https://httpbin.org/delay/11",
]
REQUEST_TIMEOUT = 10.0


@dataclass
class CheckResult:
    url: str
    status: int | None
    elapsed_ms: int
    error: str | None = None


async def check_url(
    client: httpx.AsyncClient, url: str, progress: Progress, task_id: int
) -> CheckResult:
    start = time.perf_counter()
    try:
        response = await client.get(url, timeout=REQUEST_TIMEOUT)
        return CheckResult(
            url=url,
            status=response.status_code,
            elapsed_ms=int((time.perf_counter() - start) * 1000),
        )
    except httpx.TimeoutException as error:
        return CheckResult(
            url=url,
            status=None,
            elapsed_ms=int((time.perf_counter() - start) * 1000),
            error=f"Timeout after {REQUEST_TIMEOUT:g} seconds: {error}",
        )
    except httpx.RequestError as error:
        return CheckResult(
            url=url,
            status=None,
            elapsed_ms=int((time.perf_counter() - start) * 1000),
            error=f"Request failed: {error}",
        )
    finally:
        progress.advance(task_id)


async def fetch_urls(urls: list[str]) -> tuple[list[CheckResult], float]:
    start = time.perf_counter()
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        console=console,
    ) as progress:
        task_id = progress.add_task("Checking URLs...", total=len(urls))
        async with httpx.AsyncClient() as client:
            results = await asyncio.gather(
                *(check_url(client, url, progress, task_id) for url in urls)
            )
    return results, time.perf_counter() - start


async def run(urls: list[str]) -> None:
    results, total_seconds = await fetch_urls(urls)
    table = Table(title=f"AsyncPulse Results (total: {total_seconds:.2f} s)")
    table.add_column("URL")
    table.add_column("Status", justify="right")
    table.add_column("ms", justify="right")
    table.add_column("Error")

    for result in results:
        if result.status is None:
            status = "[red]TIMEOUT[/red]" if result.error and result.error.startswith(
                "Timeout"
            ) else "[red]ERROR[/red]"
        elif 200 <= result.status < 300:
            status = f"[green]{result.status}[/green]"
        elif 400 <= result.status < 500:
            status = f"[yellow]{result.status}[/yellow]"
        elif 500 <= result.status < 600:
            status = f"[red]{result.status}[/red]"
        else:
            status = str(result.status)

        table.add_row(
            result.url,
            status,
            str(result.elapsed_ms),
            result.error or "",
        )

    console.print(table)


def main() -> None:
    asyncio.run(run(URLS))


__all__ = ["main"]
