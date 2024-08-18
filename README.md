# [PYTHON] Customer Churn Prediction
## 1. Introduction
### 1. About Customer Churn
Customer churn is one of the most important metrics for a growing business to evaluate. It's easier to save an existing customer before they leave than to convice them to come back. Understanding and preventing customer churn is critical to company's long-term success.
In this project, we will use statistical testing to analyze the key factors of customers who are more likely to churn, develop a classification model to predict churn based on those factors, and provide recommendations for retaining customers as well as predictions of churn for a list of customers (delivered via csv).
### 2. Business Goals
- What are the patterns/behavior of churned users? What are your suggestions to the company to reduce churned users. 
- Build the Machine Learning model for predicting churned users. (fine tuning) 
- Based on the behaviors of churned users, the company would like to offer some special promotions for them. Please segment these churned users into groups. What are the differences between groups? 
### 3. Data Dictionary
| Variable	 | Meaning |
| :--- | :--- | 
| CustomerID  | Unique customer ID | 
| Churn | Churn Flag | 
| Tenure | Tenure of customer in organization |
| PreferredLoginDevice | Preferred login device of customer |
| CityTier | City tier (1,2,3): miền |
| WarehouseToHome | Distance in between warehouse to home of customer |
| PreferPaymentMethod | Preferred payment method of customer |
| Gender | Gender of customer |
| HourSpendOnApp | Number of hours spend on mobile application or website |
| NumberOfDeviceRegist ered | Total number of deceives is registered on particular customer |
| PreferedOrderCat | Preferred order category of customer in last month |
| SatisfactionScore | Satisfactory score of customer on service |
| MaritalStatus | Marital status of customer |
| NumberOfAddress | Total number of added added on particular customer |
| Complain | Any complaint has been raised in last month |
| OrderAmountHikeFroml astYear | Percentage increases in order from last year |
| CouponUsed | Total number of coupon has been used in last month |
| OrderCount | Total number of orders has been places in last month |
| DaySinceLastOrder | Day Since last order by customer |
| CashbackAmount | Average cashback in last month |
## 2. Conclusion
### What are the patterns/behavior of churned users?
- The biggest particular influences for eliminating customer e-commerce services are “Complain”, “MaterialStatus”, “SatisfactionScore”, “PreferedOrderCat”, “DaySinceLastOrder”, “CashbackAmount” and “Tenure”.
- Customers who stay with the service tend to have a longer tenure, while those who leave (churn) typically do so after a shorter duration.
- Customers who prefer using a computer for login have a slightly higher churn rate compared to those who prefer mobile phones.
- Male customers have a slightly higher churn rate compared to female customers
- Single customers have a significantly higher churn rate compared to married and divorced customers.
- Surprisingly, the average satisfaction score is higher for customers who churned compared to those who didn’t. This might suggest that factors other than satisfaction scores are influencing the decision to churn, or that the satisfaction scores may not fully capture the customer’s experience or likelihood to remain with the service.
### What are your suggestions to the company to reduce churned users
- Should consider that the higher percentage are males increasing the products that grap the males interest and so on
- May be the comapny should consider taking care of the products that suits the single and the married customers as the single are more likly to churn
- The company should think of another technique other than satisfaction score or complaining may be a hot line to recive the complains to get fast results or provied regular phone calls to recive feedback from the customers
- The company should check the mobile version of the store to see if there is any problem with the ui/ux
- Once the customer has reached 12%-15% orderamount the company should consider focusing more on grap their attention with the products they like
- For customers who have just bought electronic goods, cross-selling can be done by offering electronic accessories, such as keyboards, mice, etc.
