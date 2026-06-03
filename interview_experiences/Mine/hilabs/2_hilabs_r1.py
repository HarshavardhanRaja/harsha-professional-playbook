"""
Assume you're given a table containing data on Amazon customers and their spending on products in different category, 
write a query to identify the top two highest-grossing products within each category in the year 2022. 
The output should include the category, product, and total spend.

product_spend Example Input:

category		product						user_id	spend		transaction_date
appliance		refrigerator			165			246.00	12/26/2021 12:00:00
appliance		refrigerator			123			299.99	03/02/2022 12:00:00
appliance		washing machine		123			219.80	03/02/2022 12:00:00
electronics	vacuum						178			152.00	04/05/2022 12:00:00
electronics	wireless headset	156			249.90	07/08/2022 12:00:00
electronics	vacuum						145			189.00	07/15/2022 12:00:00



SELECT * FROM customer WHERE taransaction_data  as table_a;

SLECT category, product, total_spend as SUM(spend) FROM table_a GROUP BY product, category as table_b;

SELECT category, product, total_spend, rank, ROWNUMBER(OVER total_spend PARTITION BY category) as row_num FROM table_c WHERE row_num < 2 




category		product						user_id	spend		total_spend
appliance		refrigerator			123			299.99  299.99
appliance		washing machine		123			219.80  219.80	
electronics	vacuum						178			152.00  320
electronics	wireless headset	156			249.90	
electronics	vacuum						145			189.00	




DENSE_RANK

vacuum	  1					
wireless  1
headset		1
x 				2
y					2 


RANK: 
vacuum	  1					
wireless  1
headset		1
x 				4
y					4 




0, 1, 1, 2, 3, 5, 8 


def return_nth_element(n):
    if n ==0:
    	return 0
    
    fib_sequence = [0, 1]
		for i in range(n):
    	if i >0:
      	current_sequence = sum(fib_sequence)
    		fib_sequence[0] = fib_sequence[1]
      	fib_sequence[1] = current_sequence
    return fib_sequence[1]


"""