# Repository Review & Pre-Submission Checklist

A maintainer-style review of the project before your Bharatiya Antariksha Hackathon submission, plus a copy-paste checklist.

## 1. Suggested Repository Name

Your current folder name `cloud_removal` is fine locally but is too generic for a public GitHub repo. Pick one of these (in order of preference):

1. **`clearsky-liss4`** — short, descriptive, signals both the technique and the satellite product
2. **`gen-ai-cloud-removal`** — keyword-friendly for discoverability
3. **`liss4-cloud-reconstruction`** — most literal/academic-sounding
4. **`ClearSky`** (PascalCase, used as the project's display name in the README, even if the repo slug is lowercase-hyphenated)

The README above uses "ClearSky" as the display name — rename the GitHub repo itself to `clearsky-liss4` or similar (lowercase, hyphenated, no underscores, per GitHub convention).

## 2. What to Remove Before Pushing

Delete or `.gitignore` these from your actual working directory before `git add`:

- All contents of `uploads/`, `masks/`, `outputs/`, `results/`, `temp_images/`, `temp_masks/` — these are runtime artifacts, not source. Keep the folders via `.gitkeep` (empty placeholder files) so the structure is preserved.
- Any downloaded LaMa/IOPaint model weight files (`.pt`, `.pth`, `.ckpt`, `.onnx`, `.safetensors`) — these are large binaries that should never go into source control. IOPaint re-downloads them automatically on first run.
- `venv/` — never commit a virtual environment.
- Any `.DS_Store`, `__pycache__/`, or `*.pyc` files.
- Personal/local config files, API keys, or absolute file paths hardcoded for your machine.
- Duplicate or stale test images in `real_images/` — keep only 2–3 well-chosen samples for demo purposes (large image dumps bloat repo size and slow clones).

## 3. What to Add Before Pushing

- [ ] `assets/` folder with 2–4 actual screenshots (original / mask / output) and ideally one short demo GIF
- [ ] `.gitkeep` files in empty runtime folders (`uploads/.gitkeep`, `masks/.gitkeep`, etc.) so the structure survives even though contents are ignored
- [ ] `LICENSE` file (provided above)
- [ ] Updated `README.md` (provided above)
- [ ] Updated `.gitignore` (provided above)
- [ ] `requirements.txt` pinned or minimum-versioned (provided above — adjust versions to match what you actually tested with, via `pip freeze`)

## 4. Quick Commands to Generate `.gitkeep` Placeholders

```bash
cd cloud_removal
for d in uploads masks outputs results temp_images temp_masks; do
  mkdir -p "$d"
  touch "$d/.gitkeep"
done
```

## 5. Final Pre-Submission Checklist

- [ ] `git status` shows no `venv/`, no model weights, no uploaded user images
- [ ] `README.md` renders correctly on GitHub (check Mermaid diagrams render — GitHub supports Mermaid natively in `.md` files)
- [ ] Screenshots actually present in `assets/` and linked correctly
- [ ] `requirements.txt` installs cleanly in a **fresh** venv (`pip install -r requirements.txt` on a clean clone)
- [ ] App runs end-to-end from a fresh clone (`python app.py` → upload → output generated)
- [ ] License file present and referenced in README
- [ ] Repository description (GitHub "About" section) and topics/tags filled in — e.g. topics: `remote-sensing`, `generative-ai`, `image-inpainting`, `satellite-imagery`, `lama`, `flask`, `computer-vision`
- [ ] No personal absolute paths (e.g. `/home/yourname/...`) hardcoded in `app.py`
- [ ] Repo renamed to a professional slug (see Section 1)
- [ ] Commit history is reasonably clean (squash obvious "wip"/"fix typo" commits if you want extra polish, optional)

## 6. Suggested GitHub "About" Section

**Description:**
> Generative AI-based cloud detection and reconstruction for LISS-IV satellite imagery using OpenCV and LaMa (IOPaint). Prototype built for the Bharatiya Antariksha Hackathon.

**Topics:** `remote-sensing` `satellite-imagery` `generative-ai` `image-inpainting` `lama` `iopaint` `cloud-removal` `flask` `opencv` `computer-vision` `isro` `hackathon`
