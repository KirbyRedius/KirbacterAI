import asyncio
from kirbacterai import Client

token = "token"


async def main():
	client = Client()
	await client.auth_with_token(token)

	definition = """
	{{char}}: Hi {{user}}, I'm {{char}}.
	{{user}}: Hello!
	"""

	character = await client.create_or_update_character(
		name="Bob",
		title="It's me, Bob!",
		greeting="Hello!",
		description="Just Bob",
		definition=definition,
		voice_id=38,
		visibility="PUBLIC",
		categories=["Books"]
	)
	print(character.name, "created!")

	# What if we want update only name and description?
	await character.update(
		name="Cool Bob",
		description="Just Cool Bob",
	)
	print(character.name, "updated!")

	# Now we want send message to our bot
	print(f"Creating chat with {character.name}")
	chat = await character.chat_create()

	print(f"Sending message to {character.name}")
	text = "Hello"
	reply = await chat.send_message(text)
	print(f"Got message from bot: {reply}")


asyncio.get_event_loop().run_until_complete(main())
