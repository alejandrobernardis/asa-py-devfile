#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2024/01/13

import asyncio
import uvloop
from aiohttp import web
from service import api


async def serve() -> web.Application:
    app: web.Application = web.Application()
    api.init(app)
    return app


def main() -> bool:
    uvloop.install()
    loop = asyncio.get_event_loop()
    task = loop.create_task(serve())
    app = loop.run_until_complete(task)

    try:
        web.run_app(app, host='0.0.0.0', port=8081)

    except Exception as e:
        app.logger.fatal(f'main loop -> {e}')
        return True


if __name__ == '__main__':
    while main():
        pass
