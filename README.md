[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Python+wrapper+for+beta.character.ai)](https://github.com/KirbyRedius/KirbacterAI)
>This is the unofficial API
--- 
<br><br/>
## Installation
```bash
  pip install kirbacterai
```
<br><br>

## Code example
```python
import asyncio
from kirbacterai import Client

async def main():

    client = Client()

    await client.auth_as_guest()
    # You can use client.auth_with_token(token) instead

    link = "https://c.ai/c/0FGHpcylr6O0l46xHrTMzRGnqAU6beVz0k3i294wbUQ"

    character = await client.get_character_from_link(link)

    chat = await character.chat_create()

    character_reply = await chat.send_message("Hello!")

    print(character_reply)


asyncio.get_event_loop().run_until_complete(main())

```
---
<br><br>

## Using an Access Token
**<p dir="auto"> :heavy_exclamation_mark: Some parts of the API, like managing a conversation requires for you to be logged in using an <code>accessToken</code>.
To get it, you can open your browser, go to the <a href="https://character.ai" rel="nofollow">character.ai website</a> in <code>localStorage</code>.</p>**

<ins dir="auto"> — To do so:</ins>               

❒ Open the Character AI website in your browser
<br><br/>
❒ Open the developer tools <code>F12</code> and go to the <code>Application</code> tab.
<br><br/>
❒ Go to the <code>Storage</code> section and click on <code>Local Storage</code>.
<br><br/>
❒ Look for the `@@auth0spajs@@::dyD3gE281MqgISG7FuIXYhL2WEknqZzv::https://auth0.character.ai/::openid profile email offline_access` key.
<br><br/>
❒ Open the body and copy the access token.
<br><br/>
![image](https://github.com/KirbyRedius/CharacterAI/assets/142050294/89a804e1-1d51-4caa-a01e-6824c08912ef)

---

<div id="header" align="center">
  <img src="https://media.tenor.com/oBAv0Q0H8O4AAAAi/scratch-cat.gif" width="250"/>
</div>

<br><br>

## Node.js version
---

Most of the stuff was taken from another _JavaScript_ repository:

- [Character AI Unofficial Node API](https://github.com/realcoloride/node_characterai)

--- 
