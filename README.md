# API_REST

this project is located on Heroku web in the url: api-rest-dev.heroku.com
This project has two parts:

first -> there are created an API REST where you can insert restaurants on a PostgreSQL DB, the restaurant name, the street and food. Then you have all the HTTP methods:
  - api-rest-dev.heroku.com/API/heroku_insert/name/street/food  --> Insert a record through the url
  - api-rest-dev.heroku.com/API/insert_restaurante --> insert a record with a JSON {'nombre':'name','calle':'street','comida':'food'}
  - api-rest-dev.heroku.com/API/restaurante/id --> return a JSON with the restaurant by your id 
  - api-rest-dev.heroku.com/API/get_restaurantes --> show all the restaurants saved in a JSON format
  - api-rest-dev.heroku.com/API/delete_restaurante/id --> delete the restaurant by your id

second -> you have a web form for insert and queried all the restaurants that you want
  
