# Workspace Audit - Part 2 Continuation Prompt

**Context:** This is the continuation of a comprehensive workspace audit started on Feb 3, 2026. Part 1 completed 7 of 14 tasks. This prompt will guide completion of the remaining 7 tasks.

---

## Background

I'm working on my SMU capstone project (sentiment regime detector) and recently completed the first phase of a comprehensive workspace audit to eliminate redundancies and improve organization. We've made excellent progress, and I need to complete the remaining organizational tasks.

---

## ✅ Completed in Part 1 (7/14 tasks)

1. **Security Audit** - Verified API keys never exposed in git history
2. **Environment Configuration** - .env.example properly configured with placeholders
3. **Dependency Consolidation** - Migrated from 3 files (requirements.txt, requirements.minimal.txt, pyproject.toml) to single source of truth in pyproject.toml
4. **Docker Standardization** - Consolidated docker-compose.yml and docker-compose.dev.yml into single file with profiles
5. **Session Log Archive** - Moved 10 session markdown files to `/archive/dev-sessions-jan-feb-2026/`
6. **Legacy /dev/ Directory Removal** - Archived and removed 36 outdated markdown files, updated README.md
7. **Scripts Reorganization** - Organized 89 scripts from flat structure into 10 functional directories (data_collection, data_import, validation, analysis, backtesting, processing, visualization, admin, ml_training, hpc)

**Key Files Created:**

- `/archive/README.md` - Archive documentation
- `DEPENDENCY_MIGRATION.md` - Migration guide for pyproject.toml
- `DOCKER_GUIDE.md` - Comprehensive Docker usage guide
- `scripts/README.md` - Complete scripts directory documentation

**Key Changes:**

- All operations used `git mv` and `git rm` to preserve history
- Updated references in README.md, spark/README.md, package_for_hpc.sh
- Removed 48 files total (tracked properly in git)

---

## 🎯 Remaining Tasks (7/14) - Prioritized

### Priority 2 (High Impact)

**Task 8: Create /data/README.md documenting pipeline and datasets**

- Document data flow: raw → processed → analysis
- Explain each subdirectory purpose (/kaggle, /processed, /raw, /hpc_batches)
- Create data pipeline flowchart or diagram
- Document data retention/archival policies

