# Backend run steps

Paths below use your **project root** (`pybot_NLP/`, parent of `backend/`) or the **`backend/`** folder. Scripts resolve paths from their own location, but you should still run commands as shown so imports and subprocess steps behave as expected.

Install dependencies once (from project root or with `-r` path adjusted):

```bash
pip install -r backend/requirements.txt
```

Raw Stack Overflow CSVs should live in **`pybot_data/`** at the project root (`pybot_data/Answers.csv`, `pybot_data/Questions.csv`).

---

## From project root (`pybot_NLP/`)

### Build pipeline (order matters)

```bash
python backend/scripts/build_answers_v2.py
```

```bash
python backend/scripts/build_final_dataset.py
```

```bash
python backend/scripts/build_retrieval_artifacts.py
```

Or run all three in sequence:

```bash
python backend/scripts/run_all_build_steps.py
```

### Verify artifacts and data

```bash
python backend/debug/verify_project.py
```

Other checks (optional):

```bash
python backend/debug/check_files.py
```

```bash
python backend/debug/validate_dataset.py
```

### Run the FastAPI server

```bash
cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000
```

From project root without changing directory:

```bash
cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000 && cd ..
```

Health check (in another terminal):

```bash
curl -s http://127.0.0.1:8000/health
```

---

## From inside `backend/`

### Build pipeline

```bash
python scripts/build_answers_v2.py
```

```bash
python scripts/build_final_dataset.py
```

```bash
python scripts/build_retrieval_artifacts.py
```

```bash
python scripts/run_all_build_steps.py
```

### Verify

```bash
python debug/verify_project.py
```

### Run FastAPI

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

## Outputs (default locations)

| Step | Output |
|------|--------|
| `build_answers_v2` | `backend/data/AnswersV2.csv` |
| `build_final_dataset` | `backend/data/final_chatbot_data.csv` |
| `build_retrieval_artifacts` | `backend/artifacts/vectorizer.pkl`, `question_vectors.pkl`, `chatbot_df.pkl` |

The API loads **only** the three files under **`backend/artifacts/`** at startup.

---

## Troubleshooting (paths and startup)

- **`ModuleNotFoundError: app`** — Run `uvicorn` with the **current working directory** set to `backend/` (see above). The `app` package lives at `backend/app/`.
- **`Missing required retrieval artifact(s)`** — Run the build pipeline so `backend/artifacts/` contains `vectorizer.pkl`, `question_vectors.pkl`, and `chatbot_df.pkl`. Confirm with `python backend/debug/verify_project.py` from the project root.
- **`input file not found` / missing CSV** — Ensure `pybot_data/Answers.csv` exists for `build_answers_v2`, and `pybot_data/Questions.csv` for `build_final_dataset`. Ensure `backend/data/AnswersV2.csv` exists before `build_final_dataset` (run `build_answers_v2` first).
- **Wrong working directory** — Build and debug scripts use **script-relative paths**; you can run them from any cwd. For **Uvicorn**, cwd must be `backend/` so `app.main:app` resolves.
- **Port in use** — Change the port, e.g. `--port 8001`.
