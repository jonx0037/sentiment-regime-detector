#!/usr/bin/env python3
"""
Todoist Project Setup Automation Script
Automatically creates tasks for the Capstone project timeline

Requirements:
    pip install todoist-api-python

Usage:
    1. Get your API token from: https://todoist.com/prefs/integrations
    2. Set environment variable: export TODOIST_API_TOKEN="your_token_here"
    3. Run: python todoist_setup.py
"""

import os
import sys
import importlib
from datetime import datetime, timedelta


def _load_todoist_api_class():
    """Load TodoistAPI without a hard import so linters/type checkers don't fail when
    the optional dependency isn't installed in the current environment.

    Returns:
        (TodoistAPI_class, error) where TodoistAPI_class is callable or None.
    """
    try:
        module = importlib.import_module("todoist_api_python.api")
    except ModuleNotFoundError as e:
        return None, e

    todoist_api_class = getattr(module, "TodoistAPI", None)
    if todoist_api_class is None:
        return None, AttributeError("Module 'todoist_api_python.api' has no attribute 'TodoistAPI'")

    return todoist_api_class, None


def _load_todoist_error_class():
    """Best-effort load of TodoistError without a hard dependency.

    Returns:
        TodoistError class or None.
    """
    candidates = [
        ("todoist_api_python.api", "TodoistError"),
        ("todoist_api_python.http_requests", "TodoistError"),
    ]
    for module_name, attr_name in candidates:
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        error_cls = getattr(module, attr_name, None)
        if error_cls is not None:
            return error_cls
    return None

# Project timeline configuration
PROJECT_NAME = "SMU Capstone - Sentiment Regime Detector"
START_DATE = datetime(2026, 1, 10)
END_DATE = datetime(2026, 3, 20)


def get_date_string(days_from_start):
    """Convert days from start to ISO date string."""
    target_date = START_DATE + timedelta(days=days_from_start)
    return target_date.strftime("%Y-%m-%d")