**Task 9: Audit and document dataset redundancies in /data/kaggle/**

- The audit found 21 potentially overlapping datasets in `/data/kaggle/`
- Key redundancies to investigate:
  - `stock_news/` vs `stocknews/` - Are these duplicates?
  - `financial-news/` vs `financial-news-nlp-2025/` - Different processing?
  - Multiple Reddit datasets: `reddit-finance/`, `reddit-sentiment-2025/`, `crypto-reddit/`, `wsb/`, `wsb-2022/`, `wsb-echo-chamber/`
  - Multiple crypto datasets: `crypto/`, `crypto-tweets/`, `crypto-reddit/`
- Create `/data/kaggle/README.md` with:
  - Dataset catalog table (name, source, date acquired, size, purpose)
  - Temporal coverage information
  - Overlap/redundancy notes
  - Recommended datasets for each use case

**Task 10: Consolidate test placement strategy**

- Current issue: Tests split between `/tests/` and `/src/*/tests/` subdirectories
- Decision needed:
  - Option A (recommended): Move all tests to `/tests/` with mirrored structure
  - Option B: Keep tests with code, remove `/tests/` directory
- Update pytest configuration in pyproject.toml if needed
- Document the chosen strategy

### Priority 3 (Medium - Quick Wins)

**Task 11: Fix .gitignore references**

- Problem: `.gitignore` references `/config/` directory that doesn't exist
- Lines to fix/remove:
  - `config/api_keys.json`
  - `config/credentials.json`
  - `config/secrets.json`
- Check if `/config/` directory should be created or references removed
- Verify no other broken .gitignore patterns

**Task 12: Create comprehensive /docs/ directory structure**

- Create `/docs/` directory with:
  - `API.md` - API endpoint documentation
  - `DATA_PIPELINE.md` - Data flow and processing stages
  - `ARCHITECTURE.md` - System design overview
  - `DEVELOPMENT.md` - Setup and contribution guide
  - `DEPLOYMENT.md` - Docker, HPC, production deployment
  - `DATASETS.md` - Kaggle datasets catalog (link to /data/kaggle/README.md)
  - `SCRIPTS.md` - Utility scripts reference (link to /scripts/README.md)
- Consider consolidating/moving existing documentation:
  - DOCKER_GUIDE.md → docs/DEPLOYMENT.md section?
  - DEPENDENCY_MIGRATION.md → docs/DEVELOPMENT.md section?

### Priority 4 (Low - Polish)

**Task 13: Standardize naming conventions**

- Establish conventions:
  - Directories: `kebab-case` or `snake_case`?
  - Python files: `snake_case` (already good)
  - Test files: `test_{module}.py` (already good)
  - Session docs: `YYYY-MM-DD_SESSION_NAME.md`
- Current inconsistencies:
  - Data directories mix: `stock_tweets/` (snake) vs `wsb-2022/` (kebab)
  - HPC batches: `hpc_batches/` vs `maneframe_output/`
- Document chosen conventions in a `CONVENTIONS.md` or in docs/DEVELOPMENT.md

**Task 14: Clean up root directory**

- Current root directory has too many files
- Consider moving:
  - DOCKER_GUIDE.md → docs/
  - DEPENDENCY_MIGRATION.md → docs/ or archive/
  - Other technical docs to appropriate locations
- Goal: Keep root directory minimal (README, LICENSE, pyproject.toml, docker-compose.yml, .env.example, .gitignore)

---

## 📋 Specific Action Items

### For Task 8 (Data README)

Check these directories exist and document them:

```bash
ls -la data/
ls -la data/kaggle/
ls -la data/processed/
ls -la data/hpc_batches/
```

### For Task 9 (Dataset Audit)

Get dataset information:

```bash
cd data/kaggle
for d in */; do echo "=== $d ==="; du -sh "$d"; find "$d" -type f | wc -l; done
```

### For Task 10 (Test Consolidation)

Find all test locations:

```bash
find src -type d -name "tests"
find tests -type f -name "*.py"
```

### For Task 11 (.gitignore Fix)

Check the problematic lines:

```bash
grep -n "config/" .gitignore
ls -la config/ 2>/dev/null || echo "config/ does not exist"
```

---

## 🎯 Success Criteria

By the end of Part 2, the project should have:

- [ ] Clear data pipeline documentation
- [ ] No dataset redundancies or clear documentation of overlaps
- [ ] Consistent test placement strategy
- [ ] Clean .gitignore with no broken references
- [ ] Professional `/docs/` directory with comprehensive guides
- [ ] Documented naming conventions
- [ ] Minimal, organized root directory

**Estimated Time:** 6-12 hours (remaining from 14-22 hour total estimate)

---

## 📚 Reference Information

**Project Structure (Current):**

```
DS_6210_Capstone/
├── src/sentiment_detector/    # Core application
├── frontend/                   # React dashboard
├── tests/                      # Test suite
├── scripts/                    # Organized utility scripts (✅ DONE)
├── data/                       # Data storage (needs documentation)
├── archive/                    # Historical docs (✅ DONE)
├── docs/                       # TO BE CREATED
├── pyproject.toml             # Single source for dependencies (✅ DONE)
├── docker-compose.yml         # Unified with profiles (✅ DONE)
└── README.md                  # Updated (✅ DONE)
```

**Key Git Repositories:**

- Main branch: `main`
- All changes should use `git mv` and `git rm` to preserve history

**Environment:**

- Python 3.11+
- PostgreSQL 15 + Redis 7 (via Docker)
- Project uses pyproject.toml for dependencies

---

## 💬 Starting the Session

**Suggested opening message:**

"I'm continuing a comprehensive workspace audit for my SMU capstone project. I've completed 7 of 14 tasks (see WORKSPACE_AUDIT_PART2_PROMPT.md for details). I need to complete the remaining 7 tasks focusing on:

1. Data pipeline documentation (/data/README.md)
2. Dataset redundancy audit (21 Kaggle datasets)
3. Test consolidation strategy
4. Fix .gitignore broken references
5. Create /docs/ directory structure
6. Document naming conventions
7. Root directory cleanup

Please read WORKSPACE_AUDIT_PART2_PROMPT.md and let me know when you're ready to start with Task 8 (data pipeline documentation)."

---

## 📝 Notes for Claude

- All previous work preserved full git history
- User prefers systematic, thorough approach
- Use TodoWrite to track progress through the 7 tasks
- When in doubt, ask clarifying questions
- Maintain same documentation quality as Part 1
- Remember: User chose "everything systematically" approach

---

*Created: February 3, 2026 | Part 1 completed ~8-10 hours of work*
