import asyncio
import json
import pyppeteer
import objects
from uuid import uuid4
from pyppeteer_stealth import stealth
from helpers import js_simple_request

puppeteerLaunchArgs = [
	'--fast-start',
	'--disable-extensions',
	'--no-sandbox',
	'--disable-setuid-sandbox',
	'--no-gpu',
	'--disable-background-timer-throttling',
	'--disable-renderer-backgrounding',
	'--override-plugin-power-saver-for-testing=never',
	'--disable-extensions-http-throttling',
	'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0'
]


class Client:
	def __init__(self):
		self.headers = {
			"content-type": "application/json",
			"user-agent": 'CharacterAI/1.0.1 (iPhone; iOS 12.1.6; Scale/3.00)'
		}
		self.token = ""
		self.page = None
		self._change_payload = None
		self._change_headers = None
		self._go_url = None
		self._method = None
		self._force_change = False
		self.is_started = False

	async def start(self):
		browser = await pyppeteer.launch({
			"headless": "new",
			"args": puppeteerLaunchArgs,
			"protocolTimeout": 0,
			"executablePath": None
		})
		pages = await browser.pages()
		self.page = pages[0]
		await stealth(self.page)

		await self.page.deleteCookie()

		client = await self.page.target.createCDPSession()
		await client.send('Network.clearBrowserCookies')
		await client.send('Network.clearBrowserCache')

		await self.page.setViewport({
			"width": 1920,
			"height": 1080,
			"deviceScaleFactor": 1,
			"hasTouch": False,
			"isLandscape": True,
			"isMobile": False,
		})
		await self.page.setJavaScriptEnabled(True)
		await self.page.setCacheEnabled(True)
		await self.page.goto("https://beta.character.ai")
		await self.page.waitFor(2000)

	async def send_request(self, method, url, data: dict = None):
		self._method = method
		self._go_url = url
		if data is not None:
			data = json.dumps(data)
			self._change_payload = data
		self._force_change = True
		self.page.once('request', lambda req: asyncio.ensure_future(self.modify_request(req)))
		await self.page.setRequestInterception(True)
		response = await self.page.goto(url, {"waitUntil": 'networkidle2'})
		return await response.json()

	async def modify_request(self, request):
		if self._go_url == request.url and self._force_change:
			data = {}

			if self._change_headers is not None:
				data["headers"] = self._change_headers
			else:
				data["headers"] = self.headers

			data["method"] = self._method
			if self._change_payload is not None:
				data["postData"] = self._change_payload
			self._force_change = False
			self._change_payload = None
			self._change_headers = None
			return await request.continue_(data)
		return await request.continue_()

	async def request_by_eval(self, url, data):
		await self.page.setRequestInterception(False)
		code = js_simple_request
		code = code.replace("MY_METHOD", "POST")
		code = code.replace("MY_HEADERS", str(self.headers))
		data = str(data).replace("None", "null").replace("True", "true").replace("False", "false").replace('"', "")
		code = code.replace("MY_BODY", data)
		code = code.replace("MY_URL", url)
		response = json.loads(await self.page.evaluate(code))
		return response

	async def auth_as_guest(self):
		if not self.is_started:
			await self.start()
		uuid = str(uuid4())
		data = {"lazy_uuid": uuid}
		response = await self.send_request("POST", "https://beta.character.ai/chat/auth/lazy/", data=data)
		self.token = response['token']
		self.headers['authorization'] = f"Token {self.token}"
		return response

	async def auth_with_token(self, token):
		if not self.is_started:
			await self.start()
		data = {'access_token': token}
		response = await self.send_request("POST", "https://beta.character.ai/dj-rest-auth/auth0/", data=data)
		self.token = response['key']
		self.headers['authorization'] = f"Token {self.token}"
		return response

	async def chat_create(self, character_id):
		data = {
			"character_external_id": character_id
		}
		response = await self.send_request("POST", "https://beta.character.ai/chat/history/create/", data=data)
		return objects.Chat(self, character_id, response)

	async def chat_continue(self, character_id, history_id: str = None):
		data = {
			"character_external_id": character_id,
			"history_external_id": history_id
		}
		response = await self.send_request("POST", "https://beta.character.ai/chat/history/continue/", data=data)
		return response

	async def send_message(self, chat, text):
		tgt = None
		for participant in chat.participants:
			if not participant.is_human:
				tgt = participant.user.username
				break
		data = {
			"history_external_id": chat.external_id,
			"character_external_id": chat.character_id,
			"text": text,
			"tgt": tgt,
			"ranking_method": "random",
			"staging": False,
			"model_server_address": None,
			"model_server_address_exp_chars": None,
			"override_prefix": None,
			"override_rank": None,
			"rank_candidates": None,
			"filter_candidates": None,
			"unsanitized_characters": None,
			"prefix_limit": None,
			"prefix_token_limit": None,
			"stream_params": None,
			"model_properties_version_keys": "",
			"enable_tti": None,
			"initial_timeout": None,
			"insert_beginning": None,
			"stream_every_n_steps": 16,
			"is_proactive": False,
			"image_rel_path": "",
			"image_description": "",
			"image_description_type": "",
			"image_origin_type": "",
			"voice_enabled": False,
			"parent_msg_uuid": None,
			"seen_msg_uuids": [],
			"retry_last_user_msg_uuid": None,
			"num_candidates": 1,
			"give_room_introductions": True,
			"mock_response": False
		}
		response = await self.request_by_eval("https://beta.character.ai/chat/streaming/", data)
		return objects.MessageResponse(response).replies[0].text

	async def get_featured_characters(self):
		response = await self.send_request("GET", "https://beta.character.ai/chat/characters/featured_v2/")
		characters = [objects.Character(character, client=self) for character in response["characters"]]
		return characters

	async def get_trending_characters(self):
		response = await self.send_request("GET", "https://beta.character.ai/chat/characters/trending/")
		characters = [objects.Character(character, client=self) for character in response["trending_characters"]]
		return characters

	async def get_my_user_info(self):
		response = await self.send_request("GET", "https://beta.character.ai/chat/user/")
		return objects.User(response["user"])

	async def get_characters_categories(self):
		response = await self.send_request("GET", "https://beta.character.ai/chat/character/categories/")
		categories = [objects.Category(category) for category in response["categories"]]
		return categories

	async def get_characters_voices(self):
		response = await self.send_request("GET", "https://beta.character.ai/chat/character/voices/")
		categories = [objects.Voice(voice) for voice in response["voices"]]
		return categories

	async def search_characters(self, text):
		response = await self.send_request("GET", f"https://beta.character.ai/chat/characters/search/?query={text}")
		characters = [objects.Character(character, client=self) for character in response["characters"]]
		return characters

	async def create_or_update_character(self, name: str = None, title: str = None, greeting: str = "", description: str = "",
										definition: str = "", voice_id: int = 38, visibility: str = "PUBLIC",
										categories=[], character=None, update: bool = False):
		"""
		Args:
			definition: An example of chatting with a bot like this one
				{{char}}: Hi {{user}}, I'm {{char}}.
				{{user}}: Hello {{char}}!
			categories: list with categories name like ["Acrion", "Books"]
		"""

		data = {
			"voice_id": voice_id if voice_id is not None else character.voice_id if character is not None else None,
			"strip_img_prompt_from_msg": False,  # TODO
			"visibility": visibility if visibility is not None else character.visibility if character is not None else None,
			"greeting": greeting if greeting is not None else character.greeting if character is not None else None,
			"name": name if name is not None else character.name if character is not None else None,
			"description": description if description is not None else character.description if character is not None else None,
			"definition": definition if definition is not None else character.definition if character is not None else None,
			"img_gen_enabled": False,  # TODO
			"copyable": False,
			"base_img_prompt": "",  # TODO
			"title": title if title is not None else character.title if character is not None else None,
			"avatar_rel_path": ""  # TODO
		}

		data["categories"] = []
		for category in categories:
			if isinstance(category, objects.Category):
				data["categories"].append(category.name)
			else:
				data["categories"].append(category)

		if update:
			data["external_id"] = character.external_id
			response = await self.send_request("POST", "https://beta.character.ai/chat/character/update/", data=data)
		else:
			uuid = str(uuid4())
			data["identifier"] = f"id:{uuid}"
			response = await self.send_request("POST", "https://beta.character.ai/chat/character/create/", data=data)
			character = objects.Character(response["character"])

			data = {"external_id": character.external_id}
			await self.send_request("POST", "https://beta.character.ai/chat/character/info/", data=data)

		return objects.Character(response["character"], client=self)
