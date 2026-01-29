"""API route handlers"""

import json
from aiohttp import web
from services.guest_service import guest_service
from services.notification_service import NotificationService
from api.schemas import GuestRegistrationRequest, GuestResponse, ErrorResponse


async def register_guest(request: web.Request) -> web.Response:
    """
    Handle guest registration via HTTP API

    Expected JSON body:
    {
        "name": "Guest Name",
        "guest_count": 2,
        "confirmation_status": "confirmed",
        "comment": "Optional comment"
    }

    Returns:
        201: Guest created successfully
        400: Validation error
        500: Internal server error
    """
    try:
        # Parse JSON from request with encoding fallback
        try:
            data = await request.json()
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Try to handle different encodings (e.g., cp1251 from Windows curl)
            body = await request.read()
            if body:
                # Fallback to cp1251 (common Windows encoding)
                try:
                    decoded_body = body.decode('cp1251')
                    data = json.loads(decoded_body)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    # Try UTF-8 as last resort
                    decoded_body = body.decode('utf-8')
                    data = json.loads(decoded_body)
            else:
                raise

        # Create request object
        req = GuestRegistrationRequest(
            name=data.get("name", ""),
            guest_count=data.get("guest_count", 1),
            confirmation_status=data.get("confirmation_status", "pending"),
            comment=data.get("comment")
        )

        # Debug: print the name and comment to verify encoding
        print(f"DEBUG: name='{req.name}', comment='{req.comment}'")

        # Validate request
        is_valid, error_message = req.validate()
        if not is_valid:
            return web.json_response({
                "success": False,
                "error": ErrorResponse("VALIDATION_ERROR", error_message).to_dict()
            }, status=400)

        # Create guest in database
        guest = await guest_service.create_guest(
            name=req.name.strip(),
            guest_count=req.guest_count,
            confirmation_status=req.confirmation_status,
            comment=req.comment.strip() if req.comment else None
        )

        # Notify bride and groom via Telegram
        bot = request.app.get("bot")
        if bot:
            notification_service = NotificationService(bot)
            await notification_service.notify_about_new_guest(guest)

        # Return success response
        return web.json_response({
            "success": True,
            "data": GuestResponse.from_guest(guest).to_dict()
        }, status=201)

    except KeyError as e:
        return web.json_response({
            "success": False,
            "error": ErrorResponse("INVALID_REQUEST", f"Missing required field: {str(e)}").to_dict()
        }, status=400)

    except Exception as e:
        # Log error for debugging
        print(f"Error in register_guest: {e}")
        return web.json_response({
            "success": False,
            "error": ErrorResponse("INTERNAL_ERROR", str(e)).to_dict()
        }, status=500)


async def health_check(request: web.Request) -> web.Response:
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "service": "wedding-bot-api"
    })
