from controllers.auth import get_hashed_password

password = input('Password: ')

print(get_hashed_password(password))
