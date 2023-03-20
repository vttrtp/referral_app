# Django Referral App

This is a Django application that allows you to create a referral system 
that computes referral levels and bonuses depending on the referral user level.

## Installation and running

1. Clone repository
  ```code bash
  git clone https://github.com/vttrtp/referral_app.git
  ```
2. Change into the project directory:
  ```code bash
  cd referral_app
  ```
3. Install the required dependencies:
  ```code bash
  pip3 install -r requirements.txt
  ```
4. Run database migrations
  ```code bash
  python3 manage.py migrate
  ```
5. Import data
```code bash
 python3 manage.py import_data data/data.json
 ```
6. Start server
```code bash
python3 manage.py runserver
```

## Web API

To retrieve a single ReferralUser instance by its ID please make a Get request to `http://127.0.0.1:8000/api/referral-users`.
For example http://127.0.0.1:8000/api/referral-users/01GTXNX97R9RRQ4JYVECEVA081

## Running Tests

To execute tests please run:
```code bash
python3 manage.py test
```