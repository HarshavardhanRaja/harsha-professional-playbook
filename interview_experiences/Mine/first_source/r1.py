"""
====================================================================
PROBLEM: SESSION ANALYSIS (SESSIONIZATION)
====================================================================

Table: events(visitor_id, event_timestamp, event_name)

Goal: Group events into sessions where a gap of MORE THAN 30 minutes
      between consecutive events starts a NEW session.

Return ONE ROW per session with:
  - visitor_id
  - session_id
  - session_start   (timestamp of first event in session)
  - session_end     (timestamp of last event in session)
  - event_count     (number of events in the session)

====================================================================
APPROACH: 3-Step CTE breakdown
====================================================================

STEP 1 — Calculate the gap between each event and the previous one
         (per visitor, ordered by time)

STEP 2 — Flag the START of a new session
         (first event ever for a visitor, OR gap > 30 min)

STEP 3 — Assign a session_id using a running sum of the new-session flags

STEP 4 — Aggregate to get one row per session

====================================================================
"""

# ---------------------------------------------------------------
# SAMPLE DATA (for mental walkthrough)
# ---------------------------------------------------------------
# visitor_id | event_timestamp        | event_name
# -----------+------------------------+------------
# V1         | 2024-01-01 10:00:00    | page_view
# V1         | 2024-01-01 10:10:00    | click        <- gap 10 min  (same session)
# V1         | 2024-01-01 10:45:00    | page_view    <- gap 35 min  (NEW session)
# V1         | 2024-01-01 10:50:00    | purchase     <- gap 5 min   (same session)
# V2         | 2024-01-01 09:00:00    | page_view
# V2         | 2024-01-01 09:20:00    | click        <- gap 20 min  (same session)
#
# Expected output:
# V1 | session 1 | 10:00 → 10:10 | 2 events
# V1 | session 2 | 10:45 → 10:50 | 2 events
# V2 | session 1 | 09:00 → 09:20 | 2 events
# ---------------------------------------------------------------


SOLUTION_SQL = """

-- ================================================================
-- FULL SOLUTION (works in Snowflake, BigQuery, Postgres, Redshift)
-- ================================================================

WITH

-- STEP 1: Calculate gap from the previous event (per visitor)
step1_with_gap AS (
    SELECT
        visitor_id,
        event_timestamp,
        event_name,
        LAG(event_timestamp) OVER (
            PARTITION BY visitor_id
            ORDER BY event_timestamp
        ) AS prev_event_timestamp
    FROM events
),

-- STEP 2: Flag where a new session starts
--   A new session starts when:
--   (a) It's the first event for this visitor (prev_event_timestamp IS NULL), OR
--   (b) The gap to the previous event is > 30 minutes
step2_session_flag AS (
    SELECT
        visitor_id,
        event_timestamp,
        event_name,
        prev_event_timestamp,

        -- gap in minutes from previous event
        DATEDIFF('minute', prev_event_timestamp, event_timestamp) AS gap_minutes,

        -- 1 = this event STARTS a new session, 0 = continues existing session
        CASE
            WHEN prev_event_timestamp IS NULL THEN 1          -- first event ever
            WHEN DATEDIFF('minute', prev_event_timestamp, event_timestamp) > 30 THEN 1
            ELSE 0
        END AS is_new_session
    FROM step1_with_gap
),

-- STEP 3: Assign session_id using a RUNNING SUM of the new-session flags
--   Cumulative sum of is_new_session gives a unique, incrementing ID
--   per visitor each time a new session starts
step3_session_id AS (
    SELECT
        visitor_id,
        event_timestamp,
        event_name,
        gap_minutes,
        is_new_session,

        -- Running sum of new-session flags = session number for this visitor
        SUM(is_new_session) OVER (
            PARTITION BY visitor_id
            ORDER BY event_timestamp
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS session_id
    FROM step2_session_flag
)

-- STEP 4: Aggregate — one row per (visitor, session)
SELECT
    visitor_id,
    session_id,
    MIN(event_timestamp) AS session_start,
    MAX(event_timestamp) AS session_end,
    COUNT(*)             AS event_count,

    -- bonus: session duration in minutes
    DATEDIFF('minute', MIN(event_timestamp), MAX(event_timestamp)) AS session_duration_minutes
FROM step3_session_id
GROUP BY
    visitor_id,
    session_id
ORDER BY
    visitor_id,
    session_id;

"""

# ================================================================
# SNOWFLAKE-SPECIFIC NOTES (relevant for your JD)
# ================================================================
SNOWFLAKE_NOTES = """

1. DATEDIFF('minute', start, end) — Snowflake syntax
   PostgreSQL equivalent: EXTRACT(EPOCH FROM (ts - prev_ts)) / 60
   BigQuery equivalent:   TIMESTAMP_DIFF(ts, prev_ts, MINUTE)

2. ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
   — This is the default for SUM() OVER (ORDER BY ...) but being
     explicit is best practice in interviews.

3. Alternative: Use RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
   — Behaves identically here since we ORDER BY a unique timestamp.

4. If you want a GLOBALLY unique session_id across all visitors:
   CONCAT(visitor_id, '_', session_id) AS global_session_id

"""

# ================================================================
# WHAT YOUR ORIGINAL ATTEMPT HAD RIGHT (and what to fix)
# ================================================================
YOUR_ATTEMPT_NOTES = """

Your original attempt:
    LAG(1) OVER (PARTITION BY visitor_id ORDER BY event_timestamp) AS event_lag

Issues:
  1. LAG(1) is wrong syntax — LAG takes a COLUMN name, not a literal.
     Should be: LAG(event_timestamp) OVER (...)

  2. You calculated the gap but missed the KEY step:
     → Using SUM(is_new_session) OVER (...) to assign the session_id.
     That's the "trick" in sessionization problems.

  3. You need a final GROUP BY to collapse to one row per session.

"""

# ================================================================
# QUICK REFERENCE — the 3-line mental model
# ================================================================
MENTAL_MODEL = """

1. LAG()  → get previous timestamp per visitor
2. CASE   → flag is_new_session = 1 if gap > 30 min (or first event)
3. SUM() OVER (ORDER BY ts) → running sum = session_id ✅
4. GROUP BY session_id → one row per session with MIN/MAX/COUNT

"""

if __name__ == "__main__":
    print("Session Analysis SQL Solution")
    print("=" * 50)
    print(MENTAL_MODEL)
    print("\nFull SQL:")
    print(SOLUTION_SQL)


"""
SELECT visitor_id, event_timestamp, 
    LAG(event_timestam) OVER (PARTITION BY visitor_id ORDER BY event_timestam) as prev_timestamp

SELECT visitor_id, event_timestamp, prev_timestamp, 
        DATEDIFF('minute', prev_event_timestamp, event_timestamp) AS gap_minutes,
        CASE 
            WHEN prev_timestamp is NULL THEN 1
            WHEN gap_minutes > 30 THEN 1
            ELSE 0
        END AS is_new_session


SELECT visitor_id, event_timestamp, is_newsession,
    SUM(is_newsession) OVER (PARTITION BY visitor_id 
                            ORDER BY event_timestamp
                            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                            ) as session_id

SELECT visiotr_id, MIN(event_timestamp), MAx(event_stimestamp), COUNT(*) as event_count
    FROM
    GROUP BY cisitor_id, session_id    

"""