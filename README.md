# robo-advisor

### Prerequisites
`+ Anacoda 3.7`
`+ Python 3.7`
`+ Pip`

### Setup
Use GitHub Desktop software or the command-line to download or "clone" this repository onto your computer. Choose a familiar download location like the Desktop


After cloning the repo, navigate there from the command-line:

` cd ~/Desktop/robo-advisory `

### Security Requirements
This program utlizes the AlphaVantage API (https://www.alphavantage.co/)"
This API should not be included within the sourcecode. Instead, you should set an environment variable called ALPHAVANTAGE_API_KEY, and your program should read the API Key from this environment variable at run-time.
To do this create a file called ".env" and place the following inside with your specific API key:
` ALPHAVANTAGE_API_KEY = "abc123" `

This code should also contain a file called ".gitignore" which will prevent the ".env" file to be read. If this file is not in the repository that you just cloned, create a file called ".gitignore" and place the following contents inside: 
`# .gitignore`

`# ignore secret environment variable values in the ".env" file:`
`.env `


### Environment Setup
Create and activate a unique Anaconda Environment:
`conda create -en stocks-env python=3.7 # (first time only)`
`conda activate stocks-env`


### From within the virtual environment, install the packages specified in the "requirements.txt" file
`pip install -r requirements.txt`

### From within the virtual environment, install requests package
`pip install requests`

### From within the virtual environment, install dotenv
`python-dotenv`

### From wtihin the virtual environment run the code from terminal:
`python robo-advisor.py`

### For SMS Capabilities 
Install `twilio` 

`pip install twilio`

Create a try Twilio account on https://www.twilio.com/try-twilio and request a free phone number

Verify the phone number you want messages sent to enable SMS capabilities 
 - note that if you have upgraded your twilio account you do not need to verify every number you send messages to - 

 Update the content of the ".env" file to specify the following values:

 `TWILIO_ACCOUNT_SID` 

 `TWILIO_AUTH_TOKEN` 

 `SENDER_SMS`

 `RECIPIENT_SMS`




### For Graphing 
From within the Virtual Environment do: 
` pip install matplotlib` 

### Facilated Installation of the Packages
From within the Virtual Environment do: 
` pip install -r requirements.txt` 

### Running the Finished Program
From within the virtual environment, demonstrate your ability to run the Python script from the command-line:
` python app/robo-advisor.py` 


### Testing 
Testing with Pytest Package

Use the command below to use "pytest" package to run a test
` pytest` 


### CI with Code Climate and Travis Working
Travis will check before any merge on github
Codeclimate detects and reviews any commits on the dashboard 
`https://codeclimate.com`