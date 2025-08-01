Most people throw data at an ML model and pray

# Smart-Inventory-Demand-System Dev Log

## Overview

SmartInventory AI is a cloud-deployable platform that predicts upcoming trends and demand spikes across content categories just like forecasting which pins, tags, or product types users will engage with next week or next month.

It helps content teams, ad managers, or algorithm engineers prepare inventory or promotion strategies ahead of time.

## June 14th

I figured I should’ve written this earlier but better late than never. This entry is meant to explain the groundwork before things started getting interesting.

I’ve been thinking a lot about inventory systems and what makes them smart. I don't just mean storing static data, and keeping count of certain items, but also predicting and analyzing why anyone would need a record based on trends and patterns adjusting to the human element of randomness. I realized there’s not really much public inventory-to-sales data available (unless you’re scraping something sketchy or working for a retailer). So instead of pausing everything, I just made up the data generation layer myself. The trick is: if you model the logic right, you don’t need real data, you need realistic data.

That’s where the project started. It’s a **demand forecasting simulation** that mimics what a real company might do if they had access to product reviews, ratings, and internal cost/unit pricing info.

The following is the tech stack I will use

```
**Backend:**
Python + SQLAlchemy because python has great data-working frameworks. SQLAlchemy because I want flexibility without ORM hell.
**Database**
MySQL since I want something production-realistic and not just SQLite.
**API/Data Gathering**
SerpApi is a great web scraping API so that I don't have to scrape pages myself. The scraping alone would be incredibly slow, not because of the technological aspect, but because you have to adapt to different HTML structures for data extraction. This is simply not time efficient nor relevant to the focus of this project. Instead, the API will help me get started with gathering basic products from Amazon, Google, Ebay, Pinterest, etc..
**Data Storage:**
Pandas (in-memory) for ast manipulation. Easier to debug and table export for logs. Can easily convert dictionaries/JSONs back and forth for easier data ingestion and DB submission.
```
Started with something like this:
```
[ External API ]
        ↓
[ Raw Extractor Module ]
        ↓
[ DataCleaner / Formatter ]
        ↓
[ ORM Object Model ]
        ↓
[ Category Tracker + Allocation Engine ]
        ↓
[ MySQL Upload via ORM ]
```

This was the baseline of what I thought of. It turned out to be a bit more complex than what I initially thought. I wanted to 
make the made-up data as realistic as possible. Taking into account different factors which I will discuss in the following
logs.

## June 15th, 11AM
Diving deeper into the idea of ORMs...
I’m using **SQLAlchemy** as the ORM. Could I have gone full raw SQL? Yeah, but I wanted something scalable, readable, and easy to inspect mid execution. Especially since this is basically an evolving sandbox where logic changes weekly. I will get better at raw SQL scripting in the future, I promise. After all I'm a Data Scientist so it's kind of a must :)

I initialized a `Connection` class that will serve as the parent class for our database ORM execution queries.
The basic setup is the following:

```py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Connection:
    ...

DATABASE_URL = f"mysql+pymysql://{self._user}:{self.__password}@{self.host}/{self.database}"

self.engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
self.session = SessionLocal()
```

`create_engine()` can be thought of the direct bridge to MySQL using the pymysql driver. An engine can be thought
of a factory that is tasked with creating something called a `session` which in turn dictates and "commands" the database for different queries. If anything goes wrong, for example committing and submitting something to the DB, the `session` will likely be damaged, hence we must implement a handler for error and health checkers for this session, such that if an issue arises with it, we call for a new session creation via engine.

Next, I defined the schema and general structure of how data injection should be handled from MySQLWorkbench itself. It is essential to note that our ORM (in-code base) still doesn't know this has happened. It has no idea how the database schema looks like. Hence, we must define it by creating something called a `model` that represents the database table as an in-python object.

A model is defined as...

