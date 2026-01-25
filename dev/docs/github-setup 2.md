# GitHub Repository Setup Guide

Step-by-step instructions for initializing and pushing your project to GitHub.

---

## 🎯 Repository Configuration

**Repository Name:** `sentiment-regime-detector`  
**Visibility:** Public  
**Description:** Cross-Asset Sentiment Regime Detector - Automated market psychology analysis using transformer-based NLP (SMU MSDS Capstone 2026)  
**Topics:** `machine-learning`, `nlp`, `finance`, `sentiment-analysis`, `transformers`, `fintech`, `regime-detection`, `capstone-project`

---

## 📋 Step 1: Create Repository on GitHub

### Via GitHub Web Interface

1. Go to <https://github.com/new>
2. Fill in details:
   - **Repository name:** `sentiment-regime-detector`
   - **Description:** Cross-Asset Sentiment Regime Detector - Automated market psychology analysis using transformer-based NLP (SMU MSDS Capstone 2026)
   - **Visibility:** ☑️ Public
   - **Initialize:** ☐ Do NOT check "Add README" (you already have one)
   - **Initialize:** ☐ Do NOT check "Add .gitignore" (you already have one)
   - **License:** Choose MIT License (or None for now)
3. Click **Create repository**

You'll see a page with instructions—**ignore them** and follow the steps below instead.

---

## 📋 Step 2: Initialize Local Git Repository

```bash

# Navigate to project root

cd ~/Documents/SMU/DS_6210_Capstone

# Initialize git (if not already done)

git init

# Check current status

git status

```text

**Expected output:**

```text

```bash
On branch master (or main)
Untracked files:
   .gitignore
   README.md
   course_files/
   dev/
```

---

## 📋 Step 3: Configure Git (First Time Only)

```bash

# Set your name and email (use your SMU credentials)

git config --global user.name "Jonathan Rocha"
git config --global user.email "<jrocha@smu.edu>"

# Set default branch name to 'main'

git config --global init.defaultBranch main

# Verify settings

git config --list

```

---

## 📋 Step 4: Add Files to Git

```bash
# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status

# Review specific changes (optional)
git diff --staged
```

**Verify:** Make sure no secrets or large files are staged. Check for:

- ❌ `config/api_keys.json`
- ❌ `.env` files
- ❌ Large CSVs in `dev/data/`
- ✅ `.gitignore` itself
- ✅ `README.md`
- ✅ All markdown docs

---

## 📋 Step 5: Create Initial Commit

```bash

# Commit with descriptive message

git commit -m "Initial commit: Project structure setup

- Add workspace organization (code/, docs/, research/, etc.)
- Add comprehensive .gitignore for Python/React/data files
- Add project README with timeline and milestones
- Add Todoist automation script for project management
- Add literature review search prompts
- Add Week 1 checklist and documentation guides
- Reorganize legacy files into subdirectory structure"

# Verify commit was created

git log --oneline

```

---

## 📋 Step 6: Connect to Remote Repository

```bash
# Add GitHub remote (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/jonx0037/sentiment-regime-detector.git

# Verify remote was added
git remote -v
```text

**Expected output:**

``` bash
origin  <https://github.com/jonx0037/sentiment-regime-detector.git> (fetch)
origin  <https://github.com/jonx0037/sentiment-regime-detector.git> (push)
```

---

## 📋 Step 7: Push to GitHub

```bash
# Rename branch to 'main' (if currently 'master')
git branch -M main

# Push to remote repository
git push -u origin main
```

If prompted for credentials:

- **Username:** Your GitHub username
- **Password:** Use a Personal Access Token (PAT), NOT your GitHub password
  - Generate PAT: <https://github.com/settings/tokens>
  - Scopes needed: `repo` (full control of private repositories)

---

## 📋 Step 8: Create `develop` Branch

```bash

# Create develop branch from main

git checkout -b develop

# Push develop branch to remote

git push -u origin develop

# Switch back to main

git checkout main

