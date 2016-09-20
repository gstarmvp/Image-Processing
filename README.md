# Image Processing Project


A web-based application is introduced to recognize and analyze handwritten digits. The system used is statistical methods such as Zoning and Histogram. The system crops the image such that only the significant part of the image is obtained and essentially discarding unneeded whitespace to reduce processing time. There are two different databases that are used to store feature vectors obtained from Zoning and Histogram methods. A sample of twenty images are tested against these methods and we found that Zoning method recognized our inputs correctly 95% of the time on average and Histogram method recognized them 77% of the time on average. The project URL is http://project-cp467.rhcloud.com. 

*The url may produce a 503 since it is hosted on a free tier plan on Openshift. A few refreshes may be needed to access the site*


## Features
1. Filters
  - Low / High pass filters, Median filter, Gaussian filter
  
2. Zhang-Suen Thinning

3. Image Vector Retrieval
  - Zoning and Histogram methods
  
4. Handwritten Recognition
  - single digit from 0-9


## Installation and Run
1. `pip install -r requirements.txt`
2. `python app.py`
3. Visit `127.0.0.1:8080`


### Authors:
Don Miguel and [Chunxiao Li](https://github.com/ian8170) 
