import copy
import openai
from openai import error
import math
import time
from openai.error import RateLimitError
import tiktoken
import time
from typing import Generator, Union
from logutils import get_logger
from chatgpt_klient.consts import MAX_DELAY, ENGINES, DEFAULT_ENGINES
from chatgpt_klient.exceptions import (
    InvalidAPIKeyError,
    InvalidModelError,
    InvalidResponseError,
)
from rich.console import Console

logger = get_logger("chatgpt_client")
console = Console()


class ChatGPTPrompt:
    def __init__(self, api_key, engine="gpt3.5-default", cap_tokens=math.inf):
        self.api_key = api_key
        self.openai = openai
        self.openai.api_key = self.api_key
        self.check_api_key_validity()
        self.msg_history = {"messages": [], "tokens": []}
        self.last_prompt_tokens = 0
        self.cap_tokens = cap_tokens
        self.set_engine(engine)

    def list_models(self):
        return list(ENGINES.keys()) + list(DEFAULT_ENGINES.keys())

    def check_api_key_validity(self):
        try:
            r = self.openai.Completion.create(
                model="davinci",
                prompt="Hi",
                max_tokens=5,
            )
            r = self.check_response_validity(r)
        except error.ServiceUnavailableError as e:
            logger.exception("OpenAI service seems to be down")
            raise e
        except Exception:
            logger.exception("Invalid API key.")
            raise InvalidAPIKeyError(
                "Your API key does not seem to be valid. Please check it."
            )
        else:
            logger.info("API key seems valid and working.")

    def check_model_validity(self):
        if self.engine not in self.list_models():
            logger.error(f"Engine {self.engine} is not supported")
            raise InvalidModelError(f"Engine {self.engine} not supported")
        try:
            if self.engine in [k for k, v in ENGINES.items() if v["type"] == "legacy"]:
                r = self.openai.Completion.create(
                    model=self.engine,
                    prompt="Hi",
                    max_tokens=5,
                )
                r = self.check_response_validity(r)
            elif self.engine in [k for k, v in ENGINES.items() if v["type"] == "chat"]:
                r = self.openai.ChatCompletion.create(
                    model=self.engine,
                    messages=[{"role": "user", "content": "Hi"}],
                    max_tokens=5,
                )
                r = self.check_response_validity(r)
                logger.debug(
                    f'Model validity test: {r["choices"][0]["message"]["content"]}'
                )
            else:
                raise InvalidModelError(f"Engine {self.engine} not supported")
        except error.ServiceUnavailableError as e:
            logger.exception("OpenAI service seems to be down")
            raise e
        except Exception:
            logger.info(f"Invalid model ({self.engine}) for your API key")
            raise InvalidModelError(f"Engine {self.engine} not supported")
        else:
            logger.info(f"Model ({self.engine}) seems to be valid.")

    def check_response_validity(self, r) -> dict:
        try:
            match r:
                case {"choices": [{"text": str()}]}:
                    pass
                case {"choices": [{"message": {"content": str()}}]}:
                    pass
                case _:
                    raise InvalidModelError
        except Exception:
            raise InvalidResponseError(f"Response is not well formed: {r}")
        else:
            logger.debug("Response seems to be well formed")
            return r

    def set_engine(self, engine: str):
        if engine in DEFAULT_ENGINES.keys():
            self.engine = DEFAULT_ENGINES[engine]
        else:
            self.engine = engine
        self.check_model_validity()
        self.encoding = tiktoken.encoding_for_model(self.engine)
        eng_attrs = ENGINES[self.engine]
        if "max_output_tokens" in eng_attrs:
            self.max_tokens = eng_attrs["max_tokens"] - eng_attrs["max_output_tokens"]
        else:
            self.max_tokens = int(eng_attrs["max_tokens"] / 2)

    def set_system_directive(self, directive: str):
        self.clean_history(keep_sysdir=False)
        self.msg_history["messages"].append(
            {
                "role": "system",
                "content": directive,
            }
        )
        self.msg_history["tokens"].append(len(self.encoding.encode(directive)))

    def clean_history(self, keep_sysdir=True):
        new_history = {"messages": [], "tokens": []}
        if keep_sysdir:
            for i, m in enumerate(self.msg_history["messages"]):
                if m["role"] == "system":
                    new_history["messages"].append(
                        {"role": m["role"], "content": m["content"]}
                    )
                    new_history["tokens"].append(self.msg_history["tokens"][i])
            self.msg_history = new_history
        self.last_prompt_tokens = 0

    def get_max_tokens_allowed(self):
        return (
            min([self.max_tokens, ENGINES[self.engine]["max_tokens"], self.cap_tokens])
            - 10
        )

    def get_max_output_tokens_allowed(self):
        aux = math.inf
        if "max_output_tokens" in ENGINES[self.engine]:
            aux = ENGINES[self.engine]["max_output_tokens"]
        return min(self.get_max_tokens_allowed(), aux)

    def calculate_prompt_tokens(self, text, no_history=True, keep_sysdir=False):
        aux_history = copy.deepcopy(self.msg_history)
        aux_last_prompt = self.last_prompt_tokens
        if no_history:
            self.clean_history(keep_sysdir=keep_sysdir)
        self.msg_history["messages"].append(
            {
                "role": "user",
                "content": text,
            }
        )
        self.msg_history["tokens"].append(len(self.encoding.encode(text)))
        potential_tokens = self.msg_history["tokens"][-1] + self.last_prompt_tokens
        if no_history:
            self.msg_history = aux_history
            self.last_prompt_tokens = aux_last_prompt
        return potential_tokens

    def send_prompt(
        self, text: str, no_history: bool = False, stream: bool = False
    ) -> Union[str, Generator[str, None, None]]:
        """
        Send a prompt to ChatGPT with some text to get a response.

        :param text: the text to be sent as a prompt. This will be appended as the
          latest "user" message of the conversation
        :param no_history: deactivate the use of a previous history of messages. If
          set to True, all previous messages will be cleared and only the one in
          *text* will be used
        :param stream: set to True to return the generated tokens synchronously, one
          by one as we receive them from ChatGPT. Otherwise, the text will be returned
          as a whole once it is ready.
        :returns: either a string with the whole text, or a generator of the tokens
          composing the text
        """
        response = "No response"
        if self.engine in [k for k, v in ENGINES.items() if v["type"] == "legacy"]:
            r = self.openai.Completion.create(
                engine=self.engine,
                prompt=text,
                max_tokens=self.get_max_output_tokens_allowed(),
            )
            r = self.check_response_validity(r)
            response = r["choices"][0]["text"]
        elif self.engine in [k for k, v in ENGINES.items() if v["type"] == "chat"]:
            if no_history:
                self.clean_history()
            self.msg_history["messages"].append(
                {
                    "role": "user",
                    "content": text,
                }
            )
            self.msg_history["tokens"].append(len(self.encoding.encode(text)))
            self.reduce_msg_history(text)
            if stream:
                return self.chat_completion_stream(text)
            else:
                return self.chat_completion_no_stream(text)
        else:
            logger.warning(f"Engine {self.engine} not supported")
        return response

    def interactive_prompt(self, system_directive: str | None = None, max_tokens=None):
        if system_directive:
            self.set_system_directive(system_directive)
        console.print("###########", style="bold")
        console.print("# ChatGPT #", style="bold")
        console.print("###########", style="bold")
        console.print(
            f"[bold yellow]Engine:[/bold yellow] {self.engine}", highlight=False
        )
        console.print("[bold cyan]Enter 'q'/'quit' to exit the chat[/]")
        console.print("[bold cyan]Enter anything to start chatting.[/]")
        console.print()
        while True:
            input_text = input("$ ")
            if input_text in ("q", "quit"):
                print("ChatGPT> Sayonara, baby!")
                break
            try:
                r = self.send_prompt(text=input_text)
            except RateLimitError:
                logger.warning("You are sending requests too fast. Delaying 20s...")
                time.sleep(20)
                r = self.send_prompt(text=input_text)

            console.print(f"[bold green]ChatGPT>[/] [green]{r}[/]")
            self.msg_history["messages"].append(
                {
                    "role": "assistant",
                    "content": r,
                }
            )
            self.msg_history["tokens"].append(len(self.encoding.encode(r)))

    def reduce_msg_history(self, text: str):
        potential_tokens = self.msg_history["tokens"][-1] + self.last_prompt_tokens
        logger.debug(f"Potential tokens: {potential_tokens}")
        while potential_tokens > self.get_max_tokens_allowed():
            logger.warning("Too many tokens. Reducing history size")
            aux = {"messages": [], "tokens": []}
            first_user = True
            first_assistant = True
            for i in range(len(self.msg_history["messages"])):
                if self.msg_history["messages"][i]["role"] == "user" and first_user:
                    first_user = False
                    potential_tokens -= self.msg_history["tokens"][i]
                elif (
                    self.msg_history["messages"][i]["role"] == "assistant"
                    and first_assistant
                ):
                    first_assistant = False
                    potential_tokens -= self.msg_history["tokens"][i]
                else:
                    aux["messages"].append(self.msg_history["messages"][i])
                    aux["tokens"].append(self.msg_history["tokens"][i])
            self.msg_history = aux
        if text not in [m["content"] for m in self.msg_history["messages"]]:
            raise TooManyTokensError(
                f"The maximum accepted tokens ({self.get_max_tokens_allowed()}) is not big enough to process your prompt"
            )

    def chat_completion_no_stream(self, text: str, delay: int = 5) -> str:
        try:
            r = self.openai.ChatCompletion.create(
                model=self.engine,
                messages=self.msg_history["messages"],
                max_tokens=self.get_max_output_tokens_allowed(),
                request_timeout=300,
                stream=False,
            )
            logger.debug(r)
            r = self.check_response_validity(r)
            self.last_prompt_tokens = r["usage"]["total_tokens"]
            response = r["choices"][0].message.content
            if response:
                self.msg_history["messages"].append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )
                self.msg_history["tokens"].append(len(self.encoding.encode(response)))
        except RateLimitError:
            logger.warning(f"Rate limit reached, delaying request {delay} seconds")
            if delay > MAX_DELAY:
                raise Exception(
                    "Recurring RateLimitError and delaying requests not working"
                )
            time.sleep(delay)
            return self.chat_completion_no_stream(text, delay=delay * 2)
        except openai.InvalidRequestError as e:
            if "maximum context length" in str(e):
                self.clean_history(keep_sysdir=True)
                return self.chat_completion_no_stream(text, delay=delay * 2)
            else:
                logger.warning("We shouldn't be getting here!")
                raise e
        except error.Timeout:
            logger.warning("Request failed with timeout, retrying")
            if delay > MAX_DELAY:
                raise Exception("Getting timeouts to all requests")
            time.sleep(delay)
            return self.chat_completion_no_stream(text, delay=delay * 2)
        else:
            return response

    def chat_completion_stream(
        self, text: str, delay: int = 5
    ) -> Generator[str, None, None]:
        try:
            stream = self.openai.ChatCompletion.create(
                model=self.engine,
                messages=self.msg_history["messages"],
                max_tokens=self.get_max_output_tokens_allowed(),
                request_timeout=300,
                stream=True,
            )
            aux_num_tokens = 0
            aux_text = ""
            for r in stream:
                match chunk := r["choices"][0]:
                    case {"finish_reason": "stop"}:
                        break
                    case {"delta": {"content": token}}:
                        logger.debug(f"Received chunk: {token}")
                        aux_text += token
                        aux_num_tokens += 1
                        yield token
                    case _:
                        logger.warning(f"Strange object structure: {chunk}")
            self.last_prompt_tokens = aux_num_tokens
            self.msg_history["messages"].append(
                {
                    "role": "assistant",
                    "content": aux_text,
                }
            )
            self.msg_history["tokens"].append(len(self.encoding.encode(aux_text)))
        except RateLimitError:
            logger.warning(f"Rate limit reached, delaying request {delay} seconds")
            if delay > MAX_DELAY:
                raise Exception(
                    "Recurring RateLimitError and delaying requests not working"
                )
            time.sleep(delay)
            self.chat_completion_stream(text, delay=delay * 2)
        except openai.InvalidRequestError as e:
            if "maximum context length" in str(e):
                self.clean_history(keep_sysdir=True)
                self.chat_completion_stream(text, delay=delay * 2)
            else:
                logger.warning("We shouldn't be getting here!")
                raise e
        except error.Timeout:
            logger.warning("Request failed with timeout, retrying")
            if delay > MAX_DELAY:
                raise Exception("Getting timeouts to all requests")
            time.sleep(delay)
            self.chat_completion_stream(text, delay=delay * 2)


class TooManyTokensError(Exception):
    pass
