# Online Webstore
- Minh Bui (@cwcoga123)
- Jeffrey Ellison (@Jeff-SJSU) or (@AlpyneDreams)
- Anh Nguyen (@AnhNguyen618)
- Richard Chan (@rchan119)

Team Lead: Jeffrey Ellison

# Introduction
 website will allow the user to access a web store with a personalized account.
The format of the site will follow a basic web store, where the user must log in to their
own account in order to access the various functions of the site.

# Instructions
After downloading the package from github, use pip to install flask and flask_sqlalchemy with the follow commands in terminal:
 - pip install flask
 - pip install flask_sqlalchemy
- Run the main.py file in the package
- Copy and paste the web address from the terminal to a web browser

# Web Navigation
Once the account is created, a confirmation message should appear (not implemented yet). The user will be automatically logged in upon creating the
account for the first time. Currently, the default redirection will be back to the home page. The user can go to their account profile to change their
profile pictures or any of their account information by changing their information in the textbox or upload a new picture. The user also has the
ability to delete their account, while will remove them from the system. 

The webstore portion of the site should be accessible regardless of login status. The home page contains all of the seller items that is available for purchase.
The user can then click on each individual item to see further information about the item and an increased image size. The user can then add the item to their checkout
cart. If they are not logged in before adding an item, the system will prompt the user to login, or register if they do not have an account. 

Most of the current functions are tested for debugging and as a proof of concept which require more fine tuning and minor adjustments and 
only the basic functions work completely. 
