# 🎯 Harsha's Professional Playbook

> A living career repository — where every lesson learned, interview survived, and milestone reached is stored, refined, and built upon.

This is my personal knowledge base and career archive. Everything I accumulate over my career as a Data Engineer — the hard interview questions, the problems that tripped me up, the systems I designed, the resumes I refined — lives here.

---

## 🧭 What This Repo Is For

| Purpose | Description |
|---|---|
| 📚 **Learning & Mastery** | Deep-dive notes, cheatsheets, and examples across all Data Engineering domains |
| 🎤 **Interview Readiness** | Real coding problems, question logs, and prep notes from actual interviews |
| 📄 **Career Assets** | Polished resumes in multiple formats, tailored for different roles and markets |
| 🏗️ **Long-Term Reference** | A handbook I can return to 5 years from now and still find value in |

---

## 📁 Repository Structure

```text
harsha-professional-playbook/
│
├── README.md                        ← You are here
│
├── de_playbook/                     ← 📚 Complete DE knowledge base
│   ├── README.md                    ← Module index + study schedule
│   ├── MASTER_TRACKER.md            ← Daily progress log
│   ├── 01_SQL/                      ← SQL mastery (7 topics)
│   ├── 02_Python/                   ← Python for DE (8 topics)
│   ├── 03_PySpark/                  ← PySpark & optimization (6 topics)
│   ├── 04_Data_Warehousing/         ← DWH concepts & patterns (5 topics)
│   ├── 05_dbt/                      ← dbt fundamentals to project (5 topics)
│   ├── 06_Databricks/               ← Delta Lake & Lakehouse (5 topics)
│   ├── 07_Kafka_Streaming/          ← Streaming & real-time (4 topics)
│   └── 08_Interview_Prep/           ← Cheatsheets + behavioral stories
│
├── job_hunt/                        ← 🎯 Job search command center
│   ├── freelance/
│   │   └── README.md                ← 32 freelance platforms tracker
│   ├── full_time/
│   │   ├── india.md                 ← 21 India job boards
│   │   ├── remote.md                ← 30 remote job boards (India & intl)
│   │   └── international.md         ← 49 intl boards (Gulf, EU, US, APAC)
│   └── Resume/                      ← Career documents
│       ├── full_time/               ← Full-time role resumes
│       ├── freelance/               ← Freelance / consulting resumes
│       └── reference_resumes/       ← Source-of-truth resumes (MD + PDF)
│
└── interview_experiences/           ← 🎤 Real problems from real interviews
    └── Mine/
        ├── zluri/                   ← Zluri (2 rounds)
        ├── go_daddy/                ← GoDaddy
        ├── globant/
        ├── hilabs/
        ├── purplesquare_ai/
        ├── global_logic/
        └── hacker_rank/
```

---

## 📚 DE Playbook

The [`de_playbook/`](./de_playbook/) folder is the core of this repo — a structured, session-by-session knowledge base built while actively preparing for Senior Data Engineer roles.

### 🗓️ 8-Week Study Plan

| Week | Module | Goal |
|---|---|---|
| Week 1 | **SQL** | Solve any SQL interview question cold |
| Week 2 | **Python** | Write production-grade DE code |
| Week 3 | **PySpark** | Optimize Spark jobs, ace PySpark rounds |
| Week 4 | **Data Warehousing + dbt** | Design warehouses, build dbt models |
| Week 5 | **Databricks** | Build medallion pipelines, explain Delta Lake |
| Week 6 | **Kafka + Streaming** | Explain guarantees, build a real pipeline |
| Week 7–8 | **Mock Interviews** | Full loop simulations, offers |

### 📄 How Every Topic Is Structured

```text
topic_name/
├── notes.md         ← theory + cheatsheet (written while learning)
├── practice.sql/.py ← runnable exercises with solutions
└── interview.md     ← Q&A with model answers + follow-ups
```

### 🧱 Non-Negotiables for Senior DE Roles

- **SQL:** Window Functions, CTEs, Analytical Patterns, Execution Order
- **Python:** OOP, Generators, Decorators, Multithreading
- **PySpark:** Shuffles, Partitioning, Broadcast Joins, Optimization
- **Data Warehouse:** CDC, SCD Type 2, Incremental Loads, Fact vs Dimension
- **Streaming:** Kafka, Watermarks, Exactly-once vs At-least-once
- **Modern Stack:** dbt, Databricks, Delta Lake, Medallion Architecture

---

## 💼 Job Hunt Hub

The [`job_hunt/`](./job_hunt/) folder is the command center for all job search activity — freelance platforms, full-time job boards, and resumes, all in one place.

| File | What's Inside | # of Sites |
|---|---|---|
| [`freelance/README.md`](./job_hunt/freelance/README.md) | All freelance platforms for DE consulting work | 32 |
| [`full_time/india.md`](./job_hunt/full_time/india.md) | India-specific job boards (Naukri, Instahyre, Cutshort, etc.) | 21 |
| [`full_time/remote.md`](./job_hunt/full_time/remote.md) | Remote jobs — India & International (YC, Remotive, Arc, etc.) | 30 |
| [`full_time/international.md`](./job_hunt/full_time/international.md) | Gulf, Europe, US, APAC boards + relocation platforms | 49 |
| [`Resume/`](./job_hunt/Resume/) | All resume versions (full-time, freelance, reference) | — |


