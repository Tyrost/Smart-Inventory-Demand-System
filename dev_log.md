
# Dev Log

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
{'category': 'Rug',
 'cost': 49.54,
 'product_id': 'US25061900019',
 'product_name': 'Washable Rugs 8x10',
 'unit_price': 84.99},
{'category': 'Rug',
 'cost': 6.21,
 'product_id': 'US25061900020',
 'product_name': 'FinRèc Soft Black',
 'unit_price': 13.99},
{'category': 'Rug',
 'cost': 195.44,
 'product_id': 'US25061900021',
 'product_name': 'nuLOOM 10x14 Rigo',
 'unit_price': 339.76},
{'category': 'Rug',
 'cost': 17.72,
 'product_id': 'US25061900022',
 'product_name': 'nuLOOM 2\'8" x',
 'unit_price': 44.49},
{'category': 'Rug',
 'cost': 27.28,
 'product_id': 'US25061900023',
 'product_name': 'Loloi Magnolia Home',
 'unit_price': 47.03},
{'category': 'Rug',
 'cost': 18.34,
 'product_id': 'US25061900024',
 'product_name': 'Unique Loom Outdoor',
 'unit_price': 50.0},
{'category': 'Rug',
 'cost': 20.48,
 'product_id': 'US25061900025',
 'product_name': 'Large Shag Area',
 'unit_price': 45.99},
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






