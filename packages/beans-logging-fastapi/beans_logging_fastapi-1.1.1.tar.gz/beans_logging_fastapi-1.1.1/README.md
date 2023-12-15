# beans_logging_fastapi

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bybatkhuu/module.fastapi-logging/2.build-publish.yml?logo=GitHub)](https://github.com/bybatkhuu/module.fastapi-logging/actions/workflows/2.build-publish.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/bybatkhuu/module.fastapi-logging?logo=GitHub)](https://github.com/bybatkhuu/module.fastapi-logging/releases)
[![PyPI](https://img.shields.io/pypi/v/beans-logging-fastapi?logo=PyPi)](https://pypi.org/project/beans-logging-fastapi)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beans-logging-fastapi?logo=Python)](https://docs.conda.io/en/latest/miniconda.html)

`beans_logging_fastapi` is a middleware for FastAPI to log HTTP access.

It is based on **'beans-logging'** package.

## Features

- **Logger** based on **'beans-logging'** package
- **FastAPI** HTTP access logging **middleware**

---

## Installation

### 1. Prerequisites

- **Python (>= v3.8)**
- **PyPi (>= v23)**

### 2. Install beans-logging-fastapi package

Choose one of the following methods to install the package **[A ~ F]**:

**A.** [**RECOMMENDED**] Install from **PyPi**

```sh
# Install or upgrade package:
pip install -U beans-logging-fastapi
```

**B.** Install latest version from **GitHub**

```sh
# Install package by git:
pip install git+https://github.com/bybatkhuu/module.fastapi-logging.git
```

**C.** Install from **pre-built release** files

1. Download **`.whl`** or **`.tar.gz`** file from **releases** - <https://github.com/bybatkhuu/module.fastapi-logging/releases>
2. Install with pip:

```sh
# Install from .whl file:
pip install ./beans_logging_fastapi-[VERSION]-py3-none-any.whl
# Or install from .tar.gz file:
pip install ./beans_logging_fastapi-[VERSION].tar.gz
```

**D.** Install from **source code** by building package

```sh
# Clone repository by git:
git clone https://github.com/bybatkhuu/module.fastapi-logging.git beans_logging_fastapi
cd ./beans_logging_fastapi

# Install python build tool:
pip install -U pip build

# Build python package:
python -m build

_VERSION=$(./scripts/get-version.sh)

# Install from .whl file:
pip install ./dist/beans_logging_fastapi-${_VERSION}-py3-none-any.whl
# Or install from .tar.gz file:
pip install ./dist/beans_logging_fastapi-${_VERSION}.tar.gz
```

**E.** Install with pip editable **development mode** (from source code)

```sh
# Clone repository by git:
git clone https://github.com/bybatkhuu/module.fastapi-logging.git beans_logging_fastapi
cd ./beans_logging_fastapi

# Install with editable development mode:
pip install -e .
```

**F.** Manually add to **PYTHONPATH** (not recommended)

```sh
# Clone repository by git:
git clone https://github.com/bybatkhuu/module.fastapi-logging.git beans_logging_fastapi
cd ./beans_logging_fastapi

# Install python dependencies:
pip install -r ./requirements.txt

# Add current path to PYTHONPATH:
export PYTHONPATH="${PWD}:${PYTHONPATH}"
```

## Usage/Examples

To use `beans_logging_fastapi`:

### **FastAPI**

[**`configs/logger.yml`**](https://github.com/bybatkhuu/module.fastapi-logging/blob/main/examples/configs/logger.yml):

```yaml
logger:
  app_name: "fastapi-app"
  level: "TRACE"
  use_diagnose: false
  stream:
    use_color: true
    use_icon: false
    format_str: "[<c>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</c> | <level>{level_short:<5}</level> | <w>{name}:{line}</w>]: <level>{message}</level>"
    std_handler:
      enabled: true
  file:
    logs_dir: "./logs"
    rotate_size: 10000000 # 10MB
    rotate_time: "00:00:00"
    backup_count: 90
    log_handlers:
      enabled: true
      format_str: "[{time:YYYY-MM-DD HH:mm:ss.SSS Z} | {level_short:<5} | {name}:{line}]: {message}"
      log_path: "{app_name}.std.all.log"
      err_path: "{app_name}.std.err.log"
    json_handlers:
      enabled: true
      use_custom: false
      log_path: "json/{app_name}.json.all.log"
      err_path: "json/{app_name}.json.err.log"
  intercept:
    auto_load:
      enabled: true
      only_base: false
      ignore_modules: []
    include_modules: []
    mute_modules: ["uvicorn.access"]
  extra:
    http_std_debug_format: '<n>[{request_id}]</n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"'
    http_std_msg_format: '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" {status_code} {content_length}B {response_time}ms'
    http_file_enabled: true
    http_file_format: '{client_host} {request_id} {user_id} [{datetime}] "{method} {url_path} HTTP/{http_version}" {status_code} {content_length} "{h_referer}" "{h_user_agent}" {response_time}'
    http_file_tz: "localtime"
    http_log_path: "http/{app_name}.http.access.log"
    http_err_path: "http/{app_name}.http.err.log"
    http_json_enabled: true
    http_json_path: "json.http/{app_name}.json.http.access.log"
    http_json_err_path: "json.http/{app_name}.json.http.err.log"
```

[**`.env`**](https://github.com/bybatkhuu/module.fastapi-logging/blob/main/examples/.env):

```sh
ENV=development
DEBUG=true

BEANS_LOGGING_DISABLE_DEFAULT=false
BEANS_LOGGING_CONFIG_PATH="./configs/logger.yml"
BEANS_LOGGING_LOGS_DIR="./logs"
```

[**`logger.py`**](https://github.com/bybatkhuu/module.fastapi-logging/blob/main/examples/logger.py):

```python
from beans_logging import Logger, LoggerLoader
from beans_logging_fastapi import (
    add_http_file_handler,
    add_http_file_json_handler,
    http_file_format,
)

logger_loader = LoggerLoader()
logger: Logger = logger_loader.load()


def _http_file_format(record: dict) -> str:
    _format = http_file_format(
        record=record,
        msg_format=logger_loader.config.extra.http_file_format,
        tz=logger_loader.config.extra.http_file_tz,
    )
    return _format


if logger_loader.config.extra.http_file_enabled:
    add_http_file_handler(
        logger_loader=logger_loader,
        log_path=logger_loader.config.extra.http_log_path,
        err_path=logger_loader.config.extra.http_err_path,
        formatter=_http_file_format,
    )

if logger_loader.config.extra.http_json_enabled:
    add_http_file_json_handler(
        logger_loader=logger_loader,
        log_path=logger_loader.config.extra.http_json_path,
        err_path=logger_loader.config.extra.http_json_err_path,
    )
```

[**`main.py`**](https://github.com/bybatkhuu/module.fastapi-logging/blob/main/examples/main.py):

```python
from typing import Union
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

load_dotenv()

from beans_logging_fastapi import (
    HttpAccessLogMiddleware,
    RequestHTTPInfoMiddleware,
    ResponseHTTPInfoMiddleware,
)

from logger import logger, logger_loader
from __version__ import __version__


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Preparing to startup...")
    logger.success("Finished preparation to startup.")
    logger.info(f"API version: {__version__}")

    yield
    logger.info("Praparing to shutdown...")
    logger.success("Finished preparation to shutdown.")


app = FastAPI(lifespan=lifespan, version=__version__)

app.add_middleware(ResponseHTTPInfoMiddleware)
app.add_middleware(
    HttpAccessLogMiddleware,
    debug_format=logger_loader.config.extra.http_std_debug_format,
    msg_format=logger_loader.config.extra.http_std_msg_format,
)
app.add_middleware(
    RequestHTTPInfoMiddleware, has_proxy_headers=True, has_cf_headers=True
)


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/continue", status_code=100)
def get_continue():
    return {}


@app.get("/redirect")
def redirect():
    return RedirectResponse("/")


@app.get("/error")
def error():
    raise HTTPException(status_code=500)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        access_log=False,
        server_header=False,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
```

Run the [**`examples`**](https://github.com/bybatkhuu/module.fastapi-logging/tree/main/examples):

```sh
cd ./examples
# Install python dependencies for examples:
pip install -r ./requirements.txt

uvicorn main:app --host=0.0.0.0 --port=8000
```

**Output**:

```txt
[2023-10-31 12:38:46.733 +09:00 | TRACE | beans_logging._base:578]: Intercepted modules: ['concurrent', 'concurrent.futures', 'watchfiles.watcher', 'dotenv.main', 'watchfiles.main', 'watchfiles', 'asyncio', 'fastapi', 'uvicorn.error', 'uvicorn', 'dotenv']; Muted modules: ['uvicorn.access'];
[2023-10-31 12:38:46.749 +09:00 | INFO  | uvicorn.server:76]: Started server process [56216]
[2023-10-31 12:38:46.749 +09:00 | INFO  | uvicorn.lifespan.on:46]: Waiting for application startup.
[2023-10-31 12:38:46.750 +09:00 | INFO  | main:26]: Preparing to startup...
[2023-10-31 12:38:46.750 +09:00 | OK    | main:27]: Finished preparation to startup.
[2023-10-31 12:38:46.750 +09:00 | INFO  | main:28]: API version: 0.0.0-000000
[2023-10-31 12:38:46.750 +09:00 | INFO  | uvicorn.lifespan.on:60]: Application startup complete.
[2023-10-31 12:38:46.752 +09:00 | INFO  | uvicorn.server:218]: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
[2023-10-31 12:38:48.701 +09:00 | DEBUG | anyio._backends._asyncio:807]: [c3d76377250947c29559cb103a6d2c56] 127.0.0.1 - "GET / HTTP/1.1"
[2023-10-31 12:38:48.703 +09:00 | OK    | anyio._backends._asyncio:807]: [c3d76377250947c29559cb103a6d2c56] 127.0.0.1 - "GET / HTTP/1.1" 200 17B 0.8ms
^C[2023-10-31 12:38:49.793 +09:00 | INFO  | uvicorn.server:264]: Shutting down
[2023-10-31 12:38:49.903 +09:00 | INFO  | uvicorn.lifespan.on:65]: Waiting for application shutdown.
[2023-10-31 12:38:49.903 +09:00 | INFO  | main:31]: Praparing to shutdown...
[2023-10-31 12:38:49.904 +09:00 | OK    | main:32]: Finished preparation to shutdown.
[2023-10-31 12:38:49.904 +09:00 | INFO  | uvicorn.lifespan.on:76]: Application shutdown complete.
[2023-10-31 12:38:49.904 +09:00 | INFO  | uvicorn.server:86]: Finished server process [56216]
```

---

## Running Tests

To run tests, run the following command:

```sh
# Install python test dependencies:
pip install -r ./requirements.test.txt

# Run tests:
python -m pytest -sv
```

## Environment Variables

You can use the following environment variables inside [**`.env.example`**](https://github.com/bybatkhuu/module.fastapi-logging/blob/main/.env.example) file:

```sh
ENV=development
DEBUG=true

BEANS_LOGGING_DISABLE_DEFAULT=false
BEANS_LOGGING_CONFIG_PATH="./configs/logger.yml"
BEANS_LOGGING_LOGS_DIR="./logs"
```

## Documentation

- [docs](https://github.com/bybatkhuu/module.fastapi-logging/blob/main/docs/README.md)
- [scripts](https://github.com/bybatkhuu/module.fastapi-logging/blob/main/docs/scripts/README.md)

---

## References

- <https://github.com/bybatkhuu/module.python-logging>
- <https://github.com/Delgan/loguru>
- <https://loguru.readthedocs.io/en/stable/api/logger.html>
- <https://loguru.readthedocs.io/en/stable/resources/recipes.html>
