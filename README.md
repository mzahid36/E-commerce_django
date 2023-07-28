# E-commerce Website using Django Framework

**Features :**
- User Creation 
- User Authentication & Authorization
- Cart
- Password Change
- Forget Password
- Search Product
- Category-wise Filtering

**Development Tools :**
+ Framework
    - Django 4.2
+ Code Editor
    - VsCode 1.80.1
+ Database
    - SQLite
+ Required Libraries
    - Pillow 9.5.0

**Project Documentation :** The **"Ecommerce"** directory consists of "settings.py", if a new app is created please ensure that you have included the app name there. **"Media"** directory holds all the images uploaded via django-admin(dashboard). All the project essential files (Static & templates) are stored inside **"Shop"** directory,an app of this particular project. 

**How to Run :**
Please follow the below instructions to run this project in your machine:
1. Clone the repository
    ```sh
    git clone https://github.com/mzahid36/E-commerce_django.git
    ```
2. Intall necessary libraries.
3. To access the dashboard, please create a superuser.
   ```sh
    python manage.py createsuperuser
    ```
4. To run the project
   ```sh
    python manage.py runserver
    ```