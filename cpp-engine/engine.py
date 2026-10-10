
import json
import subprocess
from pathlib import Path

ENGINE_PATH = Path(__file__).parent / "main.exe"


def process_numbers(numbers: list[int]) -> dict:
    input_data = f"{len(numbers)}\n"
    input_data += " ".join(map(str, numbers)) + "\n"

    result = subprocess.run(
        [str(ENGINE_PATH)],
        input=input_data,
        capture_output=True,
        text=True,
        check=True,
        timeout=10
    )

    return json.loads(result.stdout)
