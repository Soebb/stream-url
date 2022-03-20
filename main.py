from aiohttp import web
import aiohttp
import logging

logging.basicConfig(level=logging.INFO)

async def hello(request):
    return web.Response(text="Hello, world")


async def streamer(request):
    url = request.match_info['url']
    
    if url[:4] != "http":
        url = "http://"+url
    elif url[:5] != "https":
        url = "https://"+url

    headers = {}
    
    if range := request.headers.get("Range"):
        headers["Range"] = range
    
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url) as r:
                response = web.StreamResponse(
                    status=r.status,
                    headers=r.headers,
                )
                
                await response.prepare(request)
                
                async for chunk in r.content.iter_any():
                    await response.write(chunk)
                    
                return response

        except aiohttp.client_exceptions.InvalidURL:
            return web.HTTPBadRequest()
            
        except aiohttp.client_exceptions.ClientConnectorError:
            return web.HTTPNotFound()


async def main():
    app = web.Application()
    app.add_routes([
        web.get('/', hello),
        web.get('/{url:(.*)}',streamer),
    ])
    return app

if __name__ == "__main__":
    web.run_app(main())
