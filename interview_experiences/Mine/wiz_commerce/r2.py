"""
Sales
brand, channel, order_date, source

Find out the brand and channels where the data is coming from multiple sources on the same date

Approach:
1. Identify the level of aggregation:
   The question asks for multiple sources "on the same date" for a brand and channel.
   This means we need to evaluate the number of sources within each unique combination of (brand, channel, order_date).
   
2. Group the data:
   We group by `brand`, `channel`, and `order_date`.
   
3. Filter with HAVING:
   To find groups with "multiple sources", we count the unique sources using `COUNT(DISTINCT source)` 
   and filter for groups where this count is greater than 1.
   
4. Select the final output columns:
   We only need the `brand` and `channel`. Since a brand-channel combination could satisfy this 
   condition on multiple different dates, we use `DISTINCT` to return unique combinations.
"""

"""
-- Solution 1: Using GROUP BY and HAVING with DISTINCT
SELECT DISTINCT 
    brand, 
    channel
FROM 
    Sales
GROUP BY 
    brand, 
    channel, 
    order_date
HAVING 
    COUNT(DISTINCT source) > 1;

-- Solution 2: Using a Common Table Expression (CTE) / Subquery for readability
WITH MultiSourceSales AS (
    SELECT 
        brand, 
        channel,
        order_date
    FROM 
        Sales
    GROUP BY 
        brand, 
        channel, 
        order_date
    HAVING 
        COUNT(DISTINCT source) > 1
)
SELECT DISTINCT 
    brand, 
    channel
FROM 
    MultiSourceSales;

"""

"""
/*
======================================================================
EXAMPLE WALKTHROUGH
======================================================================
Suppose the `Sales` table contains the following sample data:

| brand  | channel | order_date | source    |
|--------|---------|------------|-----------|
| Nike   | Online  | 2026-08-01 | Shopify   |  <-- Row 1
| Nike   | Online  | 2026-08-01 | Amazon    |  <-- Row 2 (Nike/Online/Aug-1 has 2 distinct sources: Shopify & Amazon)
| Nike   | Online  | 2026-08-02 | Shopify   |  <-- Row 3 (Nike/Online/Aug-2 has only 1 source: Shopify)
| Adidas | Retail  | 2026-08-01 | Store_POS |  <-- Row 4 (Adidas/Retail/Aug-1 has only 1 source)
| Nike   | Retail  | 2026-08-01 | Store_POS |  <-- Row 5
| Nike   | Retail  | 2026-08-01 | Store_POS |  <-- Row 6 (Nike/Retail/Aug-1 has 2 rows but only 1 distinct source)

Let's trace how "Solution 1" executes:

Step 1: GROUP BY brand, channel, order_date
The rows are grouped into the following buckets:
- Group A: (Nike, Online, 2026-08-01)   -> Rows 1, 2
- Group B: (Nike, Online, 2026-08-02)   -> Row 3
- Group C: (Adidas, Retail, 2026-08-01) -> Row 4
- Group D: (Nike, Retail, 2026-08-01)   -> Rows 5, 6

Step 2: Calculate HAVING COUNT(DISTINCT source) > 1 for each group:
- Group A: Sources are {'Shopify', 'Amazon'}. Count of distinct is 2. (2 > 1 is TRUE) -> KEEP
- Group B: Sources are {'Shopify'}. Count of distinct is 1. (1 > 1 is FALSE) -> DISCARD
- Group C: Sources are {'Store_POS'}. Count of distinct is 1. (1 > 1 is FALSE) -> DISCARD
- Group D: Sources are {'Store_POS', 'Store_POS'}. Count of distinct is 1. (1 > 1 is FALSE) -> DISCARD

Only Group A (Nike, Online) survives the HAVING filter.

Step 3: SELECT DISTINCT brand, channel
Output:
| brand | channel |
|-------|---------|
| Nike  | Online  |


======================================================================
CAN WE USE PARTITIONS (WINDOW FUNCTIONS) HERE?
======================================================================
Yes, you can use PARTITIONS (via the `OVER (PARTITION BY ...)` syntax). 

However, there is an important SQL syntax rule to keep in mind:
- Standard SQL (including PostgreSQL) does NOT allow DISTINCT inside window functions. E.g., 
  `COUNT(DISTINCT source) OVER(PARTITION BY ...)` will throw a syntax error.

To work around this limitation, we must first deduplicate the dataset using `DISTINCT` in a CTE, 
and then apply the partition:

-- Solution 3: Using Window Functions (PARTITION BY)
WITH DeduplicatedSales AS (
    -- Step 1: Remove duplicate source entries for the same brand, channel, and date
    SELECT DISTINCT 
        brand, 
        channel, 
        order_date, 
        source
    FROM 
        Sales
),
PartitionedSales AS (
    -- Step 2: Use partition to count sources for each day
    SELECT 
        brand, 
        channel,
        COUNT(source) OVER(PARTITION BY brand, channel, order_date) as source_count
    FROM 
        DeduplicatedSales
)
-- Step 3: Select only the matching brands and channels
SELECT DISTINCT 
    brand, 
    channel
FROM 
    PartitionedSales
WHERE 
    source_count > 1;

----------------------------------------------------------------------
Comparison: Group By vs Window Functions (Partitions)
----------------------------------------------------------------------
1. Group By (Solution 1) is cleaner, uses less code, and is usually more performant 
   because it reduces the dataset size during aggregation.
2. Window Functions (Solution 3) are typically used when you need to retain individual 
   row details (e.g. if you wanted to see the individual transactions alongside the 
   daily source count). Since we only want to list the `brand` and `channel`, 
   GROUP BY is the standard and recommended tool.
*/
"""