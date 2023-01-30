# HackNITR_SchoolPredictor
Being developed during hackathon by NIT-Roorkie's HackNITR . This provides APIs for storing , managing and searching schools based on various indicators.
This is developed using Flask framework for processing request , pandas for data handling and tweepy for tweets rating as positive or negative.

This contains only Backend part (using python).

# Backend:
The features supported are:
1) Creating school records.
Using POST request in Postman to create new record. The request being :
http://127.0.0.1:5000/store_school?school_name=Fiitjee High School&address=Dollars colony&city=Bangalore&pin_code=560325&ph_no=6656655411&is_main_branch=yes&email=greenwoodhigh@gmail.om&school_number=21436547103&fees=190000&courses=Billiards , swimming , shooting , Science , History
This is reflected in Cloud database once logged-in and Cluster is created in which the DB is present in mongodbonline.

2) While school is created it is being rated using twitter scraping.
This uses Tweepy package to retrieve all tweets with a particular result based on keyword.

3) Records created are stored in MongoDB cloud.


4) Getting school list : from cloud DB
using API, 
http://127.0.0.1:5000/get_school_list

5) Getting details about a existing school using any of parameters like city or address ...
http://127.0.0.1:5000/search_school?address=Bangalore


6) Delete school by unique school number.
127.0.0.1:5000/delete_school/21436547895

