
# Call Record Details Project
This is a Python project with Django, where is possible record telephone call`s 
data as the time that the call started and the time that it ended. Gathering does 
informations with specific rules to calculate the price of each call, 
is possible to calculate the telephone bill of a number from a spefic month. 

In this project is possible to record the start call, then when the end call is going be registered, is verified if exists a start call with the same call id, if there is the end call is saved. 

When the end call is recorded it will be create a  telephone bill for that call, that is the registration of the duration of the call, the price of that call, the date of the call and another informations. 

With thoses telephone bills is possible to get the bill of a period like (07/2017).

### Heroku
 This project is running on Heroku in the url: https://call-record-details.herokuapp.com/
 To access the admin enter in the https://call-record-details.herokuapp.com/admin/
 with the credentials:
```
username:call-admin
password:call123
```

### Environment of Development 
 * OS: Mac OS
 * IDLE: PyCharm
  
## Project Specifications
* Python==3.6.6
* Django==1.11.4
* dj-database-url==0.5.0
* django-environ==0.4.5
* djangorestframework==3.8.2
* psycopg2-binary==2.7.5
* gunicorn==19.9.0
* python-decouple==3.1
* pytz==2018.5
* whitenoise==3.3.1
* PostgreSQL


## How To Run
to run this project first clone this repository and then:
1. Create a virtualenv and install the requirements
    In the project diretory execute :
    ```
    virtualenv -p python3 venv
    ```
    To install the requirements excute:
    ```
    source venv/bin/activate
    pip3 install -r requeriments.txt
    ```
2. Configure the database config:
    create a file .env and inside it write the database configuration:
    ```
    DATABASE_URL=postgres://<username>:<password>@<ip>:<port>/<database_name>
    ```

3. Create the database:
    Execute the command to run the migrates and create the database
    ```
    python3 manage.py migrate
    ```
4. Execute the project:
    Finally to run the project execute:
    ```
    python3 manage.py runserver
    ```
    
5. Create a user to django admin (optinal)
    If you want to verify the data from a insterface, create a super user to access django admin:
    ```
    python3 manage.py createsuperuser
    ```
    After that access the url  in the browser and enter the credentials
    ```
     <ip>:<port>/admin/
    ```
   
6. Run the tests:
	    Execute the command to run the tests
	```
	python3 manage.py test call_record
	python3 manage.pt test telephone_bill
	```
	  Those tests will test models, vies and functions for each app in the project

## API Endpoints


* `POST` record/record_call/ :
	* Register the beginning of a call
	* Data  :
	```
	{
	  call_id:(integer with the call id)
	  type: (if is the start call register type must be 0, if is the end call register type must be 1)
	  timestamp:(must be string in this format: "2016-02-29T14:00:00Z")
	  source:(string with the source number)
	  destination:(string with the destination number)
	}
	```
* `POST` record/record_call/ :
	* Register the end of a call
	* Data:
	```
		{
	  call_id:(integer with the call id)
	  type: (if is the start call register type must be 0, if is the end call register type must be 1)
	  timestamp:(must be string in this format: "2016-02-29T14:00:00Z")
	}
	```

* `GET` telephone_bill/telephone_call_bill/:
	* get all the telephone call bills

* `POST` telephone_bill/telephone_call_bill/get_telehephone_bill/:
	* get the total telephone bill of a period
	* Data:
	```
	{
	period:(string with the month and year like this "12/2017" -optional: if there is no key period it will be considered the actual period)
	number:(string with the bill`s phone number)
	}
	```


