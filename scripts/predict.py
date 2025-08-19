import argparse, os, json, zipfile, yaml
from pathlib import Path
from src.data_loader import load_from_zip, load_from_root, flatten_laws
from src.retriever_tfidf import TFIDFRetriever
from src.qa_rules import answer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-zip", type=str, default=None)
    ap.add_argument("--dataset-root", type=str, default=None)
    ap.add_argument("--config", type=str, default="configs/config.yaml")
    ap.add_argument("--output-dir", type=str, default="outputs")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))

    if args.dataset_zip:
        laws, data = load_from_zip(args.dataset_zip)
    elif args.dataset_root:
        laws, data = load_from_root(args.dataset_root)
    else:
        raise SystemExit("Cần --dataset-zip hoặc --dataset-root")

    law_items = flatten_laws(laws)
    retriever = TFIDFRetriever(law_items, max_law_chars=cfg["retriever"]["max_law_chars"])

    os.makedirs(args.output_dir, exist_ok=True)
    t1, t2 = [], []
    for ex in data:
        q = ex.get("question","")
        qtype = ex.get("question_type","")
        topk = retriever.search(q, top_k=cfg["retriever"]["top_k"]) or [{"law_id":"Không xác định","article_id":"0","score":0.0}]
        t1.append({"id":ex.get("id",""),"image_id":ex.get("image_id",""),"question":q,"relevant_articles":topk})
        ans = answer(q, qtype, yes_keywords=cfg["qa_rules"]["yes_keywords"], no_keywords=cfg["qa_rules"]["no_keywords"])
        t2.append({"id":ex.get("id",""),"image_id":ex.get("image_id",""),"question":q,"question_type":qtype or "Yes/No","relevant_articles":topk,"answer":ans})

    json.dump(t1, open(os.path.join(args.output_dir,"submission_task1.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(t2, open(os.path.join(args.output_dir,"submission_task2.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    import zipfile
    with zipfile.ZipFile(os.path.join(args.output_dir,"submission.zip"),"w",zipfile.ZIP_DEFLATED) as z:
        z.write(os.path.join(args.output_dir,"submission_task1.json"), arcname="submission_task1.json")
        z.write(os.path.join(args.output_dir,"submission_task2.json"), arcname="submission_task2.json")
    print("Done. See:", args.output_dir)

if __name__ == "__main__":
    main()
