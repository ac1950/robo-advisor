# robo-advisor

### Prerequisites
`+ Anacoda 3.7`
`+ Python 3.7`
`+ Pip`

### Setup
"Use GitHub Desktop software or the command-line to download or "clone" this repository onto your computer. Choose a familiar download location like the Desktop" 


"After cloning the repo, navigate there from the command-line:"

` cd ~/Desktop/robo-advisory `

### Security Requirements
"This program utlizes the AlphaVantage API (https://www.alphavantage.co/)"
"This API should not be included within the sourcecode. Instead, you should set an environment variable called ALPHAVANTAGE_API_KEY, and your program should read the API Key from this environment variable at run-time."
"To do this create a file called ".env" and place the following inside with your specific API key:"
` ALPHAVANTAGE_API_KEY = "abc123" `


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



