import os
from supabase import create_client, Client

url: str = "https://cwxkwruekonjpjqvpvyr.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN3eGt3cnVla29uanBqcXZwdnlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM4NDMxODgsImV4cCI6MjAxOTQxOTE4OH0.fBWSlCajKKgQ3OrEr9M_hG_wFqzU6_Ajd7C_0NBrCG4"
supabase: Client = create_client(url, key)


# data, count = supabase.table('chats').insert({"chat_id": 1}).execute()
# print(data,count)

data,count = supabase.table('chats').select('chat_id').eq('chat_id', '123').execute()
print(data[1])