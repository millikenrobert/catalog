Catalog application Version 1.1 - 14/01/2018

Compatibility:
Has been successfully run with Python 2.7.12 only

Versions:
1.0 Initial upload for Udacity review
1.1 Following bugs fixed
	- Pep8 formatting resolved
	- Updated Client_Secrets.json to refer to localhost5000 rather than localhost8000

Description:
The application mocks a sports goods store. The user can browse the categories and then the items inside of them. If the user is logged in, new categories can be added and CRUD actions performed. 

General Usage notes:
1. Clone from github
2. From terminal run "python application.py"
3. Navigate to http://localhost:8000
4. Login can only be performed with Google account only

Other Notes:
	- Code adopted from tutorials.
	- Validated PEP8 by Sublime AutoPep8 plugin
	- The Database has been populated. If required, repopulate with populateDB.py
	- To return to Categories, click in the menu bar
	- Login top right
	- Add category top right
	- Other functions, add items, delete etc are context/role specific

Page Descriptions:
('/api/categories/JSON') - Get all categories in JSON format
('/api/categories/<int:category_id>/items/<int:item_id>/JSON') - Get a single item
('/api/categories/<int:category_id>/items/JSON') - Get all items from center
('/logout') - Log out of signin
('/categories/<int:category_id>/items/<int:item_id>/delete', methods=['GET', 'POST']) - Delete item
('/categories/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST']) - Edit item
('/categories/new/', methods=['GET', 'POST']) - Add new category
('/categories/<int:category_id>/items/new/', methods=['GET', 'POST']) -  Add new item
('/categories/recentItems/') - Show recently added items
('/categories/<int:category_id>/') - Show all items for centre
('/categories/<int:category_id>/items/') - Show all items for centre
('/categories') - Show all categories
('/') - Show all categories
('/gdisconnect') - Disconnect from google
('/gconnect', methods=['POST']) - Connect to google
('/login') - Login to google

Contact Details:
Voice: 888-222-1111
Web Site: www.example.com
Email: example@gmail.com

Copyright information:
No copyright applicable for this application.