```py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, DATE, INTEGER, DECIMAL, BOOLEAN # all SQL data types

Base = declarative_base()

class MyTableName(Base)
    __tablename__ = "MyTableName"
    id = Column(VARCHAR(20), primary_key=True)
    name = Column(VARCHAR(100))
    has_pets = Column(BOOLEAN())
```
The schema placed within your models **must** be the the same as in the workbench. Otherwise there will be problems (most likely, I'm not taking chances).
The `declarative_base` function creates an instance that contains all attributes needed to tie your SQL Tables with your modeled classes. All these models are subclasses of this base as a way to tie them all together for the same database.

I made sure to add schema validator layers. Every time I parse an incoming product (whether from API, JSON, or dummy data), this function runs before the data gets committed. This has saved me from a ton of headaches, especially when using randomized mock data.
```py
match(table):
    case "table1":
        target = {
            "product_id": str,
            "unit_price": float,
            "cost": float,
        }
    case "table2":
        target = {...}
...
for key in target:
    expected_type  = target[key]
    if not isinstance(attempt[key], expected_type):
        return False
```

One of the main design decisions I made early on is not hiding logic inside functions if you’re gonna need to explain it to your future self. That’s why most of the major data ops (like cleaning, rating, and allocation) I will wrap inside classes for easier readability and debugging.

## June 19th, 10AM

After struggling and attempting complex code that concurrently runs the API data extraction, data cleansing, data storage, and data rating; I finally got it to work for the first iteration of a category chosen.

Notice that for the sake of simplicity and testing I am iterating over only one set of categories: rugs.

I made a bunch of print statements to fully understand what was happening. To be honest, I was expecting to see many more bugs than there were. For the sake of understanding, the following is the printing logs for the data; as well as the comparison for every product's rating for each category:

** The following is the list of products when the data has been cleaned and ready for DB upload. **
```py
[
{'category': 'Rug',
 'cost': 21.67,
 'product_id': 'US25061900017',
 'product_name': 'Area Rug 5x7',
 'unit_price': 43.69},
{'category': 'Rug',
 'cost': 6.19,
 'product_id': 'US25061900018',
 'product_name': 'Ophanie Area Rugs',
 'unit_price': 9.99},
...
{'category': 'Rug',
 'cost': 44.87,
 'product_id': 'US25061900026',
 'product_name': 'AMADA HOMEFURNISHING 8x10',
 'unit_price': 79.99}
]
```

** Extracted Product Names for each category **

```py
Product names for category: Rug

['Area Rug 5x7',
 'Ophanie Area Rugs',
 'Washable Rugs 8x10',
 'FinRèc Soft Black',
 'nuLOOM 10x14 Rigo',
 'nuLOOM 2\'8" x',
 'Loloi Magnolia Home',
 'Unique Loom Outdoor',
 'Large Shag Area',
 'AMADA HOMEFURNISHING 8x10']

Total category stock: 263
```

And for the next product iterations we will convert the raw extracted data into a big DataFrame; and from this data only included the key imformation for the `Rating` class that will look at the `title` otherwise know as the name of the product, the `rating` of that product and the count of `reviews` of it. To actually rate the product from raw data and the same product from clean data stored in the database I had to use a foreign key indicator to match and extract its respective `rating` and `reviews` that would be used for the main rating functionality. This foreign key will be represented as the name stored in the database; and while a product name is not recommended to be used as a lookup key value (as opposed to an ID) I didn't want to store something like an `asin` that is purely for amazon ID serializable products and not dynamic to other markets like Facebook marketplace or Ebay.

**I would like to note that there was no need for API recall for every iterations as I used inheritance to store this aggregate data into a parent attribute to be used by the `Rating` system and the `Clean`-ing of data system.**


| #  | Product Name                                                                | Rating | Reviews |
|----|-----------------------------------------------------------------------------|--------|---------|
| 0  | Area Rug 5x7, Washable Rug for Living Room, La...                           | 4.7    | 59      |
| 1  | Ophanie Area Rugs for Bedroom Living Room, Gre...                           | 4.2    | 24074   |
| 2  | Washable Rugs 8x10 Area Rugs for Living Room,R...                           | 4.5    | 502     |
| 3  | FinRèc Soft Black Rugs for Bedroom Living Roo...                            | 4.6    | 770     |
| 4  | nuLOOM 10x14 Rigo Jute Hand Woven Area Rug, Of...                           | 4.1    | 26668   |
| 5  | nuLOOM 2'8" x 8' Indoor Performance Area Rug, ...                           | 3.9    | 76      |
| 6  | Loloi Magnolia Home by Joanna Gaines Ryder Col...                           | 4.8    | 67      |
| 7  | Unique Loom Outdoor Botanical Collection Area ...                           | 4.5    | 601     |
| 8  | Large Shag Area Rugs 6 x 9, Tie-Dyed Plush Fuz...                           | 4.4    | 2333    |
| 9  | AMADA HOMEFURNISHING 8x10 Washable Area Rug, L...                           | 4.7    | 450     |
*thanks ChatGPT for the pretty formatting :)*

