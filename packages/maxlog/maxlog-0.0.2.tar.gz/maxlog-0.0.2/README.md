# maxlog

[![PyPI version](https://badge.fury.io/py/maxlog.svg)](https://badge.fury.io/py/maxlog)
## Installation

```bash
pip install maxlog
```

## Usage

```python
# Create an instance of the Log class
log = Log(rich_level="INFO", project_dir="/path/to/project")

# Log messages at different levels
log.info("This is an informational message")
log.warning("This is a warning message")
log.error("This is an error message")

# Change the rich level to log only messages with level DEBUG and above
log.rich_level = "DEBUG"

# Log a message with level DEBUG
log.debug("This is a debug message")
```
## Output

## Created by Max Ludden

![Max Ludden's Logo](https://private-user-images.githubusercontent.com/51646468/284406500-dff29293-4afb-40a5-8e1a-275108898845.svg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTEiLCJleHAiOjE3MDI4MjgxMTUsIm5iZiI6MTcwMjgyNzgxNSwicGF0aCI6Ii81MTY0NjQ2OC8yODQ0MDY1MDAtZGZmMjkyOTMtNGFmYi00MGE1LThlMWEtMjc1MTA4ODk4ODQ1LnN2Zz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFJV05KWUFYNENTVkVINTNBJTJGMjAyMzEyMTclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjMxMjE3VDE1NDMzNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWJhOTk1MThkYTM5MmExZjIwZWJjZmFhY2NiNDYwNDYyMjM4NDNlMzk1OWI1YjJiZDgyODdkNGIwY2JhNzc2Y2EmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.4KAmyPb43Tvt8UgDzfOpw3lN5aP0G8XjJT69tDbIvY8)
