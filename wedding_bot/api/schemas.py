"""Request and response schemas for API"""

from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class GuestRegistrationRequest:
    """Schema for guest registration request"""
    name: str
    guest_count: int
    confirmation_status: str
    comment: Optional[str] = None

    VALID_STATUSES = ["confirmed", "declined", "pending"]

    def validate(self) -> Tuple[bool, Optional[str]]:
        """
        Validate request data

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate name
        if not self.name or len(self.name.strip()) == 0:
            return False, "Name is required"

        # Validate guest_count
        try:
            count = int(self.guest_count)
            if count < 1:
                return False, "Guest count must be at least 1"
            if count > 20:
                return False, "Guest count cannot exceed 20"
        except (ValueError, TypeError):
            return False, "Guest count must be a valid number"

        # Validate confirmation_status
        if self.confirmation_status not in self.VALID_STATUSES:
            return False, f"Invalid confirmation_status. Must be one of: {', '.join(self.VALID_STATUSES)}"

        return True, None


@dataclass
class GuestResponse:
    """Schema for guest response"""
    id: int
    name: str
    guest_count: int
    confirmation_status: str
    comment: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_guest(cls, guest) -> "GuestResponse":
        """Create response from Guest model"""
        return cls(
            id=guest.id,
            name=guest.name,
            guest_count=guest.guest_count,
            confirmation_status=guest.confirmation_status,
            comment=guest.comment,
            created_at=guest.created_at.isoformat() if guest.created_at else None
        )

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "guest_count": self.guest_count,
            "confirmation_status": self.confirmation_status,
            "comment": self.comment,
            "created_at": self.created_at
        }


@dataclass
class ErrorResponse:
    """Schema for error response"""
    code: str
    message: str

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "code": self.code,
            "message": self.message
        }
