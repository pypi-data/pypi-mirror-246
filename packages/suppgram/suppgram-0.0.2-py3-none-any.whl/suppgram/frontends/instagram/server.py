from aiohttp import web
from aiohttp.abc import Request


async def handle(request: Request):
    print(request.query, request.headers)
    return web.Response(status=200, text=request.query["hub.challenge"])


app = web.Application()
app.add_routes([web.get("/", handle)])

if __name__ == "__main__":
    web.run_app(app, port=8765)
