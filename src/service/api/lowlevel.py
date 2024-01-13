#!/usr/bin/env python
# Author: Alejandro M. BERNARDIS
# Email alejandro.bernardis at gmail dot com
# Created: 2024/01/13

import json
from aiohttp import web
from http import HTTPStatus


def default_response(
        data: dict = None,
        status=HTTPStatus.OK,
        **kwargs
) -> web.Response:
    return web.Response(
        text=json.dumps(data) if data else None,
        status=status,
        content_type='application/json',
        **kwargs
    )


async def default_handler(_: web.Request) -> web.Response:
    return default_response(dict(
        server='Astor PIAZZOLLA',
        version='1.0.0'
    ))


def init(app: web.Application, **kwargs) -> None:
    app.router.add_get('/', default_handler)
