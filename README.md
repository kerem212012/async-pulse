# AsyncPulse

AsyncPulse checks a list of URLs concurrently and displays each HTTP status,
request duration, and any timeout or connection error in a Rich table.

Run it from the project directory:

```powershell
uv run main.py
```

The default URL list includes successful responses, HTTP 404 and 500 responses,
and a request that exceeds the 10-second timeout.