# Railway Ticket Management System

Endpoint APIs for Railway Ticket Management.
This Project uses Django Framework, Django RESTFramework, PostgreSql for Database and has Token based authentication for Customer.
For admin we have to generate an API Key that has to be used each time an API of admin is used.
To test the APIs I have used thunder extension in VSCode.
Different Endpoints are: 
* Register
* Login
* Logout
* Add Train (For Admin Only with an API key)
* Get Booking Details
* Reserve Seat
* Seat Availability
---
# Video Explanation of the working of the API 




https://github.com/sukhleen-kaur-27/IRCTC-ticket-management-system/assets/74076814/d065869f-2f47-4c05-bd95-e11ae93e3f2f

---
# How to use the API and what details are needed :
* Register API :
   * To be able to register we have share the username, email and password in the Body of the HTTPRequest.
   * Example : {"username":"Sukhleen", "email":"sukh@gmail.com", "password":"hello@123"}
   * The email address has to be unique as this is unique field in the Model.
* Login API :
   * For login you have to use the username and password used during the registeration process.
   * Example: {"username":"Sukhleen", "password":"hello123@gmail.com"}
   * This API endpoint returns a token, we will be using the same token each time we send a new request.
* Logout :
   * Just share the token in the header and you'll be logged out.
   * Once logged out token expires.
   * Example : In the header section use:
      Authorization : token "Your_token"
* Add Train :
   * This is only for admin to use.
   * We have to share the API Key in the header:
      Authorization : Api-Key "Your_Api_key"
   * In the body we have send the train details:
      { "train_number" : "TR1",
        "departureCity" : "Delhi",
        "arrivalCity" : "Gwalior",
        "dateOfDeparture" : "2023-08-12",
        "timeOfDeparture": "10:22:00",
        "timeOfArrival" : "20:22:00",
        "numberOfSeats" : "2"
       }
* Seat Availability  :
   * This is used to get the details of a train between two stations.
   * We have to share the token in the header in order to access this API.
   * Body will look something like this:
     {"departureCity":"Delhi", "arrivalCity" : "Gwalior", "dateOfDeparture":"2023-08-12"}
   * Output will the trains and the number of seat available in those trains.
* Reserve Seat :
   * Used to reserve a seat in a train.
   * Again share the token.
   * Body looks something like this :
      {"train_number":"TR1", "email":"hello123@gmail.com"}
   * Returns the reservation id
* Get Booking Details :
   * Used to get the details of the ticket once seat is booked.
   * share the token
   * body will look something like this:
       {"train_number":"TR1", "email":"hello123@gmail.com"}

   * Returns the details of the user and the train both.

---

# How to use this project on your system?

* Use the requirements.txt to install all the libraries and frameworks
* Set up your virtual environment
* Make sure you have Python installed in your system.
* To test the APIs use thunder extension in VSCode (this is the one I'm using in the video)
* Go to your terminal and activate your virtual envitronment.
* Type : "pip install -r requirements.txt" to install all the dependencies and it should work like magic.
  

 PS : If you have any questions you can ping me on sukhleenkaur2709@gmail.com

     
      
  

