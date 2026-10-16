# AsyncPulse

AsyncPulse is a small command-line tool that checks a predefined list of URLs
concurrently and displays the results in a terminal table.

For each URL, it reports the HTTP status code, request duration in milliseconds,
and any timeout or request error. The table also shows the total time taken to
check all URLs. Successful responses, client errors, and server errors are
highlighted with different colors.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)

## Run

From the project directory, run either:

```powershell
uv run main.py
```

or the installed project command:

```powershell
uv run async-pulse
```

`uv` installs the project dependencies from `pyproject.toml` when needed.

## URLs checked

The URL list is currently defined in the source code:

- `https://httpbin.org/get`
- `https://httpbin.org/status/404`
- `https://httpbin.org/status/500`
- `https://google.com`
- `https://example.com`
- `https://httpbin.org/delay/11`

Each request has a 10-second timeout. The delayed httpbin request is included
to demonstrate timeout reporting. The URLs require an internet connection and
may return different results depending on network availability or the remote
services.
