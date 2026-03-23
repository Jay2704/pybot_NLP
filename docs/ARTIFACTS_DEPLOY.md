# Ship `backend/artifacts/*.pkl` to Hugging Face Docker

If the Space fails with missing `vectorizer.pkl` / `question_vectors.pkl` / `chatbot_df.pkl`, the files were usually **not in git** or **not in the Docker build context**.

---

## 1. Verify locally

```bash
python3 backend/debug/verify_artifacts_for_deploy.py
```

Expect three `OK` lines with non-zero byte sizes.

---

## 2. Track files in git

`.gitignore` allows only `backend/artifacts/*.pkl` (not other junk in that folder).

```bash
git add -f backend/artifacts/*.pkl
git ls-files backend/artifacts
```

You should see the three `.pkl` paths.

---

## 3. Commit and push

```bash
git add .gitignore .dockerignore Dockerfile backend/app/main.py backend/debug/verify_artifacts_for_deploy.py
git commit -m "Fix: track retrieval artifacts for HF Docker deployment"
git push origin main
```

Use your real remote/branch instead of `origin main` if different. For a Hugging Face git remote, e.g.:

```bash
git push hf main
```

---

## 4. Validate inside a local container

```bash
docker build -t pybot-chatbot .
docker run --rm -d --name pybot-test -p 7860:7860 pybot-chatbot
docker exec pybot-test ls -la /app/backend/artifacts
docker stop pybot-test
```

Expect the three `.pkl` files listed with non-zero sizes.

---

## 5. Space logs

After deploy, open the Space **Logs**. You should see lines like:

`Deploy probe: artifact directory file names: [...]`  
`Deploy probe: vectorizer.pkl ... exists=True bytes=...`

If `exists=False` or the list is empty, the build context on HF did not contain the files — confirm **git push** included them and rebuild the Space.
