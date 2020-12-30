import pyrebase
firebaseConfig= {
    "apiKey": "AIzaSyBc5DKY5tX6IcnmWHytncW_YmQyDGs4ftk",
    "authDomain": "test-e241b.firebaseapp.com",
    "databaseURL": "https://test-e241b-default-rtdb.firebaseio.com",
    "projectId": "test-e241b",
    "storageBucket": "test-e241b.appspot.com",
    "messagingSenderId": "776000540974",
    "appId": "1:776000540974:web:d7a8b6fde7e6840643aabf",
    "measurementId": "G-30Z43DKCZ8"
  }
firebase =pyrebase.initialize_app(firebaseConfig)

db=firebase.database()
auth=firebase.auth()
#AUTH
email=input("Enter email")
password=input("Enter password")
try:
    auth.sign_in_with_email_and_password(email,password)
    print("Successfully Signed in ") 
except:
    print("Invalid Username or Password")
key_email=email.replace('@', '').replace('.', '')
data= {'name':"Neel", 'location':'Bangalore','area': '12345', 'crop': 'Maize'}
db.child("users").child(key_email).push(data)

#QUERY
people = db.child("users").get()
for person in people.each():
    if(person.key()=='dummyexamplecom'):
        print(person.val())


