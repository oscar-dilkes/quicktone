import json
import os
import sys
import re
from pathlib import Path


_BASE_PATH = Path("../../data")
_SPLIT_DECIMAL = re.compile(r"(\d) \.(\d)")
_SPLIT_THOUSANDS = re.compile(r"(\d) ,(\d{3})\b")
_UNICODE_EUrO = re.compile(r"x20ac")


def main(file_path: Path):
    print(f"relative file path is '{file_path}'")
    
    data: list[str] = reader(file_path=file_path)
    merged_values_data: list[str] = merge_values(data=data)
    split_records: list[dict] = split(data=merged_values_data)
    deduped_records: list[dict] = dedupe(records=split_records)
    
    jsonl_name = file_path.stem + ".jsonl"
    
    writer(split_records=split_records, jsonl_name=jsonl_name)


def reader(file_path: Path) -> list[str]:
    print("reading file...")
    
    with open(file_path, "r", encoding="latin-1") as file:
        return file.readlines()
    
    
def merge_values(data: list[str]) -> list[str]:
    data = [_SPLIT_DECIMAL.sub(r"\1.\2", line) for line in data]
    data = [_SPLIT_THOUSANDS.sub(r"\1,\2", line) for line in data]
    data = [_UNICODE_EUrO.sub(r"€", line) for line in data]
    
    return data
    
    
def split(data: list[str]) -> list[dict]:
    split_records: list[dict] = []
    
    print("Splitting records...")
    
    for record in data:
        split_record = record.split("@")
        if len(split_record) != 2:
            raise ValueError(f"Either no instance or more than one instance of delimiter ' .@' in the following record:\n{record}")
        split_records.append({"text": split_record[0], "label": split_record[1].strip()})
        
    return split_records


def dedupe(records: list[dict]) -> list[dict]:
    labels_by_text: dict[str, set[str]] = {}
    for record in records:
        labels_by_text.setdefault(record["text"], set()).add(record["label"])

    seen: set[str] = set()
    out = []
    for record in records:
        text = record["text"]
        if text in seen or len(labels_by_text[text]) > 1:
            continue
        seen.add(text)
        out.append(record)
    return out


def writer(split_records: list[dict], jsonl_name: Path):
    print("Writing JSONL...")
    
    jsonl_path = _BASE_PATH / "jsonl" / jsonl_name
    
    with open(jsonl_path, "w", encoding="utf-8") as file:
        for record in split_records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
            
    print(f"JSONL written to '{jsonl_path}'")
    

if __name__ == "__main__":
    file_name = Path(sys.argv[1])
    file_path = _BASE_PATH / "raw" / file_name
    main(file_path=file_path)
    
    