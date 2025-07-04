Most people throw data at an ML model and pray

# Smart-Inventory-Demand-System Dev Log

## Overview

SmartInventory AI is a cloud-deployable platform that predicts upcoming trends and demand spikes across content categories — just like forecasting which pins, tags, or product types users will engage with next week or next month.

It helps content teams, ad managers, or algorithm engineers prepare inventory or promotion strategies ahead of time.

## June 14th

I figured I should’ve written this earlier but better late than never. This entry is meant to explain the groundwork before things started getting interesting.

I’ve been thinking a lot about inventory systems and what makes them smart. I don't just mean storing static data, and keeping count of certain items, but also predicting and analyzing why anyone would need something based on trends and patterns adjusting to human randomness. I realized there’s not really much public inventory-to-sales data available (unless you’re scraping something sketchy or working for a retailer). So instead of pausing everything, I just made up the data generation layer myself. The trick is: if you model the logic right, you don’t need real data, you need realistic data.

That’s where the project started. It’s a **demand forecasting simulation** that mimics what a real company might do if they had access to product reviews, ratings, and some internal cost/unit pricing info.

The following is the tech stack I will use


**Backend:**
Python + SQLAlchemy --- Python because of data-working frameworks. SQLAlchemy because I want flexibility without ORM hell.
**Database**
MySQL since I want something production-realistic and not just SQLite.
**API/Data Gathering**
SerpApi --- Great web scraping API so that I don't have to scrape pages myself manually, that could be a pain. Not time efficient. This will help me get started with gathering basic products from Amazon, Google, Ebay, Pinterest, etc..
**Data Storage:**
Pandas (in-memory) for ast manipulation. Easier to debug and table export for logs. Can easily convert dictionaries/JSONs back and forth for easier data ingestion and DB submission.

Started with something like this:
```
[ External API ]
        ↓
[ Raw Extractor Module ]
        ↓
[ DataCleaner / Formatter ]
        ↓
[ Product Object Model ]
        ↓
[ Category Tracker + Allocation Engine ]
        ↓
[ MySQL Upload via ORM ]
```

This was the baseline of what I thought of. It turned out to be a bit more complex than what I initially thought. I wanted to 
make the the made-up data as realistic as possible, taking into account different factors which I will discuss in the following
logs.

## June 15th, 11AM
Diving deeper into the idea of ORMs...
I’m using **SQLAlchemy** as the ORM. Could I have gone full raw SQL? Yeah, but I wanted something scalable, readable, and easy to inspect mid execution especially since this is basically an evolving sandbox where logic changes weekly. I will get better at raw SQL scripting in the future, I promise. After all I'm a Data Scientist so it's kind of a must :)

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

`create_engine()` can be thought of being the direct bridge to MySQL using the pymysql driver. An engine can be thought
of as a factory that takes change of creating a `session` which in turn dictates the "commands" the database for different queries.

Next, I defined the schema and general structure of how data injection should be handled from MySQLWorkbench itself, but it's essential to note that our ORM (in-code base) still doesn't know this has happened. It has no idea how the database schema looks like. Hence, we must define it by creating something is a model that represents the database table as an in-python object.

A model is defined like...

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

I made sure to add schema validator layers. Every time I parse an incoming product (whether from API, JSON, or dummy data), this function runs before the data gets committed. This has saved me from a ton of headaches, especially when doing randomized mock data. Something like:
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

One of the main design decisions I made early on is not hiding logic inside functions if you’re gonna need to explain it to your future self. That’s why most of the major data ops (like cleaning, rating, and allocation) I will wrap inside OOP classes.

## June 19th, 10AM

After struggling and attempting complex code that concurrently runs the API data extraction, data cleansing, data storage, and data rating; I finally got it to work for the first iteration of the category chosen *rug*.

Notice that for the sake of simplicity and testing I am using iterating over only one set of categories: rugs

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

And for the next product iterations we will convert the raw extracted data into a big DataFrame; and from this data only included the key imformation for the `Rating` class that will look at the `title` otherwise know as the name of the product, the `rating` of that product and the count of `reviews` of it. To actually rate the product from raw data and the same product from clean data stored in the database I had to use a foreign key indicator to match and extract its respective `rating` and `reviews` that would be used for the main rating functionality. This foreign key will be represented as the name stored in the database; and while a string is not recommended to be used as a lookup key value I didn't want to store in the database the only other alternative, the `asin` that is only for amazon ID serializable products.

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

Nevermind  I changed my mind of the system. Does it ever happen to you that you overcomplicate things for no reasoning without even realizing that you can do things a simpler way? That's what was happening to me during my workaround with all of the classes interconnecting with each other. I had an idea of an algorithm that at the end was less realistic in real-world practice as well as more complicated.
Thankfully, it so happens that I came to my dad's house for the week. He pulled out his powerful Excel spreadsheet and followed the idea that I had into a general normalization. The idea is the following:

Having the product's `asin`, `rating` and `reviews` count, we can set an aggregate normalized unit for every row that can act as the relationship between the ratings and reviews that a product has. This is similar to what I was attempting to do previously. Instead of a ration rating:reviews we do the opposite: ratings x reviews. We will sum this normalized arbitrary unit to be used later on. This aggregate unit explains the total pool from the relationship that follows the logic: `The more people have bought the product, the more it is likely to have more need for stock. Wait, but also consider its rating! The more popular and highly rated it is, then the more the consumers will want it!` 

We then use these output variables to divide the individual normalized unit by the aggregate pool; that for the column, should sum up to one, just like a probability vector, which is exactly what we want. 
This probability vector explains the total percentage that we should take from our original inventory distribution, to come up with a raw floating point of the stock needed for that product.

In a dataframe practice, it looks something like this (from actual logs):

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

I stuck with the idea that to make this system even more realistic I would once choose random values received from the cold allocation vector, by extracting 20th lower percentile of the cold allocation as the `lower bound` as well as the top 80th percentile as the `upper bound`. From these two numbers, we round them down and up accordingly, so we set the range for a random integer within these two. The code looks the following way:

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

Which creates another vector: `Adjusted Allocation`, that represents the most realistic way to bring up a inventory stock for that product:

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

At the end, we never had to weird things with asin addition or name search within the data frame. Thanks dad.
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

As it follows from the previously explained logic, for NaN sales we will build logic to fairly assign allocation to these products based on their proportion of the entire set.

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