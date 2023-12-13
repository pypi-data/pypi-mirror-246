import json
import uuid
import hashlib
import tiktoken


_TOKEN_ENC: dict = {
    "gpt-3.5-turbo": tiktoken.encoding_for_model("gpt-3.5-turbo"),
    "gpt-4": tiktoken.encoding_for_model("gpt-4"),
}


def get_tiktoken_model(model: str):
    global _TOKEN_ENC
    encoding = _TOKEN_ENC.get(model)

    if encoding is None:
        try:
            _TOKEN_ENC[model] = encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            _TOKEN_ENC[model] = encoding = tiktoken.get_encoding("cl100k_base")
    else:
        if model.startswith("gpt-3.5"):
            # Default to the gpt-3.5-turbo encoding for gpt-3.5 models.
            _TOKEN_ENC[model] = encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        elif model.startswith("gpt-4"):
            # Default to the gpt-4 encoding for gpt-4 models.
            _TOKEN_ENC[model] = encoding = tiktoken.encoding_for_model("gpt-4")
        else:
            raise ValueError(f"Unknown model {model}")

    return encoding


def num_tokens_from_messages(messages: list[dict], model: str = "gpt-3.5-turbo-0301") -> int:
    """Returns the number of tokens used by a list of messages."""
    # https://platform.openai.com/docs/guides/chat/introduction

    encoding = get_tiktoken_model(model)

    if model in ["gpt-3.5-turbo-0301", "gpt-3.5-turbo", "gpt-4"]:  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")


def build_prompt_id(user_template: str = None, system_content: str = None, api_kwargs: dict = None) -> str:
    # Create a unique ID for this combination of prompt, API arguments.
    k_dict = {}

    if api_kwargs is not None:
        k_dict = {**api_kwargs}

    # Remove max_tokens from the key, since it could vary
    # depending on the length of the prompt.
    if "max_tokens" in k_dict:
        del k_dict["max_tokens"]

    k_dict["system_content"] = system_content
    k_dict["user_template"] = user_template

    jkey = json.dumps(k_dict, sort_keys=True)

    return f"{uuid.UUID(hashlib.md5(jkey.encode('utf-8')).hexdigest())}"


def get_message_hash(message: list[dict]) -> str:
    """Returns a hash of the message."""
    # https://platform.openai.com/docs/guides/chat/introduction
    #
    # The message is a list of dictionary objects, where each dictionary
    # represents a message from a user or the system.

    # The hash is calculated by converting the message to a JSON string,
    # sorting the keys, and then hashing the JSON string.
    jkey: str = json.dumps(message, sort_keys=True)

    return hashlib.md5(jkey.encode('utf-8')).hexdigest()
