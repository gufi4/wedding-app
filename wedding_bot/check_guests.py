import asyncio
from services.guest_service import guest_service

async def main():
    guests = await guest_service.get_all_guests()
    for guest in guests:
        print(f"ID: {guest.id}, Name: {guest.name}, Comment: {guest.comment}")

asyncio.run(main())
