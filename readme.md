# To-do
should not read multiple faces
if it fales to read face give option screen as..:
    need to implemnt sec. quesion on the main page as well->for this need to implement register security qestions:
        1. sec. questions
        2. otp


# to solve
read the one face

# future update
what we can add for multiple data is each user is going to keep a code of 5 digits which they can use to manage their data...once they enter that data the current login window will pop up and it will give hime the choice if he wants to log in through face or sec. questions....if he fails on both then otp screen will be opened giving them 3 tries and send the code on their registered mobile number

if this process fails his card will be blocked...and a msg will be sent on his mobile that he need to visit the bank for verification if he failes to do this within a given time frame then his card will be perma blocked

# done
1. read the face and story it into a new a dir face_data in the form of jpg.
2. for init face_unlock just matches the face and writes welcome user.
3. stores data for a face
4. both face_unlock and face_reg can be accessed from main.py in a tkinter gui
5. upon successful log in it shows log in successful