And for every iteration...

```
Foreign key: Area Rug 5x7
Rating score computed: 0.4178655438401563
Lower Bound: 10; Upper Bound: 87
Randomized score for item "Area Rug 5x7": 70

Foreign key: Ophanie Area Rugs
Rating score computed: 0.9201289221172803
Lower Bound: 24; Upper Bound: 193
Randomized score for item "Ophanie Area Rugs": 139

Foreign key: Washable Rugs 8x10
Rating score computed: 0.6078527966375836
Lower Bound: 15; Upper Bound: 127
Randomized score for item "Washable Rugs 8x10": 18

...
```

At the end, the allocation looks the following (for one category):
```py
{'Rug': {'AMADA HOMEFURNISHING 8x10': 36,
         'Area Rug 5x7': 70,
         'FinRèc Soft Black': 20,
         'Large Shag Area': 102,
         'Loloi Magnolia Home': 38,
         'Ophanie Area Rugs': 139,
         'Unique Loom Outdoor': 126,
         'Washable Rugs 8x10': 18,
         'nuLOOM 10x14 Rigo': 59,
         "nuLOOM 2'8\" x": 49}}
```

## June 20th, 2PM

Nevermind I changed my mind on the system. Does it ever happen to you that you overcomplicate things for no reasoning without even realizing that you can do things a simpler way? That's what was happening to me during my workaround with all of the classes interconnecting with each other. I had an idea of an algorithm that at the end was less realistic in real-world practice as well as more complex in-code.
Thankfully, it so happens that I came to my dad's house for the week. He pulled out his powerful Excel spreadsheet and followed the idea that I had into a general normalization. The idea is the following:

Having the product's `name`, `rating` and `reviews` count, we can set an aggregate normalized unit for every row that can act as the relationship between the ratings and reviews that a product has. This is similar to what I was attempting to do previously. Instead of a ration of `rating:reviews` we do the opposite: `ratings x reviews`. We will sum this normalized arbitrary unit to be used later on. This aggregate unit explains the total pool from the relationship that follows the logic: `The more people have bought the product, the more likely it is to have more need for stock for that product. Additionally, considering the rating, the more popular and highly rated it is, the more the consumers will want it.` 

We then use these output variables to divide the individual normalized unit by the aggregate pool; that for the column, should sum up to one, just like a probability vector, which is exactly what we want. 
This probability vector explains the total percentage that we should take from our original inventory distribution, to come up with a raw floating point of the stock needed for that product.

In dataframe practice, it looks something like this (from actual logs):

Total products chosen: 2068 for category: Drill

| #  | Title                                                | Rating | Reviews | Normalized Unit  | Standard Factor  | Cold Allocation  |
|----|------------------------------------------------------|--------|---------|------------------|------------------|------------------|
| 0  | SDS-Max to SDS-Plus Adapter,Rotary Hammer Conn...    | 5.0    | 2       | 10.0             | 0.000022         | 0.03             |
| 1  | DEWALT 20V MAX Cordless Drill Driver, 1/2 Inch...    | 4.8    | 8351    | 40084.8          | 0.089323         | 117.91           |
| 2  | DEKOPRO 8V Cordless Drill, Drill Set with 3/8"...    | 4.5    | 3536    | 15912.0          | 0.035458         | 46.80            |
| 3  | AVID POWER 20V MAX Lithium lon Cordless Drill ...    | 4.6    | 21958   | 101006.8         | 0.225079         | 297.10           |
| 4  | 20V Cordless Brushless Power Drill Set with 2 ...    | 4.7    | 405     | 1903.5           | 0.004242         | 5.60             |
| 5  | ENERTWIST Cordless Screwdriver, 8V Max 10Nm El...    | 4.3    | 6892    | 29635.6          | 0.066039         | 87.17            |
| 6  | Jar-Owl 21V Pink Cordless Drill Set for Women...     | 4.4    | 888     | 3907.2           | 0.008707         | 11.49            |
| 7  | Cordless Drill Set 21v Power Drill Cordless Wi...    | 4.4    | 136     | 598.4            | 0.001333         | 1.76             |
| 8  | WORX Nitro 40V Brushless Cordless Earth Auger,...    | 4.1    | 7       | 28.7             | 0.000064         | 0.08             |
| 9  | DEWALT 20V MAX Cordless Drill and Impact Drive...    | 4.7    | 54399   | 255675.3         | 0.569734         | 752.05           |

