import requests
from pathlib import Path

NODE56 = "http://192.168.1.56:8000"


def upload_package(zip_path):

    zip_path = Path(zip_path)

    if not zip_path.exists():
        raise FileNotFoundError(zip_path)

    with open(zip_path, "rb") as f:

        files = {
            "file": (
                zip_path.name,
                f,
                "application/zip"
            )
        }

        response = requests.post(
            f"{NODE56}/api/deployment/upload",
            files=files,
            timeout=300
        )

    return response.json()


if __name__ == "__main__":

    result = upload_package(
        r"E:\AI-Server\packages\AI-LAB-7.0.0.zip"
    )

    print(result)
