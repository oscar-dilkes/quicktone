import json
import os
import sys
from pathlib import Path

_BASE_PATH = Path("../../data")

def main(file_path: Path):
    print(f"Relative file path is '{file_path}'")
    
    data: str = reader(file_path)
    split_records: list[dict] = splitter(data)
    
    jsonl_name = file_path.stem + ".jsonl"
    
    writer(split_records=split_records, jsonl_name=jsonl_name)

def reader(file_path: Path) -> list[str]:
    print("Reading file...")
    
    with open(file_path, "r", encoding="latin-1") as file:
        return file.readlines()

def splitter(data: list[str]) -> dict:
    split_records: list[dict] = []
    
    print("Splitting records...")
    
    for record in data:
        split_record = record.split("@")
        if len(split_record) != 2:
            raise ValueError(f"Either no instance or more than one instance of delimiter ' .@' in the following record:\n{record}")
        split_records.append({"text": split_record[0], "label": split_record[1].strip()})
        
    return split_records

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
    
    