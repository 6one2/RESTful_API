# Stores RESTful Api with authentication

RESTful app for managing online store with Python, Flask and Flask extensions (-RESTful, -JWT, -SQLAlchemy).
 - access SQL database for user authentication and items management (using SQLAlchemy)
 - handle secure user registration and authentication with Flask

 The app is deployed on [heroku](https://restful-api-store.herokuapp.com/)

 ## Use (with [postman](https://www.postman.com))
  * Register User @ /register
  * Login @ /login
  * Logout @ /logout

  ### this requires 'fresh' login
  * Create/Update/Delete store with name, and store_id @ /store
  * Create/Update/Delete item with name, price and store_id @ /item

  ### this requires login
  * Check items list @ /items
  * Check stores list @ /stores