The `Cold Allocation` represents the raw floating point of what the stock product should *strictly* be (in other words, it sums up to our total set stock in this case 2068). But obviously you cannot have a fraction of the product. This leads to the next piece of this system.

I stuck with the idea that to make this system even more realistic I would once choose random values received from the cold allocation vector, by extracting 20th lower percentile of the cold allocation as the `lower bound` as well as the top 80th percentile as the `upper bound`. From these two numbers, we round them down or up accordingly, such that we set the range for a random integer within these two. The code looks the following way:

```py
lower_bound:list = self.dataframe["cold_allocation"] * 0.20
upper_bound:list = self.dataframe["cold_allocation"] * 0.80

adjusted = []
for i in range(len(self.dataframe)):
    l = floor(lower_bound[i])
    r = ceil(upper_bound[i])

    adjusted_allocation:int = randint(l, r)
    adjusted.append(adjusted_allocation)
```

Whose outputs create another vector: `Adjusted Allocation`, that represents the most realistic way to bring up a inventory stock for that product:

| #  | Adjusted Allocation |
|----|---------------------|
| 0  | 1                   |
| 1  | 34                  |
| 2  | 38                  |
| 3  | 75                  |
| 4  | 3                   |
| 5  | 30                  |
| 6  | 4                   |
| 7  | 1                   |
| 8  | 1                   |
| 9  | 472                 |


The end result for two products:

```py
{'GlueStick': [("Elmer's Disappearing Purple", 1),
               ('Amazon Basics Purple', 34),
               ('Scotch Wrinkle Free', 38),
               ("Elmer's All Purpose", 75),
               ("Elmer's E543 Washable", 3),
               ('Avery Glue Stick', 30),
               ('Scotch Permanent Glue', 4),
               ('Avery Glue Stic', 1),
               ("Elmer's All Purpose", 1),
               ('Adtech W229 34ZIP100', 472)],
    'Drill': [('SDS Max to', 1),
            ('DEWALT 20V MAX', 105),
            ('DEKOPRO 8V Cordless', 29),
            ('AVID POWER 20V', 150),
            ('20V Cordless Brushless', 3),
            ('ENERTWIST Cordless Screwdriver', 61),
            ('Jar Owl 21V', 6),
            ('Cordless Drill Set', 2),
            ('WORX Nitro 40V', 1),
            ('DEWALT 20V MAX', 940)]}
```

At the end, we never had unnecessary variables such as the previously discussed asin or name search within the data frame. Thanks dad.
Next steps, we will add this data onto the `stock` table in MySQL with all other required fields.

## June 21st, 6PM

Today I built something I’m really proud of. It’s a complete restock mapping system. Like, an actual inventory analysis engine that detects patterns from logs and **recommends how much stock to allocate** across products. Not guessing, no hardcoded values, all backed by realistic logs and probabilities.

This is the first time the system takes in actual trends from sale logs (`inventory_log` table), finds which products have been moving the most (or the least), and makes restock decisions accordingly. Let me break down how it works, because it’s actually a multi-step pipeline.

```
    ┌──────────────────────────┐
    │  Sales Logs from ORM     │ ← filter: {"change_type": "sale"}
    └────────────┬─────────────┘
                 ↓
       [ thread_restock(data) ]
                 ↓
    1. Group logs by product_id
    2. Sum quantity sold
    3. Reconstruct original stock
    4. Calculate sale rates
    5. Derive restock size
    6. Handle NaNs w/ fairness logic
    7. Normalize allocation via two metrics:
       - popularity (based on sale count)
       - speed (rate of stock movement)
    8. Average both methods into `adjusted_allocation`
    9. Format final data for ORM upload
```
Thanks ChatGPT for the amazing diagram :)