def create_project_structure(api):
    """Create the main project and all tasks."""
    
    TodoistError = _load_todoist_error_class() or RuntimeError

    try:
        # Create main project
        print(f"Creating project: {PROJECT_NAME}")
        project = api.add_project(name=PROJECT_NAME)
        project_id = project.id
        print(f"✓ Project created with ID: {project_id}")
        
        # Define sections and tasks
        sections = {
            "Week 1: Draft 0 & Setup (Jan 10-17)": [
                {
                    "content": "Complete literature review expansion (5-8 key papers)",
                    "description": "Find papers on: cross-asset sentiment, transformer models in finance, regime detection, social media sentiment predictive power",
                    "due_string": "Jan 15",
                    "priority": 4,  # p1 = highest
                },
                {
                    "content": "Finalize methods section in Draft 0",
                    "description": "Detail data collection methodology, sentiment model architecture, regime classification approach",
                    "due_string": "Jan 16",
                    "priority": 4,
                },
                {
                    "content": "Complete abstract and introduction revisions",
                    "description": "Ensure abstract is 150-200 words, introduction clearly states problem/gap/contribution",
                    "due_string": "Jan 17",
                    "priority": 4,
                },
                {
                    "content": "Set up GitHub repository (public)",
                    "description": "Initialize repo, add .gitignore, create branch structure (main/develop), push initial code",
                    "due_string": "Jan 12",
                    "priority": 3,
                },
                {
                    "content": "Request MANEFRAME HPC access",
                    "description": "Email help@smu.edu with proposal, GPU node request, estimate 50-100 GPU hours",
                    "due_string": "Jan 13",
                    "priority": 3,
                },
                {
                    "content": "Finalize faculty advisor",
                    "description": "Identify advisor with NLP/transformer expertise, send formal request email",
                    "due_string": "Jan 14",
                    "priority": 3,
                },
            ],
            "Weeks 2-3: Data Collection Pipeline (Jan 20-31)": [
                {
                    "content": "Set up Reddit API access (PRAW + Pushshift)",
                    "description": "Register Reddit app, get credentials, test API access on r/wallstreetbets",
                    "due_string": "Jan 21",
                    "priority": 3,
                },
                {
                    "content": "Set up Twitter/X API access",
                    "description": "Apply for Academic Research access or use Apify scraper alternative",
                    "due_string": "Jan 22",
                    "priority": 3,
                },
                {
                    "content": "Set up NewsAPI or financial news scraper",
                    "description": "Register NewsAPI key or build BeautifulSoup scraper for Bloomberg/Reuters",
                    "due_string": "Jan 23",
                    "priority": 3,
                },
                {
                    "content": "Build data collection pipeline",
                    "description": "Create unified pipeline that collects from all sources, stores in PostgreSQL/CSV",
                    "due_string": "Jan 28",
                    "priority": 4,
                },
                {
                    "content": "Collect historical data (2020-present)",
                    "description": "Run pipeline to gather ~1-2M samples across all asset classes",
                    "due_string": "Jan 31",
                    "priority": 4,
                },
            ],
            "Week 4: EDA & Data Preprocessing (Feb 3-7)": [
                {
                    "content": "Exploratory data analysis (EDA)",
                    "description": "Analyze text lengths, source distribution, temporal patterns, identify data quality issues",
                    "due_string": "Feb 5",
                    "priority": 3,
                },
                {
                    "content": "Data cleaning and preprocessing pipeline",
                    "description": "Remove duplicates, filter spam/bots, tokenize text, create train/val/test splits",
                    "due_string": "Feb 7",
                    "priority": 4,
                },
            ],
            "Weeks 5-6: Sentiment Model Training (Feb 10-21)": [
                {
                    "content": "Set up MANEFRAME training environment",
                    "description": "Create conda env, install transformers/torch, test GPU access with simple training run",
                    "due_string": "Feb 11",
                    "priority": 4,
                },
                {
                    "content": "Fine-tune FinBERT on financial social media data",
                    "description": "Transfer learn FinBERT on Reddit/Twitter data, validate on held-out test set",
                    "due_string": "Feb 17",
                    "priority": 4,
                },
                {
                    "content": "Train RoBERTa ensemble model",
                    "description": "Fine-tune RoBERTa as second model, create ensemble prediction system",
                    "due_string": "Feb 21",
                    "priority": 4,
                },
            ],
            "Week 7: Sentiment Indices & Feature Engineering (Feb 24-28)": [
                {
                    "content": "Build asset-class-specific sentiment indices",
                    "description": "Aggregate sentiment by asset class (equity/crypto/forex/commodity), create daily/weekly indices",
                    "due_string": "Feb 26",
                    "priority": 4,
                },
                {
                    "content": "Feature engineering for regime detection",
                    "description": "Create features: sentiment momentum, cross-asset divergence, volatility metrics, rolling correlations",
                    "due_string": "Feb 28",
                    "priority": 4,
                },
            ],
            "Weeks 8-9: Regime Classification Model (Mar 3-14)": [
                {
                    "content": "Label historical regime states",
                    "description": "Manually label Risk-On/Risk-Off/Transition periods using VIX, market performance, major events",
                    "due_string": "Mar 5",
                    "priority": 4,
                },
                {
                    "content": "Train regime classification model",
                    "description": "Test Random Forest, XGBoost, LSTM models; optimize hyperparameters; select best performer",
                    "due_string": "Mar 10",
                    "priority": 4,
                },
                {
                    "content": "Backtesting and validation",
                    "description": "Validate against COVID crash (2020), 2022 bear market, crypto winter; measure lead time accuracy",
                    "due_string": "Mar 14",
                    "priority": 4,
                },
            ],
            "Week 10: Dashboard & Final Deliverables (Mar 17-20)": [
                {
                    "content": "Build React dashboard frontend",
                    "description": "Create real-time sentiment charts (Recharts), regime indicator, divergence alerts, historical view",
                    "due_string": "Mar 18",
                    "priority": 4,
                },
                {
                    "content": "Deploy app to GitHub Pages (or Vercel/Netlify)",
                    "description": "Configure deployment pipeline, test production build, ensure API integration works",
                    "due_string": "Mar 19",
                    "priority": 4,
                },
                {
                    "content": "Finalize Draft 1 paper (MSDS Journal format)",
                    "description": "Complete all sections (intro, methods, results, discussion), format per template, proofread",
                    "due_string": "Mar 19",
                    "priority": 4,
                },
                {
                    "content": "Prepare final presentation slides",
                    "description": "Create poster/slides using SMU template, practice 10-minute presentation",
                    "due_string": "Mar 20",
                    "priority": 3,
                },
                {
                    "content": "Submit final project deliverables",
                    "description": "Submit paper, GitHub repo link, deployed app URL, presentation materials",
                    "due_string": "Mar 20",
                    "priority": 4,
                },
            ],
        }
        
        # Create sections and tasks
        for section_name, tasks in sections.items():
            print(f"\nCreating section: {section_name}")
            section = api.add_section(name=section_name, project_id=project_id)
            section_id = section.id
            print(f"  ✓ Section created with ID: {section_id}")
            
            for task_data in tasks:
                api.add_task(
                    content=task_data["content"],
                    description=task_data.get("description", ""),
                    project_id=project_id,
                    section_id=section_id,
                    due_string=task_data.get("due_string"),
                    priority=task_data.get("priority", 3),
                )
                print(f"    ✓ Task created: {task_data['content']}")
        
        print(f"\n{'='*60}")
        print("✅ Project setup complete!")
        print(f"{'='*60}")
        print(f"Project URL: https://todoist.com/app/project/{project_id}")
        print(f"Total tasks created: {sum(len(tasks) for tasks in sections.values())}")
        
    except TodoistError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except (ValueError, TypeError) as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(130)


def main():
    """Main execution function."""
    print(f"\n{'='*60}")
    print("Todoist Project Setup - SMU Capstone")
    print(f"{'='*60}\n")
    
    # Get API token from environment
    api_token = os.getenv("TODOIST_API_TOKEN")
    
    if not api_token:
        print("❌ Error: TODOIST_API_TOKEN environment variable not set")
        print("\nInstructions:")
        print("1. Get your API token: https://todoist.com/prefs/integrations")
        print("2. Export it: export TODOIST_API_TOKEN='your_token_here'")
        print("3. Run this script again\n")
        sys.exit(1)

    # Load optional dependency
    TodoistAPI, import_err = _load_todoist_api_class()
    if TodoistAPI is None:
        print("❌ Error: Missing dependency 'todoist-api-python' (todoist_api_python)")
        print("\nInstall it with:")
        print("  python -m pip install todoist-api-python\n")
        if import_err:
            print(f"Details: {import_err}\n")
        sys.exit(1)
    
    # Initialize API
    TodoistError = _load_todoist_error_class() or RuntimeError
    try:
        api = TodoistAPI(api_token)
        print("✓ Connected to Todoist API\n")
    except TodoistError as e:
        print(f"❌ Failed to connect to Todoist API: {e}\n")
        sys.exit(1)
    except (ValueError, TypeError) as e:
        print(f"❌ Failed to initialize Todoist API client: {e}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user\n")
        sys.exit(130)
    
    # Create project structure
    create_project_structure(api)


if __name__ == "__main__":
    main()