> Each file has editable columns for `My Profile/Dashboard` links and `Status` tracking so you can manage everything from these files.

---

## 📚 Data Engineering Roadmap

The [`data_engineering_roadmap/`](./data_engineering_roadmap/README.md) folder is a structured, self-paced curriculum covering everything needed to crack Senior & Staff Data Engineer roles.

### 🗺️ Learning Phases

| Phase | Topic | Goal |
|---|---|---|
| 1 | **SQL Mastery** | Solve any SQL interview question confidently |
| 2 | **Python Mastery** | Write production-grade data engineering code |
| 3 | **PySpark Mastery** | Handle TB-scale datasets efficiently |
| 4 | **Data Engineering Platform** | Build production-grade pipelines (Airflow, dbt) |
| 5 | **Data Warehouse & Modeling** | Design enterprise data warehouses |
| 6 | **Streaming** | Build real-time pipelines (Kafka, Pub/Sub) |
| 7 | **Cloud** | GCP · AWS · Azure — become platform agnostic |
| 8 | **Performance Optimization** | Diagnose and fix bottlenecks at scale |
| 9 | **System Design** | Clear Senior & Staff Engineer design rounds |

### 🧱 Non-Negotiables for Senior Roles

- **SQL:** Window Functions, CTEs, Analytical Patterns, Execution Order
- **Python:** OOP, Generators, Decorators, Multithreading
- **PySpark:** Shuffles, Partitioning, Broadcast Joins, Optimization
- **Data Warehouse:** CDC, SCD Type 2, Incremental Loads, Fact vs Dimension
- **Streaming:** Kafka, Watermarks, Exactly-once vs At-least-once
- **Cloud:** BigQuery, Redshift, Databricks, Cloud IAM
- **System Design:** Batch vs Streaming, Lakehouse, Medallion Architecture

---

## 🎤 Interview Experiences

The [`interview_experiences/Mine/`](./interview_experiences/Mine/) folder stores real problems I encountered during interviews — with my solutions, notes, and learnings.

> Each company folder contains Python files (e.g., `r1.py`, `r2.py`) representing individual rounds.

| Company | Rounds Logged |
|---|---|
| Zluri | 2 |
| GoDaddy | 1 |
| Globant | 1 |
| HiLabs | 2 |
| PurpleSquare AI | 2 |
| GlobalLogic | 1 |
| HackerRank | 1 |

### 🔑 Problem Types Encountered

- **Bucket Sort / Frequency Counting** (Top K elements — Zluri R1)
- **Anagram Grouping** (GoDaddy R1)
- **Sliding Window / Hash Maps** (HiLabs)
- **Data Engineering design questions** (GlobalLogic)

---

## 📄 Resume

The [`job_hunt/Resume/`](./job_hunt/Resume/) folder contains all versions of my resume, tailored for different contexts.

### 📂 Layout

| Folder | Contents |
|---|---|
| `full_time/` | Resume for full-time DE roles |
| `freelance/` | Upwork & platform-optimized resumes |
| `reference_resumes/` | Master copies — Markdown source + PDFs |

### 👤 My Profile (from resume)

**Harshavardhan Raja — Senior Data Engineer | Cloud & Data Platforms**

- 6+ years of experience in large-scale production data platforms
- Core expertise: Python, SQL, Apache Airflow, PySpark, MongoDB, Snowflake, BigQuery, AWS, GCP
- Built multi-tenant lakehouse platforms, high-volume ETL pipelines, real-time IoT ingestion systems
- **Certifications:** Google Cloud Professional Data Engineer · Google Cloud Professional Cloud Architect
- **Education:** B.Tech – Chemical Science & Technology, IIT Guwahati (2019)
- **Recognition:** Sequoia BackPack Award (2025) · BBI Core Value Award (Q3 2023) · Virtusa Top Talent

---

## 🚀 Career Timeline

```text
Jul 2019 – Dec 2021   →  Associate Consultant – Cloud Data Engineer @ Virtusa
Dec 2021 – May 2024   →  Senior Associate – Cloud Data Engineer @ BlackBuck Insights
Sep 2024 – Apr 2026   →  Senior Data Engineer @ Sequoia
2026+                 →  Next chapter... (this repo will document the journey)
```

---

## 💡 How I Use This Repo

1. **Every morning** → Open [`job_hunt/`](./job_hunt/) trackers, click dashboard links, check for new opportunities
2. **After every interview** → Add the problems I faced to the relevant company folder under `interview_experiences/`
3. **While preparing** → Work through the roadmap phases in `data_engineering_roadmap/`, filling in notes and examples
4. **When applying** → Pull from [`job_hunt/Resume/`](./job_hunt/Resume/) and tailor for the role
5. **Weekly** → Update platform statuses, re-order sites based on results
6. **For long-term growth** → Come back and see how my thinking has evolved

---

## 📌 Guiding Philosophy

> *"Every interview is a data point. Every problem is a lesson. Every rejection is a redirect."*

This repo is not just prep material — it's a professional journal. The goal is to walk into every room feeling like the most prepared person there, backed by documented evidence of growth.

---

*Last updated: August 2026 · Built and maintained by [Harshavardhan Raja](https://linkedin.com/in/harshavardhan-raja)*
