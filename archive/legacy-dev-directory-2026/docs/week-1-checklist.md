# Week 1 Checklist: Draft 0 & Setup

**Due:** January 17, 2026 (Friday)

## Priority 1: Draft 0 Completion

### Literature Review (DUE: Wed Jan 15)

- [ ] Find 5-8 high-quality papers on:
  - [ ] Cross-asset sentiment analysis (2-3 papers)
  - [ ] Transformer models in financial NLP (2-3 papers)
  - [ ] Market regime detection methods (2-3 papers)
  - [ ] Social media as predictive signal (1-2 papers)
- [ ] Read and annotate each paper (key findings, methodology, gaps)
- [ ] Update [draft-0.md](research/draft-0.md) Section 2 with proper APA citations
- [ ] Ensure each subsection (2.1-2.5) has 3-4 references minimum

### Methods Section (DUE: Thu Jan 16)

- [ ] Complete Section 3.1: Data Collection
  - [ ] Specify exact subreddits, Twitter hashtags, news sources
  - [ ] Define filtering criteria (language, spam detection, duplicates)
  - [ ] Clarify storage format (PostgreSQL schema vs. CSV)
- [ ] Complete Section 3.2: Sentiment Model Architecture
  - [ ] Detail FinBERT fine-tuning process
  - [ ] Explain RoBERTa ensemble methodology
  - [ ] Define evaluation metrics (F1, precision, recall)
- [ ] Complete Section 3.3: Regime Classification
  - [ ] Define Risk-On/Risk-Off/Transition labels
  - [ ] Explain feature engineering approach
  - [ ] Justify model selection (RF vs. XGBoost vs. LSTM)
- [ ] Complete Section 3.4: Validation Strategy
  - [ ] Define backtesting methodology
  - [ ] Select historical events for validation (COVID crash, 2022 bear market, etc.)

### Abstract & Introduction (DUE: Fri Jan 17)

- [ ] Revise abstract to 150-200 words (currently ~140)
  - [ ] Add expected results/findings sentence
  - [ ] Clarify practical implications
- [ ] Strengthen introduction
  - [ ] Expand "Motivation" with 1-2 concrete examples (GameStop squeeze, COVID crash)
  - [ ] Clarify the specific gap in literature
  - [ ] Sharpen research questions/hypotheses

### Final Draft 0 Polish (DUE: Fri Jan 17)

- [ ] Proofread entire document
- [ ] Ensure all placeholder text is removed (search for "[NOTE:", "[To be completed")
- [ ] Verify APA citation format
- [ ] Check that figures/tables have captions (if any)
- [ ] Save as PDF for submission (if required)

---

## Priority 2: Project Setup

### GitHub Repository (DUE: Sun Jan 12)

- [x] Create public repository: `sentiment-regime-detector`
- [x] Repository created at: github.com/jonx0037/sentiment-regime-detector
- [x] Push initial commit with current workspace structure
- [x] Add README.md to repo root
- [ ] Create `develop` branch for active development
- [ ] Add GitHub repo link to Todoist project

### MANEFRAME Access (DUE: Mon Jan 13)

- [ ] Draft email to <help@smu.edu>:
  - [ ] Attach project proposal
  - [ ] Request GPU node access (A100 or V100)
  - [ ] Estimate compute needs: 50-100 GPU hours
  - [ ] Mention advisor (once confirmed)
- [ ] Send email
- [ ] Follow up if no response within 48 hours

### Advisor Finalization (DUE: Tue Jan 14)

- [ ] Identify 3 potential advisors (NLP/finance ML expertise)
  - [ ] Check SMU Lyle faculty directory
  - [ ] Review recent publications on Google Scholar
- [ ] Draft formal advisor request email:
  - [ ] Brief project summary (2-3 paragraphs)
  - [ ] Mention timeline (Mar 20 completion)
  - [ ] Attach proposal PDF
- [ ] Send to top choice, wait 48 hours before reaching out to backup

### Todoist Setup (DUE: Sat Jan 11)

- [ ] Get Todoist API token: <https://todoist.com/prefs/integrations>
- [ ] Install `todoist-api-python`: `pip install todoist-api-python`
- [ ] Run automation script:

```bash
export TODOIST_API_TOKEN="your_token_here"
python dev/code/todoist_setup.py
```

- [ ] Review generated tasks in Todoist app
- [ ] Adjust due dates if needed

---

## Optional (Time Permitting)

### Data Pipeline Preview

- [ ] Register Reddit API credentials (takes 5 minutes)
- [ ] Test PRAW connection with simple script:

```python
import praw
reddit = praw.Reddit(client_id="...", client_secret="...", user_agent="...")
posts = reddit.subreddit("wallstreetbets").hot(limit=10)
for post in posts:
print(post.title)
```

- [ ] Estimate data collection time for 2016-present

### Literature Organization

- [ ] Create Zotero/Mendeley library for reference management
- [ ] Export .bib file for LaTeX integration (future)
- [ ] Tag papers by theme (sentiment/regime/NLP/data)

---

## Daily Time Allocation (Week 1)

| Day            | Focus Area                             | Estimated Hours |
| -------------- | -------------------------------------- | --------------- |
| **Sat Jan 11** | Setup (GitHub, Todoist, workspace org) | 3-4 hours       |
| **Sun Jan 12** | Literature search (find 5-8 papers)    | 4-5 hours       |
| **Mon Jan 13** | Read papers, MANEFRAME/advisor emails  | 5-6 hours       |
| **Tue Jan 14** | Draft literature review section        | 5-6 hours       |
| **Wed Jan 15** | Complete methods section               | 5-6 hours       |
| **Thu Jan 16** | Revise abstract/intro                  | 3-4 hours       |
| **Fri Jan 17** | Final proofreading & submission        | 2-3 hours       |

**Total:** ~30 hours

---

## Success Criteria

✅ **Draft 0 is "complete" if:**

- Abstract is 150-200 words, clear, no placeholders
- Introduction states problem, gap, contribution
- Literature review has 12-20 citations (3-4 per subsection)
- Methods section describes all 4 components (data, sentiment, regime, validation)
- No "[NOTE:" or "[To be completed]" placeholders remain
- Document is APA-formatted and proofread

✅ **Setup is "complete" if:**

- GitHub repo is live with initial code
- Todoist tasks are created and organized
- MANEFRAME access request is sent
- Advisor request is sent

---

## Blockers & Contingencies

| Potential Blocker                  | Contingency Plan                                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Can't find 5-8 papers              | Use Google Scholar alerts, ask advisor for suggestions, check arXiv preprints                           |
| MANEFRAME access delayed           | Start data collection on local machine, use Google Colab Pro ($10/month) for initial experiments        |
| No advisor response                | Reach out to 2nd choice after 48 hours, escalate to program director if needed                          |
| Draft 0 takes longer than expected | Focus on abstract + methods (most critical sections), defer some literature review expansion to Week 2  |

---

**Notes:**

- Update this checklist daily as you complete items
- Use Todoist for granular task tracking (this is high-level overview)
- Don't let perfect be the enemy of good—Draft 0 is meant to be iterative
