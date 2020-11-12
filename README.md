# API_REST

this project is located on Heroku web in the url: api-rest-dev.heroku.com
This project has two parts:

first -> you have a web form for insert and queried all the restaurants that you want through api-rest-dev.heroku.com

second -> there are created an API REST where you can insert restaurants on a PostgreSQL DB, the restaurant name, the street and food. Then you have all the HTTP methods:
  - localhost/API/heroku_insert/name/street/food  --> Insert a record through the url
  - localhost/API/insert_restaurante --> insert a record with a JSON {'nombre':'name','calle':'street','comida':'food'}
  - localhost/API/restaurante/id --> return a JSON with the restaurant by your id 
  - localhost/API/get_restaurantes --> show all the restaurants saved in a JSON format
  - localhost/API/delete_restaurante/id --> delete the restaurant by your id


  
