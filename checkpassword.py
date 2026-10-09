def password_level(password):
    if len(str(password)) < 6:
        return 'В пароле должно быть не меньше 6 символов'
    elif password.isdigit():
        return 'Пароль не может состоять из чисел'
    elif password.isalpha() and password.islower():
        return 'В пароле должны содержаться заглавные буквы'
    elif password.isalpha() and password.isupper():
        return 'В пароле не могут быть только заглавные буквы'
    elif password.isalpha() and not password.isupper():
        return 'В пароле должна содержаться цифра'
    else:
        return '1'
