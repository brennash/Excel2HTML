# GraphExcel
GraphExcel is a simple Flask application that can be run locally, or remotely, which provides a handy 
web-front end to upload and convert CSV/Excel files into animated NVD3.js graphs. The backend is 
coded entirely in Python/Flask, allowing it to be easily extended for any number of input data types 
(JSON anyone?). Very useful if you're working on a dataset which needs to be released as a quick 
and dirty online dashboard, or refreshed statically.

![GraphExcel Web Front-End](static/imgs/intro-page.png?raw=true "GraphExcel Web Front End")

When you select a CSV or Excel file, you're provided with a number of options around the type of 
chart required, the colour of the various data series etc. Once you've configured the look and 
feel, you can hit the generate button and see the raw HTML alongside the animated NVD3.js Javascript. 


### Installation
The application requires Python 2.7.x or greater. It is recommended that you install the following 
Python libraries for stand-alone operation. Serving the resulting HTML pages using something like 
Apache2 or Nginx is covered in a later section. 

```
sudo pip install virtualenv
virtualenv venv
. venv/bin/active
pip install openpyxl
pip install Flask
pip install beautifulsoup4
pip install sqlalchemy
```

### Running the application

```
python App.py
```


#### Deploying Application using a web-server
If you're deploying this web-front end in a bit more of a long-lived configuration, it is recommended
you server the resulting HTML using something like Apache2 or Nginx. 
