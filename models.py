import re
import unicodedata
from dataclasses import dataclass
import unidecode
from messages import StandaloneCard, CarouselCard


@dataclass
class MensajeRCS:
    id: str
    name: str
    filename: str
    title_rcs_msg: str
    rcs_msg: str
    fallback_msg: str
    button1_text: str | None
    button1_url: str | None
    button2_text: str | None
    button2_url: str | None
    postback_data_button1: str | None
    postback_data_button2: str | None
    rendered_json: str
    urls: list[str] | None

    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.name = kwargs["name"]
        self.filename = kwargs["filename"]
        self.title_rcs_msg = kwargs["title_rcs_msg"]
        self.rcs_msg = kwargs["rcs_msg"]
        self.fallback_msg = kwargs["fallback_msg"]
        self.button1_text = kwargs["button1_text"]
        self.button1_url = kwargs["button1_url"]
        self.button2_text = kwargs["button2_text"]
        self.button2_url = kwargs["button2_url"]
        self.fix_data()

    def fix_data(self):
        self.remove_zero_width_chars()

        self.name = unicodedata.normalize("NFKD", self.name)
        self.name = self.name.strip().replace("\n", " ")

        self.fallback_msg = unicodedata.normalize("NFKD", self.fallback_msg)
        self.fallback_msg = self.fallback_msg.replace("\n", " ")

        self.title_rcs_msg = unicodedata.normalize("NFKD", self.title_rcs_msg)
        self.title_rcs_msg = self.title_rcs_msg.replace("\n", " ")

        self.rcs_msg = unicodedata.normalize("NFKD", self.rcs_msg)
        self.rcs_msg = self.rcs_msg.replace("\n", " ")

        self.filename = unidecode.unidecode(self.filename).strip().replace(" ", "_")

        if self.button1_text is not None and self.button1_text != "":
            self.button1_text = unicodedata.normalize("NFKD", self.button1_text)
            self.button1_text = self.button1_text.replace("\n", " ")

            self.postback_data_button1 = unidecode.unidecode(self.button1_text).title()
            self.postback_data_button1 = remove_special_characters(self.postback_data_button1)
            self.postback_data_button1 = f"Button1_{self.postback_data_button1}"

            if "http" not in self.button1_url and self.button1_url != "":
                self.button1_url = f"https://{self.button1_url}".replace(" ", "")
            else:
                self.button1_url = self.button1_url.replace(" ", "")

        if self.button2_text is not None and self.button2_text != "":
            self.button2_text = unicodedata.normalize("NFKD", self.button2_text)
            self.button2_text = self.button2_text.replace("\n", " ")

            self.postback_data_button2 = unidecode.unidecode(self.button2_text).title()
            self.postback_data_button2 = remove_special_characters(self.postback_data_button2)
            self.postback_data_button2 = f"Button2_{self.postback_data_button2}"

            if "http" not in self.button2_url and self.button2_url != "":
                self.button2_url = f"https://{self.button2_url}".replace(" ", "")
            else:
                self.button2_url = self.button2_url.replace(" ", "")

        if self.id == "":
            input_ = input(f"Introduce el ID del mensaje {self.name}: ")
            self.id = input_.strip()

    def remove_zero_width_chars(self):
        def clean_text(text):
            return re.sub(r"[\u200B\u200C\u200D\u2060\uFEFF]", "", text)

        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                setattr(self, attr, clean_text(value))


def remove_special_characters(string: str):
    return re.sub(r"[^a-zA-Z0-9_]", "", string)


@dataclass
class MensajeRCS_v2:
    id: str
    name: str
    rcs_msg: StandaloneCard | CarouselCard
    fallback_msg: str
    url: None | str
