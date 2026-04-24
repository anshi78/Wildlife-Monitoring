import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Missing keys!")
    exit(1)

print(f"Connecting to Supabase at {SUPABASE_URL}...")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Creating dummy file...")
with open("dummy.txt", "w") as f:
    f.write("Hello World Wildlife!")

print("Attempting to upload to 'wildlife-images' bucket...")
try:
    with open("dummy.txt", "rb") as f:
        res = supabase.storage.from_("wildlife-images").upload("dummy.txt", f.read(), {"content-type": "text/plain"})
    print(f"Upload successful: {res}")
    
    url = supabase.storage.from_("wildlife-images").get_public_url("dummy.txt")
    print(f"Public URL: {url}")
except Exception as e:
    print(f"ERROR: {e}")
finally:
    if os.path.exists("dummy.txt"):
        os.remove("dummy.txt")
