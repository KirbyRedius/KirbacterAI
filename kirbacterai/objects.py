class Chat:
    def __init__(self, client, character_id, data):
        self.client = client
        self.title = data["title"] if "title" in data else None
        self.participants = [Participant(value) for value in data["participants"]] if "participants" in data else None
        self.external_id = data["external_id"] if "external_id" in data else None
        self.character_id = character_id
        self.created = data["created"] if "created" in data else None
        self.last_interaction = data["last_interaction"] if "last_interaction" in data else None
        self.type = data["type"] if "type" in data else None
        self.description = data["description"] if "description" in data else None
        self.speech = data["speech"] if "speech" in data else None
        self.status = data["status"] if "status" in data else None
        self.has_more = data["has_more"] if "has_more" in data else None
        self.messages = [Message(value) for value in data["messages"]] if "messages" in data else None

    async def send_message(self, text):
        return await self.client.send_message(self, text)

class Participant:
    def __init__(self, data):
        self.user = User(data["user"]) if "user" in data else None
        self.is_human = data["is_human"] if "is_human" in data else None
        self.name = data["name"] if "name" in data else None
        self.num_interactions = data["num_interactions"] if "num_interactions" in data else None
        self.username = data["username"] if "username" in data else None


class User:
    def __init__(self, data):
        self.username = data["username"] if "username" in data else None
        self.id = data["id"] if "id" in data else None
        self.first_name = data["first_name"] if "first_name" in data else None
        self.account = data["account"] if "account" in data else None
        self.is_staff = data["is_staff"] if "is_staff" in data else None
        self.subscription = data["subscription"] if "subscription" in data else None
        self.is_human = data["is_human"] if "is_human" in data else None
        self.name = data["name"] if "name" in data else None
        self.email = data["email"] if "email" in data else None
        self.hidden_characters = [Character(value) for value in data["hidden_characters"]] if "hidden_characters" in data else None
        self.blocked_users = [User(value) for value in data["blocked_users"]] if "blocked_users" in data else None
        self.user = User(data["user"]) if "user" in data else None


class Account:
    def __init__(self, data):
        self.name = data["name"] if "name" in data else None
        self.avatar_type = data["avatar_type"] if "avatar_type" in data else None
        self.onboarding_complete = data["onboarding_complete"] if "onboarding_complete" in data else None
        self.avatar_file_name = data["avatar_file_name"] if "avatar_file_name" in data else None
        self.mobile_onboarding_complete = data["mobile_onboarding_complete"] if "mobile_onboarding_complete" in data else None


class Message:
    def __init__(self, data):
        self.deleted = data["deleted"] if "deleted" in data else None
        self.id = data["id "] if "id " in data else None
        self.image_prompt_text = data["image_prompt_text"] if "image_prompt_text" in data else None
        self.image_rel_path = data["image_rel_path"] if "image_rel_path" in data else None
        self.is_alternative = data["is_alternative"] if "is_alternative" in data else None
        self.responsible_user__username = data["responsible_user__username"] if "responsible_user__username" in data else None
        self.src__character__avatar_file_name = data["src__character__avatar_file_name"] if "src__character__avatar_file_name" in data else None
        self.src__is_human = data["src__is_human"] if "src__is_human" in data else None
        self.src__name = data["src__name"] if "src__name" in data else None
        self.src__user__username = data["src__user__username"] if "src__user__username" in data else None
        self.src_char = Src_char(data["src_char"]) if "src_char" in data else None
        self.text = data["text"] if "text" in data else None
        self.uuid = data["uuid"] if "uuid" in data else None


class Src_char:
    def __init__(self, data):
        self.avatar_file_name = data["avatar_file_name"] if "avatar_file_name" in data else None
        self.participant = Participant(data["participant"]) if "participant" in data else None


class MessageResponse:
    def __init__(self, data):
        self.replies = [Message(value) for value in data["replies"]] if "replies" in data else None
        self.src_char = Src_char(data["src_char"]) if "src_char" in data else None
        self.is_final_chunk = data["is_final_chunk"] if "is_final_chunk" in data else None
        self.last_user_msg_id = data["last_user_msg_id"] if "last_user_msg_id" in data else None
        self.last_user_msg_uuid = data["last_user_msg_uuid"] if "last_user_msg_uuid" in data else None


class Character:
    def __init__(self, data, client=None):
        self.client = client
        self.external_id = data["external_id"] if "external_id" in data else None
        self.character_id = self.external_id
        self.title = data["title"] if "title" in data else None
        self.greeting = data["greeting"] if "greeting" in data else None
        self.description = data["description"] if "description" in data else None
        self.avatar_file_name = data["avatar_file_name"] if "avatar_file_name" in data else None
        self.visibility = data["visibility"] if "visibility" in data else None
        self.copyable = data["copyable"] if "copyable" in data else None
        self.participant__name = data["participant__name"] if "participant__name" in data else None
        self.participant__num_interactions = data["participant__num_interactions"] if "participant__num_interactions" in data else None
        self.user__id = data["user__id"] if "user__id" in data else None
        self.user__username = data["user__username"] if "user__username" in data else None
        self.img_gen_enabled = data["img_gen_enabled"] if "img_gen_enabled" in data else None
        self.priority = data["priority"] if "priority" in data else None
        self.trending_score = data["trending_score"] if "trending_score" in data else None
        self.identifier = data["identifier"] if "identifier" in data else None
        self.name = data["name"] if "name" in data else None
        self.categories = [Category(raw) for raw in data["categories"]] if "categories" in data else None
        self.definition = data["definition"] if "definition" in data else None
        self.avatar_rel_path = data["avatar_rel_path"] if "avatar_rel_path" in data else None
        self.base_img_prompt = data["base_img_prompt"] if "base_img_prompt" in data else None
        self.strip_img_prompt_from_msg = data["strip_img_prompt_from_msg"] if "strip_img_prompt_from_msg" in data else None
        self.voice_id = data["voice_id"] if "voice_id" in data else None

    async def update(self, **args):
        updated_character = await self.client.create_or_update_character(**args, update=True, character=self)
        self.__dict__.update(updated_character.__dict__)

    async def chat_create(self, **args):
        return await self.client.chat_create(self.character_id)


class Category:
    def __init__(self, data):
        self.name = data["name"] if "name" in data else None
        self.description = data["description"] if "description" in data else None


class Voice:
    def __init__(self, data):
        self.id = data["id"] if "id" in data else None
        self.name = data["name"] if "name" in data else None
        self.voice_id = data["voice_id"] if "voice_id" in data else None
        self.country_code = data["country_code"] if "country_code" in data else None
        self.lang_code = data["lang_code"] if "lang_code" in data else None
