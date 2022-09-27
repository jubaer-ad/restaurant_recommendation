# restaurant_recommendation
Repo to hold all the files of restaurant recommendation from data scraping to prediction.
## Data Scraping
The [fetch_data.py](https://github.com/jubaer-ad/restaurant_recommendation/blob/main/fetch_data.py) file is responsible for scraping data from websites. I used Selenium, BeautifulSoup, chrome webdriver to extract data from website and then saved all data as csv file. This data file is used for training LogisticRegression model for prediction.
* All the data is available at Firebase real time database. You can [email](mailto:jubaerad1@gmail.com) me for access request (<jubaerad1@gmail.com>).
## Model training
The [restaurant_recommendation.ipynb](https://github.com/jubaer-ad/restaurant_recommendation/blob/main/restaurant_recommendation.ipynb) file is used to train LogisticRegression model based on data I scraped before and used pickle to save the model ([restaurant_lr_model.pkl](https://github.com/jubaer-ad/restaurant_recommendation/blob/main/restaurant_lr_model.pkl)) for later use.
## API
The [restaurant_api.py](https://github.com/jubaer-ad/restaurant_recommendation/blob/main/restaurant_api.py) file is used to create an API to interact with the model and get restaurant remmendation. Follow this [link](https://documenter.getpostman.com/view/23040426/2s83f2pbB4) for API documentation.

I used uvicorn to run the server to test the API.
 
