"""HTTP server setup for API"""

from aiohttp import web
from api.routes import register_guest, health_check
from config import Config


@web.middleware
async def cors_middleware(request, handler):
    """CORS middleware to allow requests from any origin"""
    response = await handler(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


async def handle_options(request):
    """Handle OPTIONS request for CORS preflight"""
    return web.Response(status=200)


def create_http_server(bot):
    """
    Create and configure HTTP server

    Args:
        bot: Telegram bot instance for sending notifications

    Returns:
        web.AppRunner: Configured app runner
    """
    # Create app with CORS middleware
    app = web.Application(middlewares=[cors_middleware])

    # Store bot instance for use in routes
    app["bot"] = bot

    # Register routes
    app.router.add_post("/api/v1/guests/register", register_guest)
    app.router.add_get("/health", health_check)
    app.router.add_options("/api/v1/guests/register", handle_options)

    # Create runner
    runner = web.AppRunner(app)

    return runner


async def setup_http_server(runner):
    """
    Setup and start HTTP server

    Args:
        runner: AppRunner from create_http_server()
    """
    await runner.setup()
    site = web.TCPSite(runner, Config.API_HOST, Config.API_PORT)
    await site.start()
    print(f"🌐 HTTP API server started on http://{Config.API_HOST}:{Config.API_PORT}")
