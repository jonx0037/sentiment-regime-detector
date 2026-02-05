# Archive Directory

This directory contains historical development artifacts that are no longer actively used but preserved for reference.

## Structure

### `/dev-sessions-jan-feb-2026/`

Development session logs from January-February 2026 documenting:
- Daily work sessions (morning/afternoon/evening notes)
- Processing plans (HPC batch processing, data pipelines)
- Progress summaries and implementation tracking
- Final submission checklists

**Why Archived:** These session notes served their purpose during active development but cluttered the root directory. They're preserved here for historical context and retrospective analysis.

**Files:**
- `MORNING_SESSION_FEB3.md` - Latest session (Feb 3, 2026)
- `AFTERNOON_SESSION_FEB2.md` - Afternoon work log (Feb 2, 2026)
- `EVENING_SESSION_FEB2.md` - Evening session (Feb 2, 2026)
- `MORNING_SESSION_FEB2_SUMMARY.md` - Morning summary (Feb 2, 2026)
- `EVENING_SESSION_FEB1_SUMMARY.md` - Evening summary (Feb 1, 2026)
- `AFTERNOON_SESSION_FEB1_PROCESSING_PLAN.md` - Processing plan (Feb 1, 2026)
- `HPC_PROCESSING_PLAN_FEB1.md` - HPC-specific plan (Feb 1, 2026)
- `EVENING_SESSION_JAN31_PART2.md` - Split session (Jan 31, 2026)
- `FINAL_SUBMISSION_CHECKLIST_JAN_12.md` - Early submission checklist (Jan 12, 2026)
- `IMPLEMENTATION_PROGRESS.md` - Overall progress tracking

## Accessing Archived Content

To search across archived session logs:

```bash
# Search for specific topics
grep -r "sentiment analysis" archive/dev-sessions-jan-feb-2026/

# Find when a feature was discussed
grep -r "GARCH model" archive/dev-sessions-jan-feb-2026/

# View chronological development
ls -ltr archive/dev-sessions-jan-feb-2026/
```

## Archive Policy

**What Gets Archived:**
- Session logs older than 1 week
- Outdated planning documents
- Historical progress trackers
- Deprecated documentation
- Old configuration examples

**What Stays Active:**
- Current README.md
- Active documentation in `/docs/`
- Code and tests
- Configuration files in use

---

*Archive created: February 2026 during workspace audit and cleanup*
