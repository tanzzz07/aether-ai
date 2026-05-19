from functools import lru_cache

from backend.config import get_settings
from supabase import Client, create_client

@lru_cache
def get_supabase_admin() -> Client | None:
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        return None
    return create_client(str(settings.supabase_url), settings.supabase_service_role_key)