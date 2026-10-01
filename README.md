### PHASE 1 ( Data Understanding )

## Customers Dataset

- Total Rows : __1020___

- Missing Emails found.

- Missing Phone Numbers found.

- Missing Sign Up Dates found.

- Invalid age datatype (str) found and values consist strings (i.e twenty five ) and some ages re not realistic (i.e 150)

- City names are inconsistent have spacing vaiations and some upercase and lowercase variabtions of same city name 


- Duplicate Rows Exist (20).

- Invalid Phone Numbers Observed.

- Genders have inconsistent Formatting like (Male ,male , M etc ) and also have some unknown values.

- Sign up Dates use multiple Formats.


## Orders Dataset

- Total Rows: __2030___

- Missing Order Dates found.

- Missing Payment Methods found.

- Missing Shipping Cost found.

- 40 customer ids in orders data are not exist in customers data

- 81 products ids in orders data are not exist in products data

- Invalid order status varaitions (  delivered    481).



- Duplicate Rows Exist (30).

- Order Dates use multiple Formats.

- Quantity have negative values and miss matched values types with column data type.

- Payment Methods have inconsistent Formatting (i.e COD , Cash , bank , card , Nan)

- Invalid Discounts Range Observed (i.e -5 , 120 ,etc).

- Invalid Shpipping Cost Observed (i.e -50.0 , 778.0 ,etc).


## Products Dataset

- Total Rows: __510___

- Missing Products Prices found.

- Missing Products Cost found.

- invalid Data Type of Product Price.

- Duplicate Rows Exist (10).

- Invalid Product Prcies Observed (i.e -100 and $2432 adn 23242).

- Invalid Products Categories (i.e Electronics and electronics )




### PHASE 2 ( Data cleaning )

| **Step** | **Dataset** | **Action** | **Rows Before** | **Rows After** | **Business Reason** |
|:--------:|-------------|------------|----------------:|---------------:|---------------------|
| **1** | Customers | Removed exact duplicate rows | **1,020** | **1,000** | Prevent duplicate customer records and inaccurate customer counts. |
| **1** | Orders | Removed exact duplicate rows | **2,030** | **2,000** | Prevent duplicate transactions and incorrect revenue calculations. |
| **1** | Products | Removed exact duplicate rows | **510** | **500** | Prevent duplicate product listings and inconsistent inventory reports. |

### Output Summary

| **Dataset** | **Rows Removed** |
|-------------|-----------------:|
| Customers | **20** |
| Orders | **30** |
| Products | **10** |
| **Total** | **60** |



## justify the target datatype for each column.

# In Customer Dataset

- sign up date should be ----> datetime datatype

- age should be -----> int64 datatype 

# In order Dataset 

- order date should be -----> datetime datatype


# In Products Dataset 

- product price should be -----> int64



### Missing values 

So our investigation phase is FINISHED.

We have now proven that these columns cannot be recovered from any available dataset.

Column	Recoverable?	Decision
signup_date	❌ No	Keep NaT
phone	❌ No	Keep NaN
email	❌ No	Keep NaN
payment_method	❌ No	Keep NaN
price	❌ No	Keep NaN
cost	❌ No	Keep NaN

### Age Validation

**Business Rule**

- Valid customer age must be between **18 and 100** years.

**Investigation**

- Found **12** customers with age **-5**.
- Found **11** customers with age **150**.
- Total invalid ages: **23**.

**Decision**

- Replaced invalid ages with `NaN`.
- Imputed missing values using the **median age (42)**.

**Reason**

Median is more robust to extreme values than the mean and is the preferred choice for imputing demographic data such as age.

### Phone Number Validation

**Business Rule**

- Phone number must contain exactly **11 digits**.
- Phone number must contain only numeric characters.
- Placeholder values such as `123` are considered invalid.

**Investigation**

- Missing phone numbers: 23
- Placeholder value `123`: 23 records
- Invalid text value `abcd123`: 26 records

**Decision**

- Replaced invalid phone numbers (`123` and `abcd123`) with `NaN`.
- Kept missing values as `NaN` because phone numbers cannot be reliably inferred.

**Reason**

Phone numbers are unique identifiers and should never be imputed using statistical methods.


### Email Cleaning

**Investigation**

- Found 79 missing email addresses.
- Found 38 invalid email formats (missing '@' or invalid structure).
- Cross-checked the Orders dataset.
- No email information exists in any other dataset.

**Business Decision**

Invalid email addresses cannot be recovered.

**Cleaning Performed**

- Converted invalid email formats to missing values (`NaN`).
- Kept missing emails as `NaN` for future collection.

**Reason**

Guessing customer email addresses could create incorrect customer records and lead to failed communication.

### Shipping Cost Cleaning

The `shipping_cost` column contained invalid negative values (`-50`) and missing values. Previous investigation showed that these invalid values appeared across all order statuses and payment methods, indicating they were placeholder values rather than valid shipping charges.

The invalid values were converted to missing values and then all missing values were imputed using the overall median shipping cost (465). The median was selected because it is robust to skewed distributions and extreme values, making it a suitable choice for numeric business data.

After cleaning:
- No missing values remained.
- No negative shipping costs remained.
- Shipping costs ranged from 101 to 800.


### Discount Cleaning

The `discount` column contained invalid values (`-5` and `120`) that violated the business rule for percentage discounts (valid range: 0–100). Investigation showed that these invalid values were distributed across all order statuses and payment methods, meaning they could not be recovered from other columns.

The invalid values were converted to missing values and then imputed using the overall median of the valid discounts. The median was chosen because it is resistant to extreme values and is a standard imputation technique for numeric business data.

After cleaning:
- No missing values remained.
- All discount values were within the valid range (0–100).
- The dataset was ready for feature engineering and exploratory data analysis.


### Discount Cleaning

Business rule analysis showed that valid discounts should range between **0% and 100%**. The dataset contained **653 negative discounts (-5%)** and **668 discounts greater than 100% (120%)**, which are invalid.

The invalid values appeared across all order statuses and payment methods, indicating there was no reliable business pattern to recover the original values.

Therefore, all invalid discounts were first replaced with missing values (`NaN`). Since discount is a numerical feature and no recovery source was available, missing values were imputed using the **median discount (25%)**, which is robust to outliers and preserves the central tendency of the valid data.

After cleaning:

- Invalid discounts: **0**
- Missing values: **0**
- Valid discount range: **0%–50%**
### PHASE 3 ( Feature Engineering & Visualization )

**Feature Engineering**
- **ABC Analysis**: Categorized products into A, B, and C classes based on cumulative revenue percentage to identify the most valuable inventory.
- **Product Movement**: Segmented products into Fast, Medium, and Slow moving categories based on quantity percentiles.
- **Quantity & Revenue Rankings**: Ranked products to easily identify top performers and underperformers.

**Data Visualization & Insights**
- Generated comprehensive plots using Matplotlib and Seaborn.
- Analyzed customer distributions across various cities and demographics.
- Identified top 10 revenue-generating products and the bottom 10 products requiring potential strategy adjustments.
- The dataset is fully prepared for any further predictive modeling or advanced machine learning workflows.
