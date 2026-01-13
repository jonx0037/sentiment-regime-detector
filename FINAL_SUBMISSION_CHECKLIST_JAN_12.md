# Final Submission Checklist - January 12, 2026

**DEADLINE: 11:59 PM TONIGHT**  
**Status:** ✅ DRAFT COMPLETE - READY FOR FINAL REVIEW

---

## ✅ COMPLETED Items

### Content Requirements

- [x] **Title:** Clear, concise, descriptive
- [x] **Author Information:** Name, email, affiliation formatted correctly
- [x] **Abstract:** 150-200 words with motivation, methods, expected findings (currently 193 words)
- [x] **Introduction:** Problem statement, significance, research goals present
- [x] **Literature Review:**
  - [x] 15 peer-reviewed references cited
  - [x] Covers all key areas (transformers, sentiment analysis, regime detection, spillovers)
  - [x] Research hypotheses clearly stated (4 hypotheses: H1-H4)
  - [x] Gap in literature explicitly identified
- [x] **Methods Section:**
  - [x] Data sources specified (Reddit, Twitter, News APIs)
  - [x] Preprocessing pipeline detailed
  - [x] Model architecture (FinBERT + RoBERTa ensemble) explained
  - [x] Sentiment index construction with mathematical formulation
  - [x] Regime classification approach (RF, XGBoost, LSTM comparison)
  - [x] Dashboard development plan
- [x] **Expected Results:** Performance targets and validation events specified
- [x] **Discussion:** Interpretations, implications, limitations included
- [x] **Conclusion:** Two-paragraph summary of contributions
- [x] **References:** 15 complete APA citations with DOIs where available

### Quality Checks

- [x] **NO placeholder text** - All [NOTE:], [To be completed], [Placeholder] removed
- [x] **Specific metrics cited** - FinBERT 15% accuracy gain, 87.6% prediction accuracy, etc.
- [x] **Academic language** throughout
- [x] **Logical flow** from problem → literature → methods → expected results
- [x] **Citations enhanced** with Scholarcy summary details

---

## 📋 PRE-SUBMISSION Review (Do These NOW)

### Step 1: Content Verification (15 minutes)

- [ ] **Read abstract aloud** - Does it make sense to someone unfamiliar with the project?
- [ ] **Check email addresses** - <jrocha@smu.edu> correct?
- [ ] **Verify advisor status** - "[Searching - TBD]" is acceptable per syllabus
- [ ] **Scan for typos** - Run spellcheck in editor
- [ ] **Check superscripts** - Author affiliation markers (¹) formatted correctly?

### Step 2: Formatting Verification (10 minutes)

- [ ] **Section numbering** - 1, 1.1, 1.2, 2, 2.1, etc. consistent?
- [ ] **References format** - All APA style with author (year)?
- [ ] **Equation formatting** - LaTeX/MathJax renders correctly if viewing as PDF?
- [ ] **Bullet points** - Consistent style (● for main, - for sub)?
- [ ] **Line spacing** - Appropriate for readability?

### Step 3: Template Compliance (5 minutes)

Compare your draft against [ResearchOutlineTemplate.html](course_files/ResearchOutlineTemplate.html):

- [ ] Title section format matches
- [ ] Author/affiliation format matches
- [ ] Section headers match expected structure
- [ ] Reference format consistent with template

### Step 4: Final Export (5 minutes)

- [ ] **Choose format:** PDF recommended (preserves formatting)

  ```bash
  # If using Markdown to PDF converter:
  pandoc dev/research/draft-0.md -o "Rocha_ResearchOutline_Jan12_2026.pdf" \
    --pdf-engine=xelatex --variable geometry:margin=1in
  ```

- [ ] **Filename:** Follow syllabus convention (LastName_Assignment_Date format)
- [ ] **Test open:** Can you open and view the exported file correctly?

---

## 📤 SUBMISSION Instructions

### Where to Submit

Check your course Canvas/Blackboard for the exact submission portal. Typical locations:

- Canvas: Assignments → "Week 1: Research Outline"
- Email: If no portal, email to instructor with subject: "DS 6210 - Research Outline - Jonathan Rocha"

### What to Include

1. **Research Outline Document** (PDF or DOCX)
2. **Group Information** (if applicable - you're solo, note: "Individual project")
3. **Advisor Status:** "Faculty advisor search in progress - will be finalized by Week 2"

### Submission Notes

```text
Student: Jonathan Rocha (jrocha@smu.edu)
Project: Cross-Asset Sentiment Regime Detector
GitHub: github.com/jonx0037/sentiment-regime-detector
Advisor: Searching (TBD by Week 2 per syllabus allowance)
Group: Individual project
```

---

## 🎯 Quality Indicators

Your draft-0 now includes:

- ✅ **193-word abstract** (target: 150-200) ✓
- ✅ **15 peer-reviewed references** (minimum: 5-8 for Draft 0) ✓✓
- ✅ **4 explicit hypotheses** (H1-H4 with specific predictions)
- ✅ **Specific methodological details** (FinBERT + RoBERTa ensemble, 16 features)
- ✅ **Concrete metrics** (15% accuracy gain, 1-5 day lead time, 22.53% returns)
- ✅ **Enhanced citations** from Scholarcy summaries (vs. generic descriptions)
- ✅ **Complete sections** (no placeholders remaining)

---

## ⏰ Timeline for Tonight

**6:00 PM - 7:00 PM:** Final review (Steps 1-3 above)  
**7:00 PM - 7:30 PM:** Export to PDF and verify formatting  
**7:30 PM - 8:00 PM:** Upload to submission portal  
**8:00 PM - 11:59 PM:** Buffer time (keep for emergencies)

**Recommended:** Submit by 9:00 PM to avoid last-minute technical issues.

---

## 🚀 POST-SUBMISSION (January 13+)

After submitting tonight:

1. **Celebrate!** 🎉 You've completed Week 1's major deliverable
2. **Continue advisor search** - Email 2-3 potential advisors tomorrow
3. **Start MANEFRAME access request** - Draft email to <help@smu.edu>
4. **Review Week 2 tasks** - Literature review refinement and data pipeline planning

---

## 📞 Emergency Contacts

- **SMU IT Help:** <help@smu.edu> (for submission portal issues)
- **Course Instructor:** [Check syllabus for email/office hours]
- **Technical Issues:** Document error with screenshots, email instructor immediately

---

**GOOD LUCK!** Your draft is comprehensive, well-researched, and ready for submission. 💪
