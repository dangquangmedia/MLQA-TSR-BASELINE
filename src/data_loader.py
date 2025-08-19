import os, json, zipfile

def _detect_prefix(names):
    for n in names:
        if n.endswith("README.txt"):
            return n[:-10]
    import os as _os
    return _os.path.commonprefix(names)

def load_from_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()
        prefix = _detect_prefix(names)
        laws = json.loads(z.read(prefix + "law_db/vlsp2025_law.json").decode("utf-8"))
        train = json.loads(z.read(prefix + "train_data/vlsp_2025_train.json").decode("utf-8"))
        return laws, train

def load_from_root(root):
    with open(os.path.join(root, "law_db", "vlsp2025_law.json"), encoding="utf-8") as f:
        laws = json.load(f)
    with open(os.path.join(root, "train_data", "vlsp_2025_train.json"), encoding="utf-8") as f:
        train = json.load(f)
    return laws, train

def flatten_laws(laws):
    items = []
    def add(law_id, article_id, content):
        if content and isinstance(content, str):
            items.append({"law_id": law_id, "article_id": article_id, "content": content})
    if isinstance(laws, list):
        for x in laws:
            law_id = x.get("law_id") or x.get("law") or "UNKNOWN_LAW"
            article_id = x.get("article_id") or x.get("article") or x.get("id") or "UNKNOWN_ART"
            content = x.get("content") or x.get("text") or ""
            add(law_id, article_id, content)
    elif isinstance(laws, dict):
        for law_id, group in laws.items():
            if isinstance(group, dict):
                for article_id, content in group.items():
                    if isinstance(content, str):
                        add(law_id, str(article_id), content)
                    else:
                        import json as _json
                        add(law_id, str(article_id), _json.dumps(content, ensure_ascii=False))
    return items
