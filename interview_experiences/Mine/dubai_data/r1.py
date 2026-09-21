"""

you recieve multiple customer updates with 

customer_id , event_id , updated_at, and ingestion_time. 

write or explain a query that returns the latest valid record per customer. 


if event_time is the same , use updated_at and then ingestion_time as tie breakers ?


customer_id , event_id , updated_at, ingestion_time, event_time


SELECT 
    customer_id, 
    event


"""