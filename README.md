# API_REST

API REST with Flask where you can insert, queried, delete... restaurants on a PostgreSQL DB, the restaurant name, the street and food. Then you have all the HTTP methods:
  - localhost/API/insert/name/street/food  --> Insert a restaurant through the url
  - localhost/API/insert_restaurante --> insert a record with a JSON {'nombre':'name','calle':'street','comida':'food'}
  - localhost/API/restaurante/id --> return a JSON with the restaurant by your id 
  - localhost/API/get_restaurantes --> show all the restaurants saved in a JSON format
  - localhost/API/delete_restaurante/id --> delete the restaurant by your id


  
