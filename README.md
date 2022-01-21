# Mini_Ecom_API
Mini_Ecom_Api using Django Rest Framework


#Project Setup
1. Create virtual environment using python3 -m venv env
2. activate the environment
3. Install Dependencies using pip Install -r requirement.txt
4. makemigrations - python manage.py makemigrations
5. migrate - python manange.py migrate
6. runserver - ptyhon manage.py runserver

Your APIs Are Ready to serve now

urls :

http://localhost:8000/api/register/ - Customer can Register them -POST Request // No Authentication

http://localhost:8000/api/adminview/ - Admin Can Create shop and view all users - GET/POST //  Basic Authentication Username and password

http://localhost:8000/api/shops/ - Shops can create their services -POST // customer and shops view services - GET // Basic Authentication Username and password

http://localhost:8000/api/wallet/ - Customer can add money to wallet and view balance and statement - GET/POST // Basic Authentication Username and password

http://localhost:8000/api/bookings - Customer can create bookings and Shops can view their related bookings - GET/POST // Basic Authentication Username and password
