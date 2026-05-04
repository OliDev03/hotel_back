from supabase import create_async_client, AsyncClient
import os
from dotenv import load_dotenv
from typing import cast

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the environment or .env file.")

SUPABASE_URL = cast(str, SUPABASE_URL)
SUPABASE_KEY = cast(str, SUPABASE_KEY)

async def get_supabase_client() -> AsyncClient:
    
    return await create_async_client(SUPABASE_URL, SUPABASE_KEY)