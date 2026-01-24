# Workspace Setup Complete ✅

**Date:** January 10, 2026 (Saturday)  
**Status:** Ready for Week 1 work

---

## 🎉 What We Accomplished

### 1. Workspace Reorganization

- ✅ Created 6 subdirectories: `code/`, `config/`, `data/`, `docs/`, `research/`, `results/`
- ✅ Moved 20+ legacy files to proper locations
- ✅ Renamed files to use kebab-case convention
- ✅ Removed old `drafts/` folder

### 2. Git Configuration

- ✅ Created comprehensive `.gitignore` (Python, React, data, secrets)
- ✅ Set up for public GitHub repository
- ✅ Defined branch strategy: `main` (releases) + `develop` (active work)

### 3. Project Management

- ✅ Created **Todoist automation script** (`dev/code/todoist_setup.py`)
  - Auto-creates 30+ tasks across 10-week timeline
  - Organized by week/section with due dates and priorities
  - Run with: `export TODOIST_API_TOKEN="..." && python dev/code/todoist_setup.py`

### 4. Documentation

- ✅ **Main README.md** - Project overview, tech stack, getting started
- ✅ **Week 1 Checklist** (`dev/docs/week-1-checklist.md`) - Detailed task breakdown
- ✅ **Literature Review Prompts** (`course_files/paper-drafts/literature-review-prompts.md`) - Search queries for 5-8 papers
- ✅ **GitHub Setup Guide** (`dev/docs/github-setup.md`) - Step-by-step repo initialization
- ✅ **Workspace Organization** (`dev/docs/workspace-organization.md`) - File structure reference

---

## 📂 New Directory Structure

```plaintext
DS_6210_Capstone/
├── .gitignore                    # Git ignore rules
├── README.md                     # Project overview
│
├── course_files/                 # SMU templates (read-only)
│   ├── MSDS Journal Paper Template.pdf
│   ├── ds-6120_syllabus.pdf
│   └── [other course materials]
│
└── dev/
    ├── code/                     # Source code
    │   ├── todoist_setup.py     # ✨ NEW: Project management automation
    │   ├── data-pipeline-orchestrator.md
    │   └── reddit-data-collection.md
    │
    ├── config/                   # Configuration files
    │   ├── config-template.md
    │   ├── environment-files.md
    │   ├── requirements.md
    │   └── requirements-hpc.md
    │
    ├── data/                     # Data scripts & datasets (git-ignored)
    │
    ├── docs/                     # Technical documentation
    │   ├── week-1-checklist.md          # ✨ NEW: This week's tasks
    │   ├── github-setup.md              # ✨ NEW: Repo initialization guide
    │   ├── workspace-organization.md    # ✨ NEW: File structure reference
    │   ├── backend-deployment.md
    │   ├── ci-cd-pipeline.md
    │   ├── docker-compose.md
    │   ├── dockerfile-dev.md
    │   ├── dockerfile-prod.md
    │   ├── frontend-dockerfile.md
    │   ├── git-workflow.md
    │   ├── k8s-deployment.md
    │   ├── makefile-commands.md
    │   ├── maneframe-hpc-workflow.md
    │   ├── requirements-structure.md
    │   ├── slurm-job-template.md
    │   └── usage-commands.md
    │
    ├── research/                 # Academic papers & drafts
    │   ├── draft-0.md                   # Current working draft
    │   ├── project-proposal.md
    │   └── literature-review-prompts.md # ✨ NEW: Search strategies
    │
    └── results/                  # Model outputs (git-ignored)
```

---

## 🚀 Immediate Next Steps (This Weekend)

### Saturday Evening (Jan 10)

1. **Set up Todoist** (30 min)

   ```bash
   pip install todoist-api-python
   export TODOIST_API_TOKEN="your_token_from_todoist.com/prefs/integrations"
   python dev/code/todoist_setup.py
   ```

2. **Initialize GitHub repo** (30 min)
   - Follow: [dev/docs/github-setup.md](dev/docs/github-setup.md)
   - Create public repo: `sentiment-regime-detector`
   - Push initial commit

### Sunday (Jan 11)

1. **Literature search** (4-5 hours)
   - Use: [course_files/paper-drafts/literature-review-prompts.md](course_files/paper-drafts/literature-review-prompts.md)
   - Find 5-8 papers across 4 themes
   - Download PDFs, skim abstracts

### Monday (Jan 12)

1. **Read papers in depth** (5-6 hours)
   - Annotate key findings, methodology, gaps
   - Create notes file: `course_files/paper-drafts/literature-notes.md`

2. **Send critical emails**
   - MANEFRAME access request: <help@smu.edu>
   - Faculty advisor request (after identifying candidate)

---

## 📋 Week 1 Goals (Due: Jan 17)

### Priority 1: Draft 0 Completion

- [ ] Expand literature review (Section 2) with 5-8 new papers
- [ ] Complete methods section (Section 3)
- [ ] Revise abstract to 150-200 words
- [ ] Proofread and remove all placeholder text

### Priority 2: Project Setup

- [ ] GitHub repository live with initial commit
- [ ] Todoist tasks created and organized
- [ ] MANEFRAME access requested
- [ ] Faculty advisor confirmed (or backup identified)

---

## 📊 Key Resources at a Glance

