from pathlib import Path
from typing import IO
from xml.etree.ElementTree import Element

import chardet


def open_text_file(file_path: str | Path) -> IO[str]:
    enc = guess_encoding(file_path)
    f = open(file_path, encoding=enc)
    return f


def guess_encoding(file_path: str | Path, byte_count: int = 10000) -> str | None:
    with open(file_path, "rb") as file:
        data = file.read(byte_count)

    result = chardet.detect(data)
    encoding = result["encoding"]
    return "utf-8" if encoding == "ascii" else encoding


def format_xml_tag(elem: Element) -> str:
    if not elem.attrib:
        return f"<{elem.tag}>"
    attributes = " ".join(f'{name}="{value}"' for name, value in elem.attrib.items())
    return f"<{elem.tag} {attributes}>"
