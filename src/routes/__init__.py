from .user import router as user_router
from .persons import router as persons_router
from .inventory import router as inventory_router

__all__ = ["user_router", "persons_router", "inventory_router"]