I think I did a good job explaining the reasoning behind the decisions I made regarding the reallocation by taking into account human randomness and out-of-stock products. But the following reason that can be found in the code: `/data/sales/inv_management.py` is the following:

```text
We will observe the rate of change in which items are being sold.
If there are a lot of items being sold in shorter X periods of time, 
then we will prioritize allocating more stock onto that product.

From here we want to implement an algorithm that takes into account demand, as well as the urgency of having close to no stock left for an aggregate product.
Select a total number of allocations for this iteration based on total "popularity" of our products, by taking the same approach as our sales simulations when choosing how many products will be sold for that iteration. We will choose to restock 80% to 120% of what was sold for that iteration based on a random value between these two.
For products that had no sales as a result of having 0 stock initially, there is not really a great way to know the products popularity. It could very well be that the product was greatly successful or the opposite, that it may be unpopular. That's outside of our current scope, so we "promise" to allocate an arbitrary number of stock into it.
```

First, I calculate how much stock to restock for the entire batch. I group everything by product ID and track two things:
`quantity_change`: how much was sold (represented as negative values)
`stock_level`: current stock left

Then I reconstruct the original stock (before sales) and calculate how fast each product was selling.
```py
trends["original_stock"] = trends["stock_level"] + abs(trends["quantity_change"])
trends["rates"] = abs(trends["quantity_change"]) / trends["original_stock"]
```
The rates column acts like a speed indicator. The faster it's sold, the higher the demand signal.

As it follows from the previously explained logic, for NaN sales we will build logic to fairly assign allocation to these products based on their proportion of the entire set. In other words, gather a percentage based on how prominent NaN values are compared to the total record count sampled. Then use this percentage to "cut" this value from our `quantity_to_restock` and distribute the count evenly among the NaN values.

```py
num_nans = trends["rates"].isna().sum()
total_products = len(trends)
nan_proportion = num_nans / total_products

nan_total_allocation = round(quantity_to_restock * nan_proportion)
```

To bring the logically-based probability vector (Based on how often a product shows up (popularity)) and the rate-of-change probability vector (Based on how fast it’s being bought (urgency)), I took the average of these two as a way to merge them:

```py
trends["adjusted_allocation"] = (trends["cold_allocation"] + trends["rate_allocation"]) / 2
```

Finally I took the new computed restocking allocation computed and leveraged off of pandas to build my list of dictionaries that followed the correct schema to be sent to the database.
```py
dataframe["stock_level"] = dataframe["stock_level"] + dataframe["quantity_change"]
dataframe["log_date"] = date.today()
dataframe["warehouse"] = "United Warehouse Main, Washington, US"
dataframe["change_type"] = "restock"
dataframe["log_id"] = [create_invlog_id() for i in range(len(dataframe))]
dataframe["reference_id"] = None

prepared_data = dataframe.to_dict(orient="records")
for data in prepared_data:
    status = database.create_item(data)
    if status != 200:
        raise Exception(f"An error occurred when uploading `inventory_log` data. Code: {status}")
```
Note to self: Please implement database submission as a batch instead of individual commits :)

*Up next* is the big deal and primary focus of the project: Forecast and enhance my ML skills to make this system come to light.
After that comes some cloud service stuff (aka AWS Lambda, AWS RDS), which I pray will have minimal prices or free tiers for small datasets and semi-small computation intervals.

## July 21st, 7PM

Okay, I got busy with work. But we are so back.

Today was the time when all the systems were finally places together concurrently into one.
After adding some doc strings to fully captivate the functionalities of each of the systems,
we ran the script and it worked first time.

Now the task will be to run this script for various iterations to have enough data to feed it into our model. The goal
will be to have 2 months worth of data such that we can start creating our ML model for prognostication, statistics and metrics that we will later turn into endpoints for real-life usage.

I was running into the issue there wasn't enough validation when the API would fetch a non-valid response. The issue that I was having was for the product category `Book`. Which is odd, but the output looked like this:

