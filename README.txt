Code adopted from tutorials.
Validated PEP8 by Sublime AutoPep8 plugin
1) The Database has been populated
2) If required, repopulate with populateDB.py
3) To return to Categories, click in the menu bar
4) Login top right
5) Add category top right
6) Other functions, add items, delete etc are context/role specific

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