| Need                   | Resource                                                                               |
| ---------------------- | -------------------------------------------------------------------------------------- |
| **This week's tasks**  | [dev/docs/week-1-checklist.md](dev/docs/week-1-checklist.md)                           |
| **Literature search**  | [course_files/paper-drafts/literature-review-prompts.md](course_files/paper-drafts/literature-review-prompts.md) |
| **File organization**  | [dev/docs/workspace-organization.md](dev/docs/workspace-organization.md)               |
| **GitHub setup**       | [dev/docs/github-setup.md](dev/docs/github-setup.md)                                   |
| **Current draft**      | [course_files/paper-drafts/draft-0.md](course_files/paper-drafts/draft-0.md)                                     |
| **Project overview**   | [README.md](../README.md)                                                              |
| **Todoist automation** | [dev/code/todoist_setup.py](dev/code/todoist_setup.py)                                 |

---

## 🎯 Success Metrics (End of Week 1)

You'll know you're on track if:

- ✅ Draft 0 has no placeholder text
- ✅ Literature review cites 12-20 papers (3-4 per subsection)
- ✅ GitHub repo has 5-10 commits documenting progress
- ✅ Todoist shows 6/6 Week 1 tasks completed
- ✅ You have MANEFRAME access (or confirmation of pending approval)
- ✅ You have an advisor (or backup plan in place)

---

## 🤖 Todoist Preview (Auto-Generated Tasks)

When you run `todoist_setup.py`, you'll get:

**Week 1 (6 tasks):**

- Complete literature review expansion (Due: Jan 15) [P1]
- Finalize methods section (Due: Jan 16) [P1]
- Complete abstract/intro revisions (Due: Jan 17) [P1]
- Set up GitHub repo (Due: Jan 12) [P2]
- Request MANEFRAME access (Due: Jan 13) [P2]
- Finalize faculty advisor (Due: Jan 14) [P2]

**Weeks 2-10 (24 more tasks):**

- Data collection pipeline (Weeks 2-3)
- EDA & preprocessing (Week 4)
- Model training on MANEFRAME (Weeks 5-6)
- Feature engineering (Week 7)
- Regime classification (Weeks 8-9)
- Dashboard deployment & final deliverables (Week 10)

---

## 💡 Tips for Success

### Time Management

- **Block 4-6 hours/day** for capstone work (Mon-Fri)
- **Front-load literature review** (this weekend) so next week is writing-focused
- **Use Pomodoro technique** (25 min work, 5 min break) for deep focus

### Literature Review

- **Don't over-perfect** - Draft 0 needs breadth, Draft 1 will have depth
- **Use AI tools** (Perplexity, Semantic Scholar) to accelerate search
- **Focus on recent papers** (2018+) for transformer/NLP work

### Writing

- **Write messy first drafts** - You can always revise later
- **One section per day** (Mon: Lit Review, Tue: Methods, Wed: Abstract/Intro)
- **Peer feedback** - Share with classmates for quick review

### Blockers

- **MANEFRAME access delayed?** → Use Google Colab Pro for initial experiments
- **Advisor ghosting?** → Reach out to backup within 48 hours
- **Stuck on writing?** → Ask Claude/ChatGPT for paragraph starters (then rewrite in your voice)

---

## 🆘 If You Need Help

**Technical Issues:**

- Git/GitHub: [dev/docs/github-setup.md](dev/docs/github-setup.md)
- File organization: [dev/docs/workspace-organization.md](dev/docs/workspace-organization.md)
- Todoist setup: Check script comments in `dev/code/todoist_setup.py`

**Writing Issues:**

- Use course_files templates as examples
- Review `sample_of_draft_0.pdf` for structure guidance
- Check APA format: <https://owl.purdue.edu/owl/research_and_citation/apa_style/>

**Research Issues:**

- Literature search: [course_files/paper-drafts/literature-review-prompts.md](course_files/paper-drafts/literature-review-prompts.md)
- Methods clarity: Review papers with similar methodologies (FinBERT, regime detection)
- Advisor questions: Draft email and send Monday morning

---

## 📅 Timeline Reminder

**Key Dates:**

- **Jan 17 (Fri):** Draft 0 due
- **Mar 20 (Fri):** Final project due
- **Total time:** 10 weeks (70 days)

**Milestones:**

- Weeks 1-3: Research + data pipeline
- Weeks 4-7: Model training & validation
- Weeks 8-10: Results analysis + dashboard + final paper

---

## ✅ Final Checklist (Before You Start Week 1 Work)

- [x] Workspace reorganized (subdirectories created)
- [x] `.gitignore` configured
- [x] Project documentation written
- [ ] Todoist tasks created (run `todoist_setup.py`)
- [ ] GitHub repository initialized
- [ ] Week 1 checklist reviewed
- [ ] Literature search prompts reviewed
- [ ] Calendar blocked for capstone work (4-6 hours/day)

---

## 🎉 You're Ready

The workspace is now professionally organized and optimized for efficient development. All foundational documents are in place.

**Focus this weekend:**

1. Run Todoist script → Get tasks organized
2. Initialize GitHub → Version control your work
3. Find 5-8 papers → Build literature foundation

You've got this! 🚀

---

## Questions or issues?

Reach out via:

- Email: <jrocha@smu.edu>
- SMU advisor (once confirmed)
- Classmates for peer support

**Last Updated:** January 10, 2026  
**Next Review:** January 17, 2026 (after Draft 0 submission)
