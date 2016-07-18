from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')

   
    def index(self):
        return self.load_view('/users/index.html')

    def signin(self):
        return self.load_view('/users/signin.html')

    def register(self):
        return self.load_view('/users/register.html')

    def signoff(self):
        session.clear()
        return redirect('/')

    def do_signin(self):
        info = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        login_status = self.models['User'].do_signin(info)
        if login_status['status'] == False:
            flash(login_status['error'])
            return redirect('/signin')
        else:
            session['id'] = login_status['id']
            session['user_level'] = login_status['level']
            return redirect('/dashboard')

    def add_user(self):
        info = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email'],
            'password' : request.form['password'],
            'conf_password': request.form['conf_password']
        }
        add_status = self.models['User'].add_user(info)
        if add_status['status'] == False:
            for error in add_status['errors']:
                flash(error)
            if 'id' not in session:
                return redirect('/register')
            else:
                return redirect('/users/new')
        else:
            if 'id' not in session:
                session['id'] = add_status['id']
                session['user_level'] = add_status['level']
            return redirect('/dashboard')

    def dashboard(self):
        if 'id' not in session:
            return redirect('/')
        if session['user_level'] == 'admin' :
            return redirect('/dashboard/admin')
        else:
            users = self.models['User'].get_all_users()
            return self.load_view('/users/dashboard.html', users = users)

    def dashboard_admin(self):
        if 'id' not in session:
            return redirect('/')
        if session['user_level'] == 'normal' :
            return redirect('/dashboard')
        else:
            users = self.models['User'].get_all_users()
            return self.load_view('/users/dashboard_admin.html', users = users)

    def new(self):
        return self.load_view('/users/new.html')

    def edit(self):
        user = self.models['User'].get_user_by_id(session['id'])
        return self.load_view('/users/edit.html', user = user)

    def edit_user(self, id):
        if session['user_level'] == 'normal':
            return redirect ('/dashboard')
        user = self.models['User'].get_user_by_id(id)
        return self.load_view('/users/edit_user.html', user = user)

    def self_update(self):
        #do different things based on what we want to update
        edit_type = request.form['edit']
        #editing information
        if edit_type == 'info':
            info = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'user_level': session['user_level']
            }
            update_status = self.models['User'].update_info(info, session['id'])
            if update_status['status'] == False:
                for error in update_status['errors']:
                    flash(error, 'info')
                return redirect('/users/edit')
            else:
                return redirect('/dashboard')
        #editing password
        if edit_type == 'password':
            info = {
                'password': request.form['password'],
                'conf_password': request.form['conf_password']
            }
            update_status = self.models['User'].update_password(info, session['id'])
            if update_status['status'] == False:
                for error in update_status['errors']:
                    flash(error, 'password')
                return redirect('/users/edit')
            else:
                return redirect('/dashboard')
        #editing description
        if edit_type == 'description':
            info = {'description': request.form['description']}
            self.models['User'].update_description(info, session['id'])
            return redirect('/dashboard')

    def admin_update(self, id):
        #do different things based on what we want to update
        edit_type = request.form['edit']
        #editing information
        if edit_type == 'info':
            info = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'user_level': request.form['user_level']
            }
            update_status = self.models['User'].update_info(info, id)
            if update_status['status'] == False:
                for error in update_status['errors']:
                    flash(error, 'info')
                return redirect("/users/edit/" + str(id))
            else:
                return redirect('/dashboard/admin')
        #editing password
        if edit_type == 'password':
            info = {
                'password': request.form['password'],
                'conf_password': request.form['conf_password']
            }
            update_status = self.models['User'].update_password(info, id)
            if update_status['status'] == False:
                for error in update_status['errors']:
                    flash(error, 'password')
                return redirect('/users/edit/' + str(id))
            else:
                return redirect('/dashboard/admin')

    def show(self, id):
        user = self.models['User'].get_user_by_id(id)
        messages = self.models['User'].get_messages(id)
        comments = self.models['User'].get_comments(id)
        return self.load_view('/users/show.html', user = user, messages = messages, comments = comments)

    def message(self, id):
        info = {
            'from_id': session['id'],
            'to_id': id,
            'message': request.form['message']
        }
        self.models['User'].add_message(info)
        return redirect('/users/show/' + str(id))

    def comment(self, user_id, message_id):
        info = {
            'message_id' : message_id,
            'user_id' : session['id'],
            'content' : request.form['comment']
        }
        self.models['User'].add_comment(info)
        return redirect('/users/show/' + str(user_id))

    def delete(self, id):
        if session['user_level'] == 'normal':
            return redirect('/dashboard')
        self.models['User'].delete_user(id)
        return redirect('/dashboard/admin')

