# 🛠️ Platform Notes & Search Strategies

Notes on how each platform works and tips specific to finding remote DE roles from India.

---

## LinkedIn

**Best for**: Volume, recruiter inbound, network referrals

**Search filters**:
- Job type: Remote
- Keywords: `Data Engineer` + `Spark` or `dbt` or `Airflow`
- Date posted: Past 24 hours (apply fast!)
- Location: Worldwide / Remote

**X-Ray search**:
```
site:linkedin.com/jobs "data engineer" "remote" "worldwide" -"US only" -"W-2"
```

**Tips**:
- Headline: `Data Engineer | Spark · dbt · Airflow | Open to Remote Worldwide`
- Turn on Open to Work (recruiter-only visibility)
- Post 1–2x/week to boost algorithmic visibility

---

## Turing.com

**Best for**: Passive matching, India-optimized pipeline

**Process**: Apply once → take skill assessments → get matched to US companies

**Tips**:
- Complete all assessments (Python, SQL, System Design)
- Keep profile up to date — recruiters browse it

---

## Toptal

**Best for**: Premium rates ($80–150/hr), consistent work once in

**Process**: 3-stage vetting (English → Coding → Live project)
- ~3% acceptance rate — worth the effort

**Tips**:
- Practice on LeetCode Medium before applying
- Prepare a strong 15-min project walkthrough

---

## We Work Remotely

**Best for**: Curated remote-only postings

**URL**: https://weworkremotely.com/categories/remote-data-science-jobs

**Tips**:
- Check daily — postings move fast
- Filter for "Worldwide" not "USA only"

---

## Wellfound (AngelList Talent)

**Best for**: Startups, equity upside, flexible culture

**Search**: Remote → Data Engineer → Full-time

**Tips**:
- Startups are more timezone-flexible than enterprises
- Equity can be valuable if company-stage is right

---

## Greenhouse / Lever (Direct Company Boards)

**Best for**: Bypassing aggregators, faster response

**Google search**:
```
site:greenhouse.io "data engineer" "remote" -"US only"
site:jobs.lever.co "data engineer" "remote" "async"
```

---

## Communities & Networking

| Community | Platform | Link |
|-----------|----------|-------|
| dbt Community | Slack | getdbt.com/community |
| Data Talks Club | Slack | datatalks.club |
| Seattle Data Guy | Discord | — |
| DataCouncil | Forum | datacouncil.ai |
| Locally Optimistic | Slack | locallyoptimistic.com |

---

## 🔍 Master X-Ray Search Queries

> Paste these directly into Google. Tweak the role/stack terms as needed.

---

### LinkedIn Jobs

```
site:linkedin.com/jobs "data engineer" "remote" "worldwide"
```
```
site:linkedin.com/jobs "data engineer" "remote" -"US only" -"United States only"
```
```
site:linkedin.com/jobs "senior data engineer" "remote" "async"
```
```
site:linkedin.com/jobs "data engineer" "dbt" "remote" "worldwide"
```
```
site:linkedin.com/jobs "data engineer" "spark" "remote" -"W-2"
```
```
site:linkedin.com/jobs "data engineer" "airflow" "remote" "APAC"
```
```
site:linkedin.com/jobs "analytics engineer" "remote" "worldwide"
```
```
site:linkedin.com/jobs "data platform engineer" "remote" "worldwide"
```

---

### Greenhouse (Company ATS)

```
site:greenhouse.io "data engineer" "remote" "worldwide"
```
```
site:greenhouse.io "data engineer" "remote" -"US only" -"United States"
```
```
site:greenhouse.io "data engineer" "dbt" "remote"
```
```
site:greenhouse.io "data engineer" "spark" "airflow" "remote"
```
```
site:greenhouse.io "analytics engineer" "remote" "worldwide"
```
```
site:greenhouse.io "data engineer" "async" "remote"
```

---

### Lever (Company ATS)

```
site:jobs.lever.co "data engineer" "remote" "worldwide"
```
```
site:jobs.lever.co "data engineer" "remote" "async"
```
```
site:jobs.lever.co "data engineer" "remote" -"US only"
```
```
site:jobs.lever.co "analytics engineer" "remote"
```
```
site:jobs.lever.co "data engineer" "dbt" OR "spark" "remote"
```

---

### Ashby (Growing ATS used by modern startups)

```
site:jobs.ashbyhq.com "data engineer" "remote"
```
```
site:jobs.ashbyhq.com "data engineer" "remote" "worldwide"
```
```
site:jobs.ashbyhq.com "analytics engineer" "remote"
```

---

### Workable

```
site:apply.workable.com "data engineer" "remote" "worldwide"
```
```
site:apply.workable.com "data engineer" "remote" -"US only"
```

---

### We Work Remotely

```
site:weworkremotely.com "data engineer"
```
```
site:weworkremotely.com "analytics engineer"
```

---

### Remote.co

```
site:remote.co "data engineer" "worldwide"
```
```
site:remote.co "data engineer" -"US only"
```

---

### General / Broad (Any Job Board)

```
"data engineer" "remote" "worldwide" "async-first" -"US only" -"W-2"
```
```
"senior data engineer" "remote" "APAC" OR "worldwide" OR "timezone flexible"
```
```
"data engineer" "remote" "India" OR "APAC" "full-time"
```
```
"analytics engineer" "dbt" "remote" "worldwide" -"US only"
```
```
"data platform engineer" "spark" "remote" "worldwide"
```

---

### 💡 Modifier Cheat Sheet

| Intent | Operator | Example |
|--------|----------|---------|
| Must include | `"exact phrase"` | `"worldwide remote"` |
| Exclude | `-"term"` | `-"US only"` |
| Either/or | `OR` | `"APAC" OR "worldwide"` |
| Specific site | `site:` | `site:greenhouse.io` |
| Combine stacks | `"dbt" OR "spark" OR "airflow"` | stack flexibility |

**Exclusions to always add**:
```
-"US only" -"United States only" -"W-2" -"must be based in US" -"Americas only"
```
