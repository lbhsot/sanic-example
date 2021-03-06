from sanic import Sanic
from aoiklivereload import LiveReloader
import asyncio
import uvloop
import logging

import config

from blueprints import Blueprints
from database import init_db


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

loop = asyncio.get_event_loop()

app = Sanic(__name__)

app.blueprint(Blueprints.auth, url_prefix='/api/auth')

loop.create_task(init_db())

# TODO: Put somewhere for better code style
if config.DEBUG:
    reloader = LiveReloader()
    reloader.start_watcher_thread()

    @app.middleware('response')
    async def request_log(request, response):
        logging.info(
            f'{request.method} - {request.url} - {response.status}')


if __name__ == '__main__':
    app.go_fast(port=config.PORT, workers=config.WORKERS,
                debug=config.DEBUG, loop=loop)
