# Video presentation
https://drive.google.com/file/d/150v5MkgzrNY2MqgMGySWMruEDS9Q3FIS/view?usp=sharing
# How to run

To run the application you have to run the app.py file in the application folder, then you go to localhost:5000 in a browser.

# Testing instructions

## Usernames and passwords

| **Username** | **Password** |   **Role**  |
|:------------:|:------------:|:-----------:|
|    johndoe   |    Joe123    | normal user |
|   maryjane   |   LoveDogs   | normal user |
|     admin    |   admin123   |    admin    |

## Admin

If a user has the role of "admin" they can acces the route "/admin"

# Functionality

- Users can register accounts.
  - The username has to be 3-10 characters long and can only contain numbers and letters.
  - The password must be at least 5 characters long and have at least 1 letter, it can only contain numbers and letters.
  - The user must confirm the password by retyping it.
  - If any of these validations fail an error is displayed.
  - These validation is done both client- and server-side.
- Users can login to an account.
  - If the password or username is incorrect an error is displayed.
- The home page is a list of all the products stored in the database.
  - Users can search for specific products
  - The users can choose to sort the products by price, name and relevance to the search word if there is one.
    - Sort prefrences are stored in a cookie and is present when user revisits the page.
- Clicking on a product takes you to its product page.
  - On the product page users can select a quantity and add it to their cart.
    - If the item is already in the cart it gets replaced.
- On both the home page and product page there is a summary of the cart with the last five items added.
- On the cart page there is a table with all the items in the cart and a checkout form.
  - If the user is logged in, their cart is stored in the database.
  - If the user is not logged in, the cart is stored in a cookie.
  - If the user has items in their cart without being logged in and registers an account, the cart gets added to the account.
  - Users can update the quantity and delete items from their cart.
    - The quantity must be between 1 and 99, if it is below 1 the quantity is set to 1 and if its above 99 it is set to 99.
  - In the checkout form, users must fill in billing details and adress
    - All the fields must be filled
    - Email must be in the format "email@example.org"
    - Postalcode must be 4 numbers
    - Users must agree to the terms of service
    - If any of the above validations fail an error is displayed.
    - Validations are done client- and server-side
    - When the form is submitted it gets stored in the database, and all items from the cart gets deleted.
- The admin page ("/admin") can only be accessed by users with the role "admin"
  - If a user accesses the page without the role "admin" a message saying "You do not have access to this page" is displayed.
  - In the admin page users can add, update and delete products from the database.
    - The name and price must be filled and the price must be more than 0
    - There must be an image if a product is being added, not if its being updated then it will use the old image.
    - The image must be in the "jpg" or "png" file format.
    - The image size must be less than 100Kb.
    - ⚠️ Due to browser caching, you may have to reload the page to update the image client-side when you update the image of a product.
  - There is a preview of how the product should look on the home page.
  - If a user somehow accesses the product editing without the role "admin" they cannot edit anything since the server also checks their role.
    
