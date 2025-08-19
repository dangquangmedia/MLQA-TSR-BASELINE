# MLQA-TSR Baseline (Code Skeleton) — Bám sát dữ liệu BTC

## 1) Cấu trúc dữ liệu BTC
Sử dụng đúng 2 mục ban tổ chức cấp:
```
<dataset_root>/
├─ law_db/
│  ├─ vlsp2025_law.json
│  └─ images.zip
└─ train_data/
   ├─ vlsp_2025_train.json
   └─ train_images.zip
```
Hoặc dùng nguyên vẹn file ZIP tổng của BTC.

## 2) Cách chạy
### Cách A — ZIP gốc
```
python scripts/predict.py --dataset-zip "/path/to/VLSP 2025 - MLQA-TSR Data Release-XXXX.zip"
```
### Cách B — Thư mục đã giải nén
```
python scripts/predict.py --dataset-root "/path/to/extracted_root"
```
Kết quả: `outputs/submission_task1.json`, `outputs/submission_task2.json`, `outputs/submission.zip`.
