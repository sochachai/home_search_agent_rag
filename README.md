# Home Search Agent using RAG
## Introduction
This project aims to build a local home search AI assistant with Redfin's data of (new listed) on-sales property, which is open to public.

Users will type requirements/queries on home properties. This AI home search assistant will return the best matches of on-sales home based on the Redfin's "about this home"
descriptions which are web-scraped to local.

## Step-by-step Walk Through
#### 1. Run in terminal: "pip install -r requirements.txt" to install packages 

#### 2. If any package fails to be installed. Try:
        2.1 Open terminal an use "pip install package_name" or
        2.2 Go to Pycharm -> Settings -> Python Interpreter to install the missing package

#### 3. Run in terminal: "python redfin_new_listings.py" to webscrape the url's of Redfin's new listed on sales properties and store the url list as "opening_dec_14_2024.txt"
#### 4. Run in terminal: "python redfin_webscrape.py" to webscrape the "about this home" text descriptions of all properties whose url's are given in "opening_dec_14_2024.txt" and save the text descriptions as pdf's under the directory data/home
#### 5. Run in terminal: "python update_database.py" to convert the pdf's in Step 4 into vectors in a vector database named "chroma_data"
#### 6. Run in terminal: "python home_search.py 'Client query'" to ask AI assistant to return the best matched properties or answer any other questions raised by the client.

## Results Demo
Some results are stored in result_screenshots for demo.
Below is a breakdown of each client query and the corresponding results.

#### Query 1: "I want a home with a spacious backyard. Return me the property url of the best match."
     Results: Url of the best matched is returned. query_1_text_introduction.png shows the "about this home" section of the property.
              query_1_picture.png is the street view of the property. 
              The AI assistant has found a property that fulfills the requirement of "a spacious backyard"

#### Query 2: "I want a home in California with at least 5 rooms. Return me the property url rooms. Return me the property url of the best match."
     Results: Url of the best matched is returned. query_2_text_introduction.png shows the "about this home" section of the property.
              query_2_picture.png is the street view of the property. 
              The AI assistant has found a property that fulfills the requirements of "in California" and "at least 5 rooms"

#### Query 3: "I want a home with new appliances and furnitures. Return me the property urls of the top 3 matches. "
     Results: Url's of top 3 matched are returned. The first two links/properties are relevant. 
              "Newer vinyl windows, appliances all new and stainless, Central AC, Furnace and Hot Water Tank all inspected and in excellent condition."
              described in the first link is very closed to what the client looks afer
              The third link/property does not satisfy the client's requirement. The words "brand new" and "ready to move in" might have confused AI.

#### Query 4: "Give me the text description of the property with url being 'https://www.redfin.com/TX/Anna/2008-Erlinda-Dr-75409/home/180312999'"
     Results: AI returns the same text description as displayed in the "about this home" section in the url.

## Note
The data in this project was web-scraped from Redfin on Dec 14, 2024. The results stored in result_screenshots were generated in Dec 15, 2024. 
Results might vary if the code scripts are run in a different date as some of the property status might change, i.e. on-sales properties will be off market in the future.  

## Disclaimer
All data uploaded in this project is open to public and can be found in Redfin's websites