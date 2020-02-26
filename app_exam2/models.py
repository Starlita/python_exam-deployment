from django.db import models
import re
class UserManager(models.Manager):
    def basic_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['first_name']) < 3:
            errors['firstname'] = "First name is too short"
        if len(requestPOST['last_name']) < 3:
            errors['lastname'] = "Last name is too short"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):               
            errors['email'] = "Invalid email address"
        users_with_email = User.objects.filter(email=requestPOST['email'])
        if len(users_with_email) > 0:
            errors['duplicate'] = "Email already taken"
        if len(requestPOST['password']) < 8:
            errors['password'] = "Password is too short"
        if requestPOST['password'] != requestPOST['password_conf']:
            errors['no_match'] = "Password and Password Confirmation must match"
        return errors
    def login_validator(self, requestPOST):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):               
            errors['email'] = "Invalid email address or password"
        return errors
    def edit_validator(self, requestPOST):
        errors ={}
        if len(requestPOST['first_name']) < 1:
            errors['firstname'] = "First name is too short"
        if len(requestPOST['last_name']) < 1:
            errors['lastname'] = "Last name is too short"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):               
            errors['email'] = "Invalid email address"
        return errors



class User(models.Model):
    firstname= models.CharField(max_length= 255)
    lastname= models.CharField(max_length= 255)
    email= models.CharField(max_length= 255)
    password= models.CharField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # thoughts_uploaded= a list of thoughts uploaded by a given user 
    # liked_thoughts= a list of thoughts liked by a given user

class ThoughtManager(models.Manager):
    def basic_validator(self, requestPOST):
        errors = {}
        if len(requestPOST['thought_text']) < 6:
            errors['title'] = "Thought too short"
        return errors


class Thought(models.Model):
    thought_text= models.TextField()
    uploaded_by= models.ForeignKey(User, related_name='thoughts_uploaded', on_delete=models.CASCADE)
    users_who_like= models.ManyToManyField(User, related_name='liked_thoughts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ThoughtManager()

