import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

state_dir = Path.home() / ".local_chat_toolkit"
state_dir.mkdir(exist_ok=True, parents=True)

models_dir = state_dir / "models"
models_dir.mkdir(exist_ok=True, parents=True)

state_file = state_dir / "state.json"


def get_formatted_now() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def format_model_name(name: str) -> str:
    return name.strip().replace(" ", "_").lower()


def get_model_list():
    return [model.name.replace(".json", "") for model in models_dir.glob("*.json")]


def load_model_instructions(name: str) -> str:
    model_file = _model_file_from_name(name)
    return json.loads(model_file.read_text())["instructions"]


def _model_file_from_name(name: str) -> Path:
    model_name = format_model_name(name)
    model_file = models_dir / f"{model_name}.json"
    return model_file


def save_new_model(name: str, instructions: str):
    model_file = _model_file_from_name(name)
    model_file.write_text(json.dumps({"name": name, "instructions": instructions}))


@dataclass
class State:
    """Keeps the state of the app."""

    @classmethod
    def load(cls):
        if state_file.exists():
            return cls(**json.loads(state_file.read_text()))
        return cls()