```py
{   
    '_parameters': {'engine': 'amazon', 'k': 'Book', 'amazon_domain': 'amazon.com', 'device': 'desktop'},
    ...
    'search_information': {'organic_results_state': 'Fully empty'}, 
    'error': "Amazon hasn't returned any results for this query."
}
```

The reason why the first system was working for only one iteration was that the category -as the search parameter (k)- so happened to find results; so we have to validate the output so that if the category input was not valid we could skip that product as a whole. This way, our system works for the 60-time iteration (2 months).

Now, to actually create the the threading system that will run the script many times, we will have to keep track of the dates. Aditionally, since we dont want to introduce a new product category to our system for every iteration, I will only introduce a singular category only 10% of the times.

```py
def thread_simulation(simulation_days=30):
    current_date = date(2020, 1, 1) # arbitrary start date
    for day in range(simulation_days):
        prob = randint(1, 100)
        ...
        execute(current_date, False, 1) if prob > 90 else execute(current_date)

        current_date = current_date + timedelta(days=1)
        sleep(3)
    ...
    return
```
Where the `execute()` function calls the three system processes at once.
Notice that I also included a `sleep()` function for three seconds to avoid something like a 406.
At the end, the logs look like this:

```bash
2025-07-22 10:16:52,497 [INFO] root: 1/3 Processing `product` and `allocation`. Now populating...
2025-07-22 10:16:54,184 [INFO] root: Processing data batch (10 records): Toaster
2025-07-22 10:16:54,254 [INFO] root: Product creation and allocation complete.
2025-07-22 10:16:54,254 [INFO] root: 2/3 Processing `sales` and updating `inventory_log` accordingly...
2025-07-22 10:16:54,290 [INFO] root: Sale simulation successful. Moving on.
2025-07-22 10:16:54,290 [INFO] root: 3/3 Threading `inventory_log` restock process...
2025-07-22 10:16:54,303 [INFO] root: Iteration was successful. Day: 2020-01-01
...
2025-07-22 10:17:11,415 [INFO] root: 1/3 API product gathering process has been skipped. Continuing with simulation...
2025-07-22 10:17:11,415 [INFO] root: 2/3 Processing `sales` and updating `inventory_log` accordingly...
2025-07-22 10:17:11,597 [INFO] root: Sale simulation successful. Moving on.
2025-07-22 10:17:11,597 [INFO] root: 3/3 Threading `inventory_log` restock process...
2025-07-22 10:17:11,648 [INFO] root: Iteration was successful. Day: 2020-01-05
...
2025-07-22 10:20:22,874 [INFO] root: 1/3 Processing `product` and `allocation`. Now populating...
2025-07-22 10:20:22,992 [INFO] root: Processing data batch (10 records): Shampoo
2025-07-22 10:20:23,025 [INFO] root: Product creation and allocation complete.
2025-07-22 10:20:23,025 [INFO] root: 2/3 Processing `sales` and updating `inventory_log` accordingly...
2025-07-22 10:20:23,191 [INFO] root: Sale simulation successful. Moving on.
2025-07-22 10:20:23,191 [INFO] root: 3/3 Threading `inventory_log` restock process...
2025-07-22 10:20:23,213 [INFO] root: Iteration was successful. Day: 2020-02-29

Product record count: 100
Unique product categories: ['Toaster', 'FirstAidKit', 'LightBulb', 'Drill', 'Curtains', 'Crayons', 'PaperShredder', 'Iron', 'JumpRope', 'Shampoo']

Inventory log record count: 6909
```
Now we have enough data to focus on the last part of the project.

## July 22nd, 10AM

I must be transparent. I've taken limited college courses on Data Science; but as I continue, I know I will improve in this regard. Many of the functionalities that I created involving AI were not what I was hoping for, but in the end I created a simple ML forecast that works. It may not be very accurate, but it is something. ChatGPT helped me a lot along this process. I did my best to attempt to understand every line of code, and to that I succeeded.

Well then, to an explenation of the code.
I began with the `Train` class which prepared our data's features for prognostication. I made various logistical modifications to my core infrastructure, which included the addition to a new type of filter. 

