import json

encodings = ["utf-8", "utf-16", "utf-16-le", "utf-16-be"]

for enc in encodings:
    try:
        with open("db_backup.json", "r", encoding=enc) as f:
            data = json.load(f)

        print(f"Successfully loaded using {enc}")

        with open("db_backup_utf8.json", "w", encoding="utf-8") as out:
            json.dump(data, out, ensure_ascii=False, indent=2)

        print("Converted to UTF-8 successfully")
        break

    except Exception as e:
        print(f"{enc} failed: {e}")