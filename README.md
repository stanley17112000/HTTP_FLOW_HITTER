# HTTP_FLOW_HITTER

This is a Python2.7 Project.

It's helps you to increase the flow count of some websites, which based on counting different IP sources. 



## Installation

Please install python2.7 first

before you start
-----------------------------------
        sudo pip install -r requirements.txt

## Usage

parameters in washer.py
-----------------------------------
        - target_url : the website you want to access
        - proxy_use_limit : the proxy will be removed after reach this limit
        - max_request_time : maximum wait time for next request
        - min_request_time : minimum wait time for next request
        - max_proxy_request_time : maximum wait time for next proxy update request
        - min_proxy_request_time : minimum wait time for next proxy updaterequest
        - config_method : specify the proxy source

start to hit
-----------------------------------
		python washer.py