```py
if filter: # old version
    query = query.filter_by(**filter)
if table_filter: # new version
    query = query.filter(and_(*table_filter))
```

which not takes an array of conditions to be met. Suppose we wanted to filter and return records which include certain attributes such as date. Then we would have to gather that table model's date attribute and filter it like so:
```py
my_database = Commander("table1")
date_object = my_database.table.date # gather the instantiated object's date
dog_type = my_database.table.type
my_filter = [date_object > date(2025, 1, 1), date_object < date(2020, 1, 1), dog_type == "Dog", ...]

data = my_database.read(filter_table=my_filter)
```
This type of filter will allow us to have better control over more complex data gathering.

From this class, the main focus is to gather the data we want specifically. Since the point is to forecast the amount of stock we will need to allocate in the future month then operation on this class will include: Grouping sale data by product id, filtering data by window cutoff, gathering latest product's stock left, compute and describe data metrics, as well as proper validation and error handling.
When this has been created we will ensure the output of the main executing function is consumed by our modeling class to split and train the data leveraging off of sklearn functions. I decided to go for the `Random Forest Regression` algorithm as of the recommendation of ChatGPT.

## July 25th, 8PM

To have more control over the overall simulation, I decided to give the user the option to configure global variables to passed among function parameters for metric ranges/bounds, variability, computation time and date ranging.

When it comes time to modify these parameters by a user –that may not understand the core program– the logic, datatype, context and usage are all account for when error may come up. I created unittest-like guardian-coded functions that protect the program around these potentially illogical parameters via assertion:

```py
# definitions
PRODUCT_RESTOCK_LOWER_PROPORTION:float = None
PRODUCT_RESTOCK_UPPER_PROPORTION:float = None
...
ITERATION_PRODUCT_COUNT_ALLOCATION_LOWER_BOUND:int = None
ITERATION_PRODUCT_COUNT_ALLOCATION_UPPER_BOUND:int = None
ITERATION_PRODUCT_COUNT_ALLOCATION_UNIFORM_BOUND:int = None
...

def validate_config()->None:
    test = True
    if (PRODUCT_RESTOCK_LOWER_PROPORTION and PRODUCT_RESTOCK_UPPER_PROPORTION) or PRODUCT_RESTOCK_UNIFORM_PROPORTION:
    test = test and not (
        PRODUCT_RESTOCK_LOWER_PROPORTION < PRODUCT_RESTOCK_UPPER_PROPORTION and
        not (PRODUCT_RESTOCK_LOWER_PROPORTION and PRODUCT_RESTOCK_UPPER_PROPORTION and PRODUCT_RESTOCK_UNIFORM_PROPORTION) and 
        (not (PRODUCT_RESTOCK_LOWER_PROPORTION + PRODUCT_RESTOCK_UPPER_PROPORTION == 1) or
        PRODUCT_RESTOCK_UNIFORM_PROPORTION <= 1) and
        (isinstance(PRODUCT_RESTOCK_LOWER_PROPORTION, float) and isinstance(PRODUCT_RESTOCK_UPPER_PROPORTION, float)) or isinstance(PRODUCT_RESTOCK_UNIFORM_PROPORTION, float)
    )
    ...
    if SIMULATION_STARTING_DATE:
        test = test and isinstance(SIMULATION_STARTING_DATE, date)
    ...
    assert(test)
```
These variables are directly exported to the location of the respective context and used by integration to the simulation. If a global configuration variable is not defined then there will always exists some default value to take it's place:
```py
if config.SALE_SIMULATION_PROPORTION_LOWER_BOUND and config.SALE_SIMULATION_PROPORTION_UPPER_BOUND:
    lower = config.SALE_SIMULATION_PROPORTION_LOWER_BOUND
    upper = config.SALE_SIMULATION_PROPORTION_UPPER_BOUND
    assert(lower < upper and (lower + upper) < 1)
else:
    lower = 0.05
    upper = 0.30
```

## July 31st, 9PM

I started working on the two options to running this program: CLI & AWS Lambda.
The CLI will be primarily used as an internal tool for testing purposes, while Lambda will be used for production use.

The CLI utilizes various flags for their respective configuration-setting as discussed in the previous log, pretty straight forward tool.

