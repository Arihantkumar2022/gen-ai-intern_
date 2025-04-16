from .admin import router as admin_router
from .candidate import router as candidate_router
from .interviews import router as interviews_router

__all__ = ["admin_router", "candidate_router", "interviews_router"]