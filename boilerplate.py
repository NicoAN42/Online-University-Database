from datetime import datetime
import os
import pymysql.cursors 

class Session:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                              user="root",
                              password="prince",
                              db='UNIVERSITY',
                              port=5005,
                              cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.connection.cursor()
        self.logged_in = False
        self.role = None
        self.current_user=None
    
    def ask_user_action(self, fun_name):
        print("Oops, you entered something wrong or missed something")
        while(True):
            print("1. Retry")
            print("2. Exit")
            choice = input()
            if(choice == "1"):
                fun_name()
                break
            elif(choice == "2"):
                return
            else:
                print("Invalid choice")
        return

    def login_screen(self):
        print("Hello!")
        while True:
            print("1. Login")
            print("2. Sign Up")
            print("3. Exit")

            selection = input()
            if(selection == "1"):
                self.login()
            elif(selection == "2"):
                self.signup()
            elif(selection == "3"):
                break
            else:
                print("Invalid option")

    def user_screen(self):
        while True:
            print("1. BEFRIEND")
            print("2. UPDATE STUDENT INTEREST")
            print("3. SHOW SUBJECTS")
            print("4. EXIT")
            choice = input()
            if(choice == "1"):
                self.add_languageKnown()
            elif(choice == '2'):
                self.update_interest()
            elif(choice == '3'):
                self.show_subject()
            elif(choice == "4"):
                break
            else:
                print("Invalid choice")

    def login(self):
        try:
            UName = input('UserName: ')
            DNumber = int(input('DNumber'))
            Pass = input('Password')
            query = "SELECT Password from `USER` where UserName = '%s' AND DNum = %d" % (UName,DNumber)
            self.cursor.execute(query)
            resultset = self.cursor.fetchone()
            if(not(resultset)):
                print("You need to sign up first")
            else:
                if(resultset['Password'] == Pass):
                    print("Sucessfully logged in")
                    self.current_user = [UName,DNumber]
                    self.user_screen()
                    
                else:
                    print("Authentication failed")
            
        except Exception as e:
            print(e)
        return   
    def signup(self):
        self.add_user()
    
    def admin_screen(self):
        os.system('clear')
        print("Hello!")
        while True:
            
            print("1. Add User")
            print("2. Add Course")
            print("3. Add Subject")
            print("4. Add Language")
            print("5. Exit")

            selection = input()
            if(selection == "1"):
                self.add_user()
            elif(selection == "2"):
                self.add_course()
            elif(selection == "3"):
                self.add_subject()
            elif(selection == "4"):
                self.add_language()
            elif(selection == "5"):
                break
            else:
                print("Invalid option") 
    def add_entry_screen(self):
        return
    def see_available(self):
        return

    # User Actions
    def show_subject(self):
        query= 'SELECT * FROM SUBJECT'
        self.cursor.execute(query)
        resultset = self.cursor.fetchall()
        for r in resultset:
            print(r)

    
    def enroll(self):
        return
    def unenroll(self):
        return
    def join_studygroup(self):
        return
    def create_studygroup(self):
        return
    def create_event(self):
        return
    def pin_event(self):
        return
    def make_post(self):
        try:
            username = input("Username: ") # [TODO:] Replace with logged in username
            dnum = input("DNum: ") # [TODO:] Replace with logged in Dnum
            post_number = input("PNo.: ")   # [TODO:] Generate post_number based on no. of posts made by the username+dnum
            post_title = input("Post title: ")
            post_content = input("Post content: ")
            post_type = ""
            while(post_type!="Review" and post_type!="Blog"):
                post_type = input("Type [Review/Blog]: ")
            sql = "INSERT INTO `POST` "
            
            if(post_type == "Review"):
                post_courseid = input("CourseID: ")
                post_rating = input("Rate the course [1-10]: ")
                sql += "(`UserName`, `DNum`, `PostNumber`, `PostTitle`, `PostContent`, "
                sql += "`Type`, `CourseID`, `ReviewRating`) "
                sql += "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s );"
                self.cursor.execute(sql, (username, dnum, post_number, post_title, post_content, post_type, post_courseid, post_rating))
            else:
                sql += "(`UserName`, `DNum`, `PostNumber`, `PostTitle`, `PostContent`, `Type`) "
                sql += "VALUES ( %s, %s, %s, %s, %s, %s );"
                self.cursor.execute(sql, (username, dnum, post_number, post_title, post_content, post_type))
            self.connection.commit()

        except Exception as e:
            print(e)
            self.ask_user_action(self.make_post)

        return
            

    def befriend(self):
        try:
            attributes = {
                "Friend2Name" : "",
                "Friend2DNum" : ""
            }
            for attribute in attributes:
                    while(attributes[attribute]==""):
                        if(attribute == 'Friend2DNum'):
                            attributes[attribute] = int(input(attribute+": "))
                        else:
                            attributes[attribute] = input(attribute+": ")
                        
                        
            
            query = "INSERT INTO `FRIENDS_WITH` (Friend1Name,Friend1DNum,Friend2Name,Friend2DNum) VALUES ('%s',%d,'%s',%d)" % (attributes["Friend2Name"],attributes["Friend2DNum"],self.current_user[0],self.current_user[1])
            self.cursor.execute(query)
            self.connection.commit()
        
        except Exception as e:    
            print(e)
            self.ask_user_action(self.befriend)
        
    def update_interest(self):
        try:
            SubName = ""
            while(SubName == ""):
                SubName = input("Subject Name: ")
            InterestType = ""
            while(InterestType == ""):
                InterestType = input('Modified Interest Type["Research" ,"Professional" , "Major" ,"Minor" ,"Casual"]: ')
                if InterestType not in ["Research" ,"Professional" , "Major" ,"Minor" ,"Casual"]:
                    InterestType = ""
            query = "UPDATE `HAS_INTEREST_IN` SET InterestType = '%s' WHERE UserName = '%s' and DNum = %d and SubName = '%s'" %(InterestType,self.current_user[0],self.current_user[1],SubName)
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:    
            print(e)
            self.ask_user_action(self.update_interest)
    # Admin Actions
    def add_user(self):
        try:
            os.system('clear')
            print("ADD NEW USER")
            username = input("Username*: ")
            dnum = self.get_number(username,"USER","UserName")
            fname = input("First Name*: ")
            mname = input("Middle Name: ")
            if(mname == ""):
                mname = None
            lname = input("Last Name*: ")
            dob = input("Date of Birth (YYYY-MM-DD))*: ")
            email = input("Email*: ")
            password = input("Password*: ")
            sql = "INSERT INTO `USER` values ('%s',%d, '%s', '%s', '%s', '%s', '%s','%s');" % (username,dnum,fname,mname,lname,dob,email,password)
            print(sql)
            self.cursor.execute(sql)
            
            numberOfLanguagesKnown = 0
            while(numberOfLanguagesKnown <= 0):
                numberOfLanguagesKnown = int(input("Enter Number of languages known[atleast one]: "))
            for _ in range(numberOfLanguagesKnown):
                self.add_languageKnown(username,dnum)
            numberOfSubjectInterest = 0
            while numberOfSubjectInterest <= 0:
                numberOfSubjectInterest = int(input("Enter Number of Subject Interest[atleast one]: "))
            for _ in range(numberOfSubjectInterest):
                self.add_subjectInterest(username,dnum)
            self.connection.commit()

        except Exception as e:
            print(e)
            self.ask_user_action(self.add_user)
    def get_number(self, username,tablename,columnname):
        query = "SELECT COUNT(*) FROM `%s` WHERE %s='%s'"%(tablename,columnname,username)
        print(query)
        self.cursor.execute(query)
        resultset = self.cursor.fetchone()
        
        return resultset['COUNT(*)']
    def add_course(self):
        try:
            os.system("clear")
            print("ADD NEW COURSE")
            attributes = {"Course Name: ":"", 
                        "Course Org: ":"", 
                        "Course Platform: ":"",
                        "Weekly Course Hours: ":"",
                        "Course Duration: ":""
                    }
            coursedifficulty=""
            for attribute in attributes:
                while(attributes[attribute]==""):
                    attributes[attribute] = input(attribute)
            while(coursedifficulty not in ["Beginner", "Intermediate", "Expert"]):
                coursedifficulty = input("Course Difficulty [Beginner/Intermediate/Expert]: ")

            sql_difficulty = "INSERT INTO `COURSE_DIFFICULTY` (`CourseName`, `CourseOrg`, `CoursePlatform`, `CourseDifficulty`) values (%s, %s, %s, %s);"
            sql_course = "INSERT INTO `COURSE` (`CourseName`, `CourseOrg`, `CoursePlatform`, `CourseHours`, `CourseDuration`) values (%s, %s, %s, %s, %s);"

            self.cursor.execute(sql_difficulty, tuple(attributes.values())[:3]+(coursedifficulty,))
            self.cursor.execute(sql_course, tuple(attributes.values()))
            self.connection.commit()
        except Exception as e:
            print(e)
            self.ask_user_action(self.add_course)


    def add_subject(self):
        try:
            print('ADDING SUBJECT')
            
            attributes = {"SubName":""
                }
        
            for attribute in attributes:
                while(attributes[attribute]==""):
                    attributes[attribute] = input(attribute+": ")
                
            query = "INSERT INTO `SUBJECT` VALUES ('%s');" % (attributes['SubName']) 
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(e)
            self.ask_user_action(self.add_subject)
        
    def add_subjectInterest(self,username,dnum):
        try:
            SubName = ""
            while(SubName == ""):
                SubName = input("Subject Name: ")
            InterestType = ""
            while(InterestType == ""):
                InterestType = input('Interest Type["Research" ,"Professional" , "Major" ,"Minor" ,"Casual"]: ')
                if InterestType not in ["Research" ,"Professional" , "Major" ,"Minor" ,"Casual"]:
                    InterestType = ""
            query = "INSERT INTO `HAS_INTEREST_IN` VALUES ('%s',%d,'%s','%s')" %(username,dnum,SubName,InterestType)
            self.cursor.execute(query)
            
        except Exception as e:
            print(e)
            print("Try again")
            self.add_languageKnown()

    def add_languageKnown(self,username,dnum):
        try:
            LangCode = ""
            while(LangCode == ""):
                LangCode = input("Language Code[3 characters]: ")
                if(len(LangCode) != 3):
                    LangCode = ""
            Fluency = ""
            while(Fluency == ""):
                Fluency = input('Fluency["Elementary" ,"Limited Working" , "Professional Working" ,"Native"]: ')
                if Fluency not in ["Elementary" ,"Limited Working" , "Professional Working" ,"Native"]:
                    Fluency = ""
            query = "INSERT INTO `KNOWS` VALUES ('%s',%d,'%s','%s')" %(username,dnum,LangCode,Fluency)
            print(query)
            self.cursor.execute(query)
            
        except Exception as e:
            print(e)
            print("Try again")
            self.add_languageKnown()
    def add_language(self):
        try:
            print("ADDING LANGUAGE")
            attributes = {
                'LangCode' : "",
                'LangName' : ""
            }
            
            for attribute in attributes:
                while(attributes[attribute]==""):
                    attributes[attribute] = input(attribute+": ")
                    if attribute == 'LangCode':
                        while(len(attributes[attribute]) != 3):
                            print("LangCode should be of 3 character")
                            attributes[attribute] = input(attribute+": ")
            
            query = "INSERT INTO `LANGUAGE` VALUES ('%s','%s')" % (attributes['LangCode'],attributes['LangName'])
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(e)
            self.ask_user_action(self.add_language)
    
    def add_prerequisite(self):
        return 
    
    def main_screen(self):
        print("WELCOME TO OPEN SOURCE UNIVERSITY")
        print("1. ADMIN")
        print("2. USER")
        print("3. EXIT")
        choice = input()
        if(choice == "1"):
            self.admin_screen()
            
        elif(choice == "2"):
            self.login_screen()
        elif(choice == "3"):
            return 0
            
        else:
            print("invalid choice")
    
        
        

def main():
    session = Session()
    while(True):
        if(session.main_screen() == 0):
            break
    

if(__name__ == "__main__"):
    
    main()