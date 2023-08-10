# Inst scraper

This is a service for scraping urls of pics.


## Requirements

To start working with the service, firstly you need to: 

1. Clone it to your machine.
2. Create an .env file consisting of following variables:

```bash 
PARSER_PROFILE_USERNAME=Inst profile username that is used to login
PARSER_PROFILE_PASSWORD=Password to this profile
```

## Run
1. Move to docker folder

```bash
cd docker
```

2. Run

```bash
docker-compose up
```

## Test

There is a Test client that sends multiple queries at once.

Python3 should be already installed.  
To start working with the client, firstly you need to: 

1. Create a virtual environment using

```bash 
python3 -m venv venv
```

2. Activate this environment using

```bash
source venv/bin/activate
```

3. Install dependencies using

```bash
pip3 install -r requirements.txt
```

4. Run

```bash
python3 test_client.py
```
