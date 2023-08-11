import asyncio
from cai import CaiClient

token = "YourToken"

async def main():
	client = CaiClient()

	await client.start()

	await client.auth_with_token(token)

	character = await client.create_or_update_character(
		name="Test Kirby",
		title="hello!",
		greeting="ff",
		description="ff",
		definition="ff",
		voice_id=38,
		visibility="PUBLIC",
		categories=[]
	)
	print(character.name, "created!")

	character = await character.update(
		name="LMAO",
		title="hello!",
		greeting="ff",
		description="ff",
		definition="ff",
		voice_id=38,
		visibility="PUBLIC",
		categories=[]
	)
	print(character.name, "updated!")


asyncio.get_event_loop().run_until_complete(main())
