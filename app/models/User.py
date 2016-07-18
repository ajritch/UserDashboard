""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()


    def add_user(self, info):
        #check: will this be the first user added? if so, make admin
        users = self.db.query_db("SELECT * FROM users")
        if len(users) == 0:
            level = 'admin'
        else: 
            level = 'normal'

        errors = []
        #check: has this email already been entered?
        query = "SELECT * FROM users WHERE email = :email"
        data = {'email': info['email']}
        user = self.db.query_db(query, data)
        if len(user) > 0:
            errors.append("That email address has already been registered.")
        #standard validations
        if not EMAIL_REGEX.match(info['email']):
            errors.append("Invalid email address.")
        if len(info['first_name']) < 2 or len(info['last_name']) < 2:
            errors.append("Name fields must contain at least 2 letters.")
        if not info['first_name'].isalpha() or not info['last_name'].isalpha():
            errors.append("Name fields must only contain letters.")
        if len(info['password']) < 8:
            errors.append('Password must contain at least 8 characters.')
        if not re.compile(r'\d').search(info['password']):
            errors.append("Password must contain at least 1 number.")
        if info['password'] != info['conf_password']:
            errors.append("Confirmation password must match password.")

        if errors:
            return {'status': False, 'errors': errors}
        else:
            query = ("INSERT INTO users " +
                    "(first_name, last_name, email, password, user_level, created_at, updated_at) " +
                    "VALUES (:first_name, :last_name, :email, :password, :user_level, NOW(), NOW())")
            data = {
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'email': info['email'],
                'password': self.bcrypt.generate_password_hash(info['password']),
                'user_level': level
            }
            new_id = self.db.query_db(query, data)
            return {'status': True, 'id': new_id, 'level': level}


    def get_all_users(self):
        return self.db.query_db("SELECT * FROM users")

    def do_signin(self, info):
        #get info from database
        query = "SELECT * FROM users WHERE email = :email"
        data = {'email': info['email']}
        user = self.db.query_db(query, data)
        #is the email registered yet?
        if len(user) == 0:
            return {'status': False, 'error': "That email is not registered to a user."}
        #does the entered password match?
        if not self.bcrypt.check_password_hash(user[0]['password'], info['password']):
            return {'status': False, 'error': "Incorrect password."}
        else:
            return {'status': True, 'id': user[0]['id'], 'level': user[0]['user_level']}

    def get_user_by_id(self, id):
        query = "SELECT * FROM users WHERE id = :id"
        data = {'id': id}
        user = self.db.query_db(query, data)
        return user[0]

    def update_info(self, info, id):
        #first, perform some validations:
        valid = True
        errors = []
        #check: has this email already been entered by another user?
        query = "SELECT email FROM users WHERE email = :email AND NOT (id = :id)"
        data = {
            'email': info['email'],
            'id': id
        }
        emails = self.db.query_db(query, data)
        if len(emails) > 0:
            errors.append("That email address is registered to another user.")
        #standard validations
        if not EMAIL_REGEX.match(info['email']):
            errors.append("Invalid email address.")
        if len(info['first_name']) < 2 or len(info['last_name']) < 2:
            errors.append("Name fields must contain at least 2 letters.")
        if not info['first_name'].isalpha() or not info['last_name'].isalpha():
            errors.append("Name fields must only contain letters.")
        if errors:
            return {'status': False, 'errors': errors}
        else:
            query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email, user_level = :user_level WHERE id = :id" 
            data = {
                'first_name': info['first_name'],
                'last_name': info['last_name'],
                'email': info['email'],
                'user_level': info['user_level'],
                'id': id
            }
            self.db.query_db(query, data)
            return {'status': True}

    def update_password(self, info, id):
        valid = True
        errors = []
        if len(info['password']) < 8:
            errors.append('Password must contain at least 8 characters.')
        if not re.compile(r'\d').search(info['password']):
            errors.append("Password must contain at least 1 number.")
        if info['password'] != info['conf_password']:
            errors.append("Confirmation password must match password.")

        if errors:
            return {'status': False, 'errors': errors}
        else:
            query = "UPDATE users SET password = :password WHERE id = :id"
            data = {
                'password': self.bcrypt.generate_password_hash(info['password']),
                'id': id
            }
            self.db.query_db(query, data)
            return {'status': True}

    def update_description(self, info, id):
        query = "UPDATE users SET description = :description WHERE id = :id"
        data = {
            'description': info['description'],
            'id': id
        }
        return self.db.query_db(query, data)

    def add_message(self, info):
        query = ("INSERT INTO messages " +
                "(content, created_at, to_user_id, from_user_id) " +
                "VALUES (:message, NOW(), :to_user_id, :from_user_id)")
        data = {
            'message': info['message'],
            'to_user_id': info['to_id'],
            'from_user_id': info['from_id']
        }
        return self.db.query_db(query, data)

    def get_messages(self, id):
        query = ("SELECT messages.id, content, messages.created_at, first_name, last_name, from_user_id FROM messages " +
                "JOIN users ON messages.from_user_id = users.id " +
                "WHERE to_user_id = :to_user_id ORDER BY created_at DESC")
        data = {'to_user_id': id}
        return self.db.query_db(query, data)

    def add_comment(self, info):
        query = ("INSERT INTO comments " +
                "(content, created_at, message_id, user_id) " +
                "VALUES (:comment, NOW(), :message_id, :user_id)")
        data = {
            'comment': info['content'],
            'message_id': info['message_id'],
            'user_id': info['user_id']
        }
        return self.db.query_db(query, data)

    def get_comments(self, id):
        query = ("SELECT comments.id, message_id, comments.content, comments.created_at, first_name, last_name, messages.to_user_id, comments.user_id " +
                "FROM messages JOIN comments ON messages.id = comments.message_id " +
                "JOIN users ON comments.user_id = users.id " +
                "WHERE messages.to_user_id = :id")
        data = {'id': id}
        return self.db.query_db(query, data)

    def delete_user(id):
        query = "DELETE FROM comments WHERE user_id = :id"
        query2 = "DELETE FROM messages WHERE from_user_id = :id OR to_user_id = :id"
        query3 = "DELETE FROM users WHERE id = :id"
        data = {'id': id}
        self.db.query_db(query, data)
        self.db.query_db(query2, data)
        return self.db.query_db(query3, data)

    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """