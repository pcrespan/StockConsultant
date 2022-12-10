# StockConsultant

## Disclaimer
Project made for educational purposes only, I'm not responsible for how the code is used. The mere presence of this code on my profile does not imply that I encourage scraping the website referenced in the code. The source code only help illustrate the technique behind creating an API that returns information scraped from a website. This API should not be hosted publically, as Yahoo Finance does not allow its data to be shown outside of the website.

## Description
Stock Consultant is an API written in Python using `Flask`, `BeautifulSoup` and `PyJWT`, as well as PostgreSQL as its database. The project was made for my learning purposes regarding how to create an API using JWT tokens as authentication.

## Usage
The register process should be done on the website hosted locally. The user should Log In already inside of the app that will consume the API. A POST request containing username and password should be sent to http://127.0.0.1:5000/login - assuming the user will host locally with `Flask`. The response of that request will be a JSON containing the JWT token, which should be sent to the server in another POST request containing the token inside of `accessToken` JSON variable, as well as `stockSymbol`, which represents the stock symbol chosen by the user.

### Example - using `curl` command

```
curl -X POST -d "username=<user>&password=<password>" http://127.0.0.1:5000/login
```

The command will return a response from the server, which will be the token.

```
curl -X POST -d "accessToken=<token>&stockSymbol=<symbol>" http://127.0.0.1/quote
```

The command will return all the information regarding the stock
