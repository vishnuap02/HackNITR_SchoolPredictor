from flask import Flask, redirect, url_for, request , jsonify ,make_response
import pymongo
import certifi
import requests
from data_helper import tweet_sentiment
from urllib.parse import quote_plus

app = Flask(__name__)

def connect_db():
    

    client = pymongo.MongoClient("mongodb+srv://username:pw@cluster0.cnrej4y.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=certifi.where())


    dbname = client['hacknitr']
    return dbname
    # Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection)



@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

# below are CRUD operation for school list.
@app.route('/store_school',methods = ['POST'])
def store_school():
   dbname = connect_db()
   collection_name = dbname["school"]
   school_data = {}
    # getting arguments from request to store them.
   school_data["school_name"] = request.args.get('school_name')
   school_data["website"] = request.args.get('website')
   school_data["address"] = request.args.get("address")
   school_data["city"] = request.args.get("city")
   school_data["pin_code"] = request.args.get("pin_code")
   school_data["ph_no"] = request.args.get("ph_no")
   school_data["is_main_branch"] = request.args.get("is_main_branch")
   school_data["email"] = request.args.get("email")
   school_data["school_number"] = request.args.get("school_number")
   school_data["fees"] = request.args.get("fees")
   # Below Courses is provided with 'comma separated string' from frontend , and converted to list in backend.
   courses=request.args.get("courses")
   school_data["courses"] = courses.split(',')

   # below function assigns a score to this school based on 'Tweeter scrapping' which uses twitter apis , sentiment analysis
   # method from mltk and pandas
   school_data["score"] = tweet_sentiment(school_data["school_name"])

   collection_name.insert_one(school_data)
   return redirect(url_for('success',name = school_data["school_name"]))

@app.route('/get_school_list',methods = ['GET'])
def get_school_list():
    dbname = connect_db()
    collection_name = dbname["school"]
    school_list = collection_name.find({})
    schools = []
    ctr = 1
    for r in school_list:
        # print(r)
        del r['_id']
        # if courses are there in data , then dont display in list
        if 'courses' in r:
            del r['courses']
        schools.append(r)
    response = make_response(jsonify(schools), 201, )
    return response

@app.route('/get_school_by_id/<school_number>',methods = ['GET'])
def get_school_by_id(school_number):
    dbname = connect_db()
    collection_name = dbname["school"]
    school_list = collection_name.find({})
    school=None
    for r in school_list:
        if r['school_number']==school_number:
            school=r
    response = make_response(jsonify(school), 201, )
    return response

@app.route('/delete_school/<school_number>', methods=['DELETE'])
def delete_school(school_number):
    dbname = connect_db()
    collection_name = dbname["school"]
    school_list = collection_name.find({})
    present = -1
    for r in school_list:
        if r['school_number'] == school_number:
            present=1
    if present==-1:
        message = school_number + " not present!"
    else:
        collection_name.delete_one({'school_number':school_number})
        message = school_number+" deleted!"
    return make_response(jsonify({"message": message}), 201,)

# Below are functions supporting search.

# for the below url to use , in frontend any parameter can be used
# more than one condition is also acceptable.
@app.route('/search_school/',methods = ['GET'])
def search_school():
    args = request.args
    args = args.to_dict() #getting the parameters and values which are passed in dictionary args.
    dbname = connect_db()
    collection_name = dbname["school"]
    school_list = collection_name.find({})
    school=[]
    for r in school_list:
        truth = True
        for key,value in args.items():
                # if every value matches with corresponding entry , then we can consider
                if r[key]!=value:
                    truth=False
                    break
        if truth==True:
            del r['_id']
            school.append(r)

    response = make_response(jsonify(school), 201, )
    return response

if __name__ == '__main__':
   app.run(debug = True)

# tried for general web scrapper which is not possible as classes and ids are different

# THe below helped me solve the 'CERTIFICATE_VERIFY_FAILED' and CERTIFICATE_EXPIRED error
# Here is what worked for me (Windows 11) -
#
# heck that dnspython, pymongo and certifi are installed in your virtual environment or install them by:
#
# pip install dnspython pymongo certifi
# Can you use the terminal/command line and run Python, in the Python environment can you enter and = run the following commands (please change the password as appropriate for your user in your Atlas cluster):