```

**Branch Strategy:**

- `main` - Production-ready code, final deliverables
- `develop` - Active development, work-in-progress
- `feature/*` - Optional feature branches (e.g., `feature/data-pipeline`)

---

## 📋 Step 9: Verify Repository on GitHub

1. Go to <https://github.com/YOUR_USERNAME/sentiment-regime-detector>
2. Check that you see:
   - ✅ README.md displayed on homepage
   - ✅ Directory structure (`dev/`, `course_files/`)
   - ✅ `.gitignore` file
   - ✅ Initial commit message
   - ✅ Two branches (`main`, `develop`)

---

## 🔧 Optional: Set Up GitHub Pages (For Future Dashboard Deployment)

### Enable GitHub Pages

1. Go to: <https://github.com/jonx0037/sentiment-regime-detector/settings/pages>
2. Under "Source", select:
   - Branch: `main`
   - Folder: `/docs` (or `/` for root)
3. Click **Save**
4. Your site will be published at: `https://jonx0037.github.io/sentiment-regime-detector/`

**Note:** This is for later when you build the React dashboard. For now, just enable it.

---

## 🔧 Optional: Add Repository Topics

1. Go to: <https://github.com/jonx0037/sentiment-regime-detector>
2. Click the gear icon next to "About"
3. Add topics:
   - `machine-learning`
   - `nlp`
   - `finance`
   - `sentiment-analysis`
   - `transformers`
   - `fintech`
   - `regime-detection`
   - `capstone-project`
   - `python`
   - `react`
4. Add website URL (when deployed)
5. Click **Save changes**

---

## 📝 Daily Git Workflow (Going Forward)

### When Starting Work

```bash
# Switch to develop branch
git checkout develop

# Pull latest changes (if collaborating)
git pull origin develop

# Create feature branch (optional)
git checkout -b feature/literature-review
```

### While Working

```bash

# Check status frequently

git status

# Stage specific files

git add dev/research/draft-0.md
git add dev/research/literature-notes.md

# Commit with meaningful message

git commit -m "Expand literature review with 3 new papers on cross-asset sentiment"

```

### End of Day

```bash
# Push to remote
git push origin develop

# Or if on feature branch
git push origin feature/literature-review
```

### When Feature is Complete

```bash
# Switch to develop
git checkout develop

# Merge feature branch
git merge feature/literature-review

# Delete feature branch
git branch -d feature/literature-review

# Push merged changes
git push origin develop
```

### When Ready for Release (End of Week, Milestone)

```bash
# Switch to main
git checkout main

# Merge develop into main
git merge develop

# Tag release
git tag -a v0.1-draft-0 -m "Draft 0 completed"

# Push with tags
git push origin main --tags
```

---

## 🛡️ Git Best Practices

### ✅ DO

- Commit frequently (multiple times per day)
- Write clear, descriptive commit messages
- Review changes before committing (`git diff`)
- Use `.gitignore` to exclude secrets and large files
- Pull before pushing (if collaborating)
- Create branches for experimental work

### ❌ DON'T

- Commit API keys, passwords, or secrets
- Commit large datasets (>10MB) - use Git LFS instead
- Use generic commit messages ("updated files", "changes")
- Work directly on `main` branch (use `develop`)
- Force push (`git push -f`) unless you know what you're doing
- Commit generated files (build artifacts, `__pycache__/`)

---

## 🆘 Common Issues & Solutions

### Issue: "Repository not found" when pushing

**Solution:**

```bash
# Check remote URL
git remote -v

# If wrong, remove and re-add
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/sentiment-regime-detector.git
```

### Issue: Authentication failed

**Solution:** Use Personal Access Token (PAT) instead of password

1. Generate PAT: <https://github.com/settings/tokens>
2. Use PAT as password when prompted
3. Cache credentials (so you don't have to re-enter):

```bash
git config --global credential.helper cache
# Or use macOS keychain
git config --global credential.helper osxkeychain
```

### Issue: Large files rejected

**Solution:**

```bash
# If file >100MB, Git will reject it
# Option 1: Add to .gitignore and don't commit
echo "dev/data/large_dataset.csv" >> .gitignore

# Option 2: Use Git LFS for large files
git lfs install
git lfs track "*.csv"
git add .gitattributes
```

### Issue: Committed secrets by accident

**Solution:**

```bash
# Remove file from history (DANGER: rewrites history)
git rm --cached config/api_keys.json
git commit -m "Remove accidentally committed secrets"
git push origin develop

# Then rotate/regenerate all exposed secrets immediately
```

### Issue: Merge conflicts

**Solution:**

```bash
# When pulling causes conflicts
git status  # See which files have conflicts

# Open conflicted files, look for:
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> branch-name

# Manually resolve conflicts, then:
git add resolved-file.md
git commit -m "Resolve merge conflict in draft-0.md"
```

---

## 📊 Useful Git Commands Reference

```bash
# View commit history
git log --oneline --graph --all

# See what changed in last commit
git show

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes (DANGER)
git reset --hard HEAD

# Create and switch to new branch
git checkout -b feature/new-feature

# List all branches
git branch -a

# Delete local branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature

# Stash uncommitted changes
git stash
git stash pop  # Restore stashed changes

# View differences
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git diff main develop       # Between branches

# Search commit messages
git log --grep="literature"

# Find when a bug was introduced
git bisect start
git bisect bad    # Current version has bug
git bisect good v0.1  # This version was good
# Git will check out commits for you to test

# Amend last commit message
git commit --amend -m "New message"
```

---

## 🎯 Week 1 Git Milestones

By end of Week 1, you should have:

- [x] GitHub repository created (public)
- [x] Initial commit with workspace structure
- [x] `main` and `develop` branches
- [ ] 5-10 commits documenting Draft 0 progress
- [ ] All work on `develop` branch
- [ ] GitHub Pages enabled (for future deployment)
- [ ] Repository description and topics added

---

## 📚 Additional Resources

- **Git Basics:** <https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control>
- **GitHub Guides:** <https://guides.github.com/>
- **Git Cheat Sheet:** <https://education.github.com/git-cheat-sheet-education.pdf>
- **Visualizing Git:** <https://git-school.github.io/visualizing-git/>
- **SMU Git Workshop:** (Check if SMU Lyle offers Git training)

---

**Next Steps:**

1. Complete Steps 1-9 above
2. Update README.md with your actual GitHub username
3. Add repository URL to Todoist project
4. Share repo link with advisor (once confirmed)

**Estimated Time:** 30 minutes
