"""
    Routes Configuration File

    Put Routing rules here
"""
from system.core.router import routes

"""
    This is where you define routes
    
    Start by defining the default controller
    Pylot will look for the index method in the default controller to handle the base route

    Pylot will also automatically generate routes that resemble: '/controller/method/parameters'
    For example if you had a products controller with an add method that took one parameter 
    named id the automatically generated url would be '/products/add/<id>'
    The automatically generated routes respond to all of the http verbs (GET, POST, PUT, PATCH, DELETE)
"""
routes['default_controller'] = 'Users'
routes['GET']['/signin'] = 'Users#signin'
routes['GET']['/register'] = 'Users#register'
routes['POST']['/add_user'] = 'Users#add_user'
routes['GET']['/dashboard'] = 'Users#dashboard'
routes['GET']['/dashboard/admin'] = 'Users#dashboard_admin'
routes['POST']['/do_signin'] = 'Users#do_signin'
routes['GET']['/signoff'] = 'Users#signoff'
routes['GET']['/users/new'] = 'Users#new'
routes['GET']['/users/edit'] = 'Users#edit'
routes['POST']['/users/self_update'] = 'Users#self_update'
routes['GET']['/users/edit/<int:id>'] = 'Users#edit_user'
routes['POST']['/users/admin_update/<int:id>'] = 'Users#admin_update'
routes['GET']['/users/show/<int:id>'] = 'Users#show'
routes['POST']['/users/message/<int:id>'] = 'Users#message'
routes['POST']['/users/comment/<int:user_id>/<int:message_id>'] = 'Users#comment'
routes['GET']['/users/delete/<int:id>'] = 'Users#delete'


"""
    You can add routes and specify their handlers as follows:

    routes['VERB']['/URL/GOES/HERE'] = 'Controller#method'

    Note the '#' symbol to specify the controller method to use.
    Note the preceding slash in the url.
    Note that the http verb must be specified in ALL CAPS.
    
    If the http verb is not provided pylot will assume that you want the 'GET' verb.

    You can also use route parameters by using the angled brackets like so:
    routes['PUT']['/users/<int:id>'] = 'users#update'

    Note that the parameter can have a specified type (int, string, float, path). 
    If the type is not specified it will default to string

    Here is an example of the restful routes for users:

    routes['GET']['/users'] = 'users#index'
    routes['GET']['/users/new'] = 'users#new'
    routes['POST']['/users'] = 'users#create'
    routes['GET']['/users/<int:id>'] = 'users#show'
    routes['GET']['/users/<int:id>/edit' = 'users#edit'
    routes['PATCH']['/users/<int:id>'] = 'users#update'
    routes['DELETE']['/users/<int:id>'] = 'users#destroy'
"""
