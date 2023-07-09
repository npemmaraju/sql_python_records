#input
#maininp() to run this code

import mysql.connector
import csv
import os
from tkinter import *
from tkinter import messagebox
import display_cp as dcp




db=mysql.connector.connect(host='localhost',user='root',passwd='mysql123', database='school_records')
mc=db.cursor()

def execute(string):
    mc.execute(string)
    y=[]
    
    for i in mc:
        for j in i:
            y.append(j)
    return y

def msginput():
    
    response= messagebox.showwarning("WARNING", "Invalid Input. Please Re-Enter a valid input")
    
def lencsvsql(file, test):
    
    with open(file, 'r', encoding='utf-8-sig') as file:
        reader=csv.reader(file)
        lines=len(list(reader))
    st='select count(*) StudID from %s'%test
    mc.execute(st)
    for i in mc:
        for j in i:
            j=a
            

    if lines==a:
        return True
    else:
        return False

    


gui=Tk()
gui.title("School Database")

frame=LabelFrame(gui, padx=50, pady=50,bg="black" )
frame.pack(padx=5, pady=5,)




def test_exists(grade):#return list of tests of the grade
    l="show tables like 'test_"+str(grade)+"_%' ;"
    mc.execute(l)
    j=mc.fetchall()
    l=[]
    for i in j:
        l.append(i)
    q=[]
    for i in range(len(l)):
        q.append(l[i][0])
    return(q)


def grade_exists(grade):
    j="SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = 'school_records') AND (TABLE_NAME = 'grade"+str(grade)+"');"  #checks if the table exists in the database
    mc.execute(j)
    op=mc.fetchall()
    if op[0][0]:
        return(True)
    else:
        return(False)


def name_test(grade, number):#naming new test 
    return("test_"+str(grade)+"_"+str(number)) 

def insert_into_grade(grade,val):#accepting grade and data in form of nested list to be inputted
    p="create table if not exists grade"+str(grade)+" (StudID varchar(4), Name varchar(30), section varchar(1));"
    mc.execute(p)
    k='grade'+str(grade)
    #sql = "INSERT INTO grade10 (Admno, Name, section) VALUES (%s, %s, %s)"
    sql = "INSERT INTO "+k+" (StudID, Name, section) VALUES (%s, %s, %s);"
    
    mc.executemany(sql, val)    
    db.commit()
    
    
def insert_into_test(tst_nm,val):#accepting test name and data in form of nested list to be inputted
    s="create table if not exists " +tst_nm+ " (StudID varchar(4), English integer, maths integer, Science integer);"
    mc.execute(s)
    sql = "INSERT INTO "+ tst_nm +" (StudID, English, maths, Science) VALUES (%s, %s, %s, %s);"
    mc.executemany(sql, val)
    db.commit()

def fill_test(grade):#to set default marks of new student as 0 in all subjects and all tests when grade data is inputted; user can later update marks using update option
    q=[]
    for t in test_exists(grade):
        
        c="select count(*) from "+t+";"    
        mc.execute(c)#get number of records in that particular test    
        count=mc.fetchall()#stores [(no.of records,)]
        u=grade*100+count[0][0]+1# new student id
        print(t)
        
        for j in range(grade*100+count[0][0]+1,u+1):#run loop till no. of records in test is equal to no. of records in grade; i is admission no.
            sql="insert into "+t+" (StudID, English, maths, Science) values ('" + str(j)+ "',0,0,0);"
            mc.execute(sql)
            db.commit()
            

def add_data_grade(grade):
    
    l=[]#stores the records inputted by the user

    name="grade"+str(grade)
    p="create table if not exists "+name+" (StudID varchar(4), Name varchar(30), section varchar(1));"
    mc.execute(p)

    t="select count(*) from "+name+";"    
    mc.execute(t)    
    count=mc.fetchall()#stores [(no.of records,)] count[0][0]= no.of records
    
    u=grade*100+count[0][0]+1# new admission number
    
    ch='y'
    
    root=Toplevel()
    root.title("GRADE DATA")
    root.configure(background='#AAA0FF')
    
    
    q="Entering data for grade "+str(grade)+".      Admission number is auto-generated"
    lbl1=Label(root, text=q,bg='orange')
    lbl1.grid(row=0, column=0)      
    
    lbl2=Label(root, text="Section should be single alphabet only",bg='orange')
    lbl2.grid(row=1, column=0)


    #ACCEPT DATA
    
    lbl4 = Label(root, text="Enter Student name:",bg='orange')
    lbl4.grid(row=3, column=0)
    n=Entry(root, width=20, bg="#678293", fg="#FFFFFF", borderwidth=10)
    n.grid(row=3, column=1)
    #n=input("Student Name: ")

    lbl5 = Label(root, text="Enter Section: ",bg='orange')
    lbl5.grid(row=4, column=0)
    s=Entry(root, width=20, bg="#678293", fg="#FFFFFF", borderwidth=10)
    s.grid(row=4, column=1)        
    #s=input("Enter Section: ")        

    
    u=grade*100+count[0][0]+1# new student id

   
    
        
    def myclick(lst,ad,choice):
        sec=s.get()        
        if len(sec)!=1 or sec.isalpha()==False :#ensure that section is single character alphabet only; only when both these are false, 0+0=0 then it exits while loop
            messagebox.showwarning("WARNING","Invalid Section")

        else:
            messagebox.showinfo("CONGRATS!","Data successfully saved")

            if len(lst)>0:#incrementing student id
                ad=int(lst[-1][0])+1
                
            lst.append([str(ad),n.get(),sec])
            
            print(lst)#check
            
            
            
                
    def leavedestroy(win, grade, l):
        win.destroy()
        insert_into_grade(grade,l)#adding the data to the sql file
        fill_test(grade)
        

    
    myButton = Button(root, text="Save data", padx=30, pady=30,command= lambda: myclick(l,u,ch), fg="#000000", bg="#FFFFA0")
    myButton.grid(row=6, column=0)

            
    tonleave=Button(root, text="Return to main Menu", command=lambda: leavedestroy(root, grade, l)).grid(row=7, column=1)
        
    


def add_data_test(grade,test_no):#adding new test data one by one;in pre-existent tables, data can only be updated (where no. of records is limited by the no. of students in grade table)

    
    
    if grade_exists(grade):#If grade table exists
        
        grd='grade'+str(grade)#name of respective grade table
        t="select count(*) from " + grd + ";"
        
        mc.execute(t)    
        count=mc.fetchall()
        #stores [(no.of records,)] count[0][0]= no.of records
        print("count", count)
        
        if not count[0][0]:#if no data exists in table
            messagebox.showinfo("INFORMATION ","Grade data does not exist. Input grade data first")
            
        else:

            root=Toplevel()
            root.title("TEST DATA")
            root.configure(background='lavender')
    
            test_data=[]#to store test data inputted by user

            #creating table name for new test
            test=name_test(grade,test_no)
            
            num=0
            
            txt1="Entering data for test: " +str(test)
            Label(root, text=txt1,bg='red').grid(row=0, column=0)

            
            #To overwrite test file if exists
            s="create table if not exists " +test+ " (StudID varchar(4), English integer, maths integer, Science integer);"
            mc.execute(s)
            s='drop table '+test+" ;"
            mc.execute(s)
            s="create table if not exists " +test+ " (StudID varchar(4), English integer, maths integer, Science integer);"
            mc.execute(s)
            
            sql1="select "+grd+".Name ,"+grd+".StudID from "+grd+" ;"
            mc.execute(sql1)
            a=mc.fetchall()#contains (name, admno)
            
             
            p=[]#store list of tuples containing name and studid. of student [(name,studid),]
            for x in a:
                p.append(x)

            end=p[-1][-1]#stores student ID of last student
            #information about how many records are pre-existent in the Grade table
            if len(p)==1:
                txt2="There is "+str(len(p))+" record in the Grade "+ str(grade)+ " Table"   ##while true, if admssion number becomes a particular no, then break
                Label(root, text=txt2,bg='red').grid(row=1,column=0)
                
            else:
                txt2="There are "+str(len(p))+" records in the Grade "+str(grade)+" Table"
                Label(root, text=txt2,bg='orange').grid(row=1,column=0)

            Label(root, bg='yellow',text="Enter Integer value in range 0-100 for marks. If you don't enter marks for all students at once, marks will be set as 0 by default for the remaining students. You can update marks later using update option").grid(row=2,column=0) 
            
            def add_tst(number,last,l,eng,sci,mth,c,testname):#function for button command

                                                             #accept lase studID, test_data as l, marks, choice and test name


                if not eng.isdigit() or int(eng)not in range(0,101):
                    messagebox.showwarning("ERROR!",'Invalid integer marks in English in range 0-100')
                    entry(number)
                    
                elif not sci.isdigit() or int(sci)not in range(0,101):
                    messagebox.showwarning("ERROR!",'Invalid integer marks in Science in range 0-100')
                    entry(number)
                    
                elif not mth.isdigit() or int(mth)not in range(0,101):
                    messagebox.showwarning("ERROR!",'Invalid integer marks in Maths in range 0-100')
                    entry(number)
                
                else:    
                    if len(l)==0:#for first records
                        l.append([str(((int(last))//100)*100+1),int(eng),int(mth),int(sci)])
     
                    else:
                        l.append([str(int(l[-1][0])+1),int(eng),int(mth),int(sci)])#student ID calulated by adding 1 to student ID of previous student

                    print(l)
                        
                    if c.lower()!='y' or int(l[-1][0])==int(last):#if user doesn't want to enter more values or the user has entered data for all students
                        if int(l[-1][0])!=int(last):
                            for i in range(int(l[-1][0])+1,int(last)+1):
                                l.append([str(i),0,0,0])
                        else:
                            messagebox.showinfo("INFORMATION",'You have filled data for all students')
                    
                        
                        insert_into_test(testname,l)
                        messagebox.showinfo("CONGRATS!","Test data successfully saved")
                        root.destroy()

                    else:
                        entry(number+1)#run loop again to accept more entries


            
            def entry(i):#creates tkinter form and accepts data entered by user

                txt="You are entering data for \nName: "+p[i][0]+"\nAdmission Number: "+p[i][1]

                Label(root, text=txt, bg='#90EE90').grid(row=3, column=0)
                
                #Accepting data from user
                Label(root, text="Enter English Marks",bg='cyan').grid(row=4, column=0)
                eng= Entry(root,bg='cyan')
                eng.insert(0,0)
                eng.grid(row=4, column=1)

                Label(root, text="Enter Science Marks",bg='navy',fg='white').grid(row=5, column=0)
                sci= Entry(root,bg='navy',fg='white')
                sci.insert(0,0)
                sci.grid(row=5, column=1)
                

                Label(root, text="Enter maths Marks",bg='purple',fg='white').grid(row=6, column=0)
                mth= Entry(root,bg='purple',fg='white')
                mth.insert(0,0)
                mth.grid(row=6, column=1)

                Label(root, text="Enter y or Y to enter more records, anything else to quit",bg='magenta').grid(row=7, column=0)
                c= Entry(root,bg='magenta')
                c.grid(row=7, column=1)
                

                Button(root, text='CONFIRM', bg='pink', command= lambda:add_tst(i,end,test_data,eng.get(),sci.get(),mth.get(),c.get(),test)).grid(row=8,column=0)
            
                
            entry(num)
              
        
    else:
        messagebox.showinfo("INFORMATION ","Grade data does not exist. Input grade data first")    


def add_grade_csv(grade):#user must first save the csv in cwd, then run this function; this fxn accepts grade and name of csv file to transfer the data into the database

    def csv_grade(name,grade):
        file_name=name+'.csv'
        if os.path.exists(file_name):
            l=[]#to store data from csv
            with open(file_name, 'r',encoding='utf-8-sig') as file:
                csvreader=csv.reader(file)
                for i in csvreader:
                    l.append(i)
            insert_into_grade(grade,l)  #testcsv, len
            #gradecsv if grade exists dont allow
            messagebox.showinfo("CONGRATS!", "Data succesfully saved!")
            root.destroy()
            
            
        else:
            txt="Could not find CSV file with name '"+name+"' in current working directory"
            messagebox.showwarning("ERROR!", txt)

    if grade_exists(grade):
        txt="Grade data for grade "+str(grade)+" already exists!"
        messagebox.showinfo("INFORMATION",txt)

    else:

        
        
        root=Toplevel()
        root.title("GRADE CSV UPLOAD")
        root.configure(background='magenta')

        Label(root, text="First, save the csv file in the current working directory of this code, only then press confirm, to tranfer data into database", bg='#AAA0FF').grid(row=0, column=0)
        Label(root, text="Enter name of csv file", bg='#AAA0FF').grid(row=2, column=0)
        e= Entry(root,bg='yellow')    
        e.grid(row=2, column=1)
        Button(root, text="CONFIRM ",command=lambda:csv_grade(e.get(),grade), bg='yellow').grid(row=3, column=0)
               
        
    

def add_test_csv(grade,test_no):#user must first save the csv in cwd, then run this function


    def csv_test(name,grade,num,rec):
        file_name=name+'.csv'
        test_name="test_"+str(grade)+"_"+str(num)
        if os.path.exists(file_name):
            l=[]#to store data from csv
            with open(file_name, 'r',encoding='utf-8-sig') as file:
                csvreader=csv.reader(file)
                for i in csvreader:
                    l.append(i)

            if len(l)==rec:
                insert_into_test((test_name),l)
                messagebox.showinfo("CONGRATS!", "Data succesfully saved!")
                root.destroy()

            else:
                txt="Number of records should be "+str(rec)+" ; found "+str(len(l))+" records"
                messagebox.showerror("ERROR", txt)
                
            
        else:
            txt="Could not find CSV file with name '"+name+"' in current working directory"
            messagebox.showwarning("ERROR!", txt)
     
    if name_test(grade,test_no) in test_exists(grade):
        txt="Test data for test '"+name_test(grade,test_no)+"' already exists!"
        messagebox.showinfo("INFORMATION",txt)

    else:  
        root=Tk()
        root.title("TEST CSV UPLOAD")
        root.configure(background='cyan')

        grd='grade'+str(grade)#name of respective grade table
        t="select count(*) from " + grd + ";"    
        mc.execute(t)    
        count=mc.fetchall()#stores [(no.of records,)] count[0][0]= no.of records


        Label(root, text="First, save the csv file in the current working directory of this code, only then press confirm, to tranfer data into database",bg='#990E99',fg='yellow').grid(row=0, column=0)

        txt="Ensure that csv contains exactly "+str(count[0][0])+" records with correct Student ID"
        Label(root, text=txt,bg='#990E99',fg='yellow').grid(row=1, column=0)
        
        Label(root, text='Enter name of csv file',bg='#990E99',fg='yellow').grid(row=2, column=0)
        
        e= Entry(root,bg='yellow')    
        e.grid(row=2, column=1)
        
        txt="Entering data for test: test_"+str(grade)+"_"+str(test_no)
        Label(root, text=txt,bg='#990E99',fg='yellow').grid(row=3, column=0)
        
        Button(root, text="CONFIRM ",bg='yellow',command= lambda:csv_test(e.get(),grade,test_no,count[0][0])).grid(row=4, column=0)
               
        
    

def maininp():

    root=Toplevel()
    root.title("INPUT DATA")
    root.geometry('460x350')

    #Create containers
    top_frame = Frame(root, bg='navy', width=400, height=100, pady=3)
    main = Frame(root, bg='lavender', width=400, height=300, pady=3)

    #layout of containers
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    top_frame.grid(row=0,column=0,sticky='nsew',columnspan=2)
    main.grid(row=1,column=0,sticky='nsew',columnspan=2)

        
    #widgets for top_frame
    lbl = Label(top_frame, text="Enter Grade")
    grade=Entry(top_frame)
    
    test_label=Label(top_frame, text="Enter Test number(If applicable)")
    number_test=Entry(top_frame)
    number_test.insert(0,'')


    #layout of top_frame widgets
    lbl.grid(row=0, column=0)
    grade.grid(row=0,column=1)
    test_label.grid(row=1,column=0)
    number_test.grid(row=1,column=1)



    

    #main frame widgets
    Modes=[("Grade data",1),("Test data",2)]

    data = StringVar()
    data.set('Grade data')
    
    
    def tst(ch,grade,test_no):#command for test button
        k=True

        if test_no=='':
            messagebox.showwarning("WARNING!" ,"Invalid test number")
            
        else:

            if test_no.isdigit():
                if ch=='Enter csv':
                    add_test_csv(int(grade),int(test_no))

                else:

                    if name_test(grade,test_no) in test_exists(grade):
                        
                        MsgBox = messagebox.askquestion ('INFORMATION','Test data for this test already exists. Are you sure you want to overwrite data?',icon = 'warning')
                        if MsgBox == 'yes':
                           add_data_test(int(grade),int(test_no))
                        else:
                            pass

                    else:
                        add_data_test(int(grade),int(test_no))
        
                    
            else:
                messagebox.showwarning("WARNING!" ,"Invalid integer test number")

        

    def grd(ch,grade):#Command for grade button
                if ch=='Enter csv':
                    add_grade_csv(int(grade))
                    
                else:
                    add_data_grade(int(grade))
                    
    def clicked(value,grade):#Command of button1
        
        
        acceptable_grades=[]
        for i in range(1,13):
            acceptable_grades.append(str(i))    
           
        if grade in acceptable_grades:        
            if value=='Grade data':#If user wants to enter grade data

                data = StringVar()
                data.set('Enter csv')
                

                Radiobutton(main,text="Enter csv", variable=data, value='Enter csv').grid(row=0,column=1)
                Radiobutton(main,text="Enter Individual Records", variable=data, value='Enter Individual Records').grid(row=1,column=1)
                button1_2= Button(main, text="CONFIRM CHOICE", command=lambda: grd(data.get(),grade))
                button1_2.grid(row=2,column=1)
      
            else:#If user wants to enter test data

                data = StringVar()
                data.set('Enter csv')

                Radiobutton(main,text="Enter csv", variable=data, value='Enter csv').grid(row=0,column=1)
                Radiobutton(main,text="Enter Individual Records", variable=data, value='Enter Individual Records').grid(row=1,column=1)
                button1_2= Button(main, text="CONFIRM CHOICE", command=lambda: tst(data.get(),grade,number_test.get()))
                button1_2.grid(row=2,column=1)
                
        else: 
            messagebox.showwarning("WARNING","Invalid Grade")

        

    Radiobutton(main,text="Grade data", variable=data, value='Grade data').grid(row=0, column=0)   
    Radiobutton(main,text="Test data", variable=data, value='Test data').grid(row=1, column=0)   

    button1= Button(main, text="CONFIRM CHOICE", command=lambda: clicked(data.get(),grade.get()))
    button1. grid(row=2, column=0)
    


    




    
    
def display():

    def destroy(main,n ):
        main.destroy()

        displayroot=Toplevel()
        displayroot.configure(background="#cbe330")
        displayroot.title('Analyse Data')
        
        
##        displayroot.configure(background="black")
        displayrootlabel=Label(displayroot, text='', bg="#cbe330").grid(row=22, column=2)
        

        displayrootton=Button(displayroot, text="Return To main menu", command= lambda: displayroot.destroy()).grid(row=23, column=2)

        if n==1:
            label2=Label(displayroot, text="Class Performance", bg="#cbe330").grid(row=1, column=2)
            labele=Label(displayroot, text="Enter grade", bg="#cbe330").grid(row=3, column=1)
            
            

            e=Entry(displayroot, width=25, bg="black", fg="white", borderwidth=5)
            e.grid(row=3, column=2)
            e.insert(0,"")
            
           #e.get() is the input field

          

            def indipart():
                
                    
                etest=Entry(displayroot, width=10, bg="black", fg="white", borderwidth=5)
                labele=Label(displayroot, text="Enter test name in the format 'test'_grade_testno :  ", bg="#cbe330").grid(row=7, column=1)
                etest.grid(row=8, column=1)
                etest.insert(0,"")

                def indigraph(m):
                    
                    if dcp.tableexists(m):
                        dcp.multisingle(m)

                    else:
                        msginput()

                    
                

                
                tonindi=Button(displayroot, text="Graph induvidual test", command= lambda:indigraph(etest.get()) ).grid(row=11, column=1)
                
                    


                
                    #dcp.multisingle(etest.get()))

            def multi():

                def cpgraph(n):
                    if n==0:
                        dcp.multisubjgraph(e.get())
                    elif n==1:
                        dcp.multiavggraph(e.get())

                    else:
                        pass
                        


                optmulti=IntVar()

               
                blabel2=Label(displayroot, text="",bg="#cbe330").grid(row=7,column=3)
                Rton3= Radiobutton(displayroot, text="a.Subjectwise ",  bg="#cbe330", variable=optmulti, value=0).grid(row=8, column=3)
                Rton4= Radiobutton(displayroot, text="b.Class Average ",  bg="#cbe330", variable=optmulti, value=1).grid(row=9, column=3)
                
                tonindi=Button(displayroot, text="Graph", fg="blue", command= lambda: cpgraph(optmulti.get())).grid(row=11, column=3)
                

                

                
                

            def options2(n):
                if n==0:
                    indipart()
                elif n==1:
                    multi()

                else:
                    pass
            

            def dummyfun():
                n=e.get()
                if n.isdigit():

                    n=int(n)
                
                    if n>=1 and n<=12:

                        opt=IntVar()
                        
                        Rton1= Radiobutton(displayroot, text="1.A Particular Test", bg="#cbe330", variable=opt, value=0).grid(row=5, column=1)
                        Rton2= Radiobutton(displayroot, text="2.For Cumulative Tests", bg="#cbe330", variable=opt, value=1).grid(row=5, column=3)


                        #Button to select option
                            
                        tonradio=Button(displayroot, text="Select", command= lambda: options2(opt.get()))
                        tonradio.grid(row=5, column=2)
                    else:
                        msginput()
                else:
                    msginput()
                    
                    

                    
                    
                    
                

            ton1=Button(displayroot, text="Next", fg= "green", command=dummyfun).grid(row=3, column=3)

            
            
            
        
        else:
            #induvidual performance
            
            def optionsindi(n):
                if n==0:
                    invpart()
                    
                elif n==1:
                    invmulti()

                else:
                    pass

            def invpart():
                
                etestinv=Entry(displayroot, width=10, bg="black", fg="white", borderwidth=5)
                labele=Label(displayroot, text="Enter test name in the format 'test'_grade_testno :  ", bg="#cbe330").grid(row=7, column=1)
                etestinv.grid(row=8, column=1)
                etestinv.insert(0,"")
                
                def invgraph(m):
                    if dcp.tableexists(m):
                        pro=Toplevel()
                        pro.configure(background="#cbe330")
                        pro.title("Student Performance Analysis")
                        invipartlabel=Label(pro, text="Student Performance Details", padx=25, pady=26, bg="#cbe330" ).grid(row=11,column=1)
                        
                        
                        name, data=dcp.inditest(eadmin.get(),egrade.get(),m)
                        j=12
                        for i in range(len(name)):
                            Label(pro, text=name[i], bg="#cbe330").grid(row=j, column=1)
                            j+=1
                        for i in range(len(data)):
                            
                            Label(pro, text=data[i][0]+str(data[i][1]), bg="#cbe330").grid(row=j, column=1)
                            j+=1
                        tonpro=Button(pro, text="go back", command=pro.destroy).grid(row=j, column=1)


                    else:
                        responsetest= messagebox.showwarning("WARNING", "Invalid test no\n Or Test not in correct format.\n Please Re-Enter a valid input")                    
                            

                


                toninv=Button(displayroot, text="Show details of test", command= lambda:invgraph(etestinv.get()) ).grid(row=11, column=1)
                

               

                
                
            
            def invmulti():
                
            

                def invgraph(n):
                    if n==0:
                        dcp.indisubjgraph(eadmin.get(),egrade.get())
                    elif n==1:
                        dcp.indiavggraph(eadmin.get(), egrade.get())

                    else:
                        pass
                        


                optindi=IntVar()

               
             
                Rton3= Radiobutton(displayroot, text="a.Subjectwise ",  bg="#cbe330", variable=optindi, value=0).grid(row=8, column=3)
                Rton4= Radiobutton(displayroot, text="b.Overall Average ", bg="#cbe330", variable=optindi, value=1).grid(row=9, column=3)
                
                tonindi=Button(displayroot, text="Graph", fg="blue", command= lambda: invgraph(optindi.get())).grid(row=11, column=3)
        

            def indiper(admin, grade):
                




                if dcp.gradeexists(grade):
                    if dcp.adminexists(admin, grade):

                        opt=IntVar()
                        
                        Rton1= Radiobutton(displayroot, text="1.A Particular Test", bg="#cbe330", variable=opt, value=0).grid(row=6, column=1)
                        Rton2= Radiobutton(displayroot, text="2.For Cumulative Tests",  bg="#cbe330", variable=opt, value=1).grid(row=6, column=3)


                        #Button to select option
                            
                        tonradio=Button(displayroot, text="Select",command=lambda: optionsindi(opt.get()) )
                        tonradio.grid(row=6, column=2)
                        



                    else:

                        responseadmni= messagebox.showwarning("WARNING", "Invalid ADMIN no. Please Re-Enter a valid input")
                        




                else:
                    responsegrade= messagebox.showwarning("WARNING", "GRADE NOT FOUND. Please Re-Enter a valid input")
                    
            
                    

            labeltitleindi=Label(displayroot, text="Induvidual Performance", bg="#cbe330").grid(row=1, column=2)
            labeladmin=Label(displayroot, text="Enter Admission No: ", bg="#cbe330").grid(row=3, column=1)
            
            

            eadmin=Entry(displayroot, width=25, bg="black", fg="white", borderwidth=5)
            eadmin.grid(row=3, column=2)
            eadmin.insert(0,"")

            
            labelgrade=Label(displayroot, text="Enter grade: ", bg="#cbe330").grid(row=4, column=1)
            egrade=Entry(displayroot, width=25, bg="black", fg="white", borderwidth=5)
            egrade.grid(row=4, column=2)
            egrade.insert(1,"")
        
        
            
            
            tondetails=Button(displayroot, text="Next", fg= "green", command=lambda: indiper(eadmin.get(),egrade.get())).grid(row=4, column=3)

            


    top=Toplevel()
    top.title('Analyse Data')
    top.configure(background="black")
    top.geometry('300x200')




    headlabel=Label(top, text="\nDisplay Graphs based on Student Performance\nSelect Option", fg="#cbe330", bg="black").pack()#0,0



    r=IntVar()

    MODES=[("Induvidual Student",0), ("Class Performance", 1)]

    for opt, ch in MODES:
        Radiobutton(top, text=opt,bg="black", fg="#cbe330", variable=r, value=ch).pack()

    
    tontopquit=Button(top, text="Next", command=lambda:destroy(top,r.get() ) ).pack()

    




def update():
        
    def updategraph(test, admn, subj, score):
        if dcp.tableexists(test):
            if subj in ['english', 'maths', 'science']:
                
            
                if dcp.admintestexists(admn, test):

                    if score.isdigit() and int(score)<101 and int(score)>=0:
                        
                        stdata="select * from %s where StudID="%test+admn
                        old=execute(stdata)
                        
                        
                        
                        
                        st="UPDATE %s set "%test+ "%s = "%subj + str(score) + " where StudID = '%s'"%admn;
                        
                        
                        mc.execute(st)
                        db.commit()
                        

                        
                        new=execute(stdata)
                        
                        head=['StudID', 'English', 'maths', 'Science']
                        
                
               
                        labelhead2=Label(upd, text="OLD", bg="#cbe330").grid(row=10, column=2)
                        labelhead3=Label(upd, text="NEW", bg="#cbe330").grid(row=10, column=3)
                        
                        
                        for i in range(4):
                            if old[i]==[]:
                                old[i]='1'
                            Label(upd, text=head[i], bg="#cbe330").grid(row=12+i, column=1)
                            Label(upd, text=old[i], bg="#cbe330").grid(row=12+i, column=2)
                            Label(upd, text=new[i], bg="#cbe330").grid(row=12+i, column=3)



                    else:
                        responsetest= messagebox.showwarning("WARNING", "SCORE MUST BE AN INTEGER VARYING FROM 0-100. \nPlease Re-Enter a valid input")
                        
                            

                    
                    

                    
            

                
                
                else:
                    responseadmni= messagebox.showwarning("WARNING", "Admn. No has not written the test. \nPlease Re-Enter a valid input")

            else:
                    responsesunj=messagebox.showwarning("WARNING", "Subject should be \n'english', 'maths' or 'science'. \nPlease Re-Enter a valid input")
                            
        else:
            responsetest= messagebox.showwarning("WARNING", "TEST NOT FOUND. \nPlease Re-Enter a valid input")
        
            

       
        
        
        
    upd= Toplevel()
    upd.title("UPDATE SCORES")
    upd.configure(background="#cbe330")
    labelupd=Label(upd, text="FILL IN DETAILS: ", bg="#cbe330").grid(row=2, column=1)
    
    j=5
    for i in ['test', 'admin','subject','score']:
        st="Enter %s : "%i
        Label(upd, text=st, bg="#cbe330").grid(row=j, column=1)
        j+=1

    eupdtest=Entry(upd, width=25, bg="black", fg="white", borderwidth=5)
    eupdtest.grid(row=5 , column=2)
    eupdadmin=Entry(upd, width=25, bg="black", fg="white", borderwidth=5)
    eupdadmin.grid(row=6 , column=2)
    eupdsubject=Entry(upd, width=25, bg="black", fg="white", borderwidth=5)
    eupdsubject.grid(row= 7 , column=2)
    eupdscore=Entry(upd, width=25, bg="black", fg="white", borderwidth=5)
    eupdscore.grid(row= 8, column=2)

    tonupdate=Button(upd, text="UPDATE", command=lambda: updategraph(eupdtest.get(), eupdadmin.get(), eupdsubject.get(), eupdscore.get())).grid(row=10, column=1)

    displayrootton=Button(upd, text="Return To main menu", command= lambda: upd.destroy()).grid(row=20, column=2)
    
    
        
    

def function():
    if r.get()==0:
        maininp()
    if r.get()==1:
        display()
    elif r.get()==2:
        update()
    



#menu formatting
headlabel=Label(frame, text="Welcome to Database\nSelect operation", bg="black", fg="#cbe330").pack()#0,0

#radiobutton options

r=IntVar()

MODES=[("Insert Data",0), ("Analyze Data", 1), ("Update Data",2)]

for opt, ch in MODES:
    Radiobutton(frame, text=opt,bg="black", fg="#cbe330", variable=r, value=ch).pack()


#Button to select option
    
tonradio=Button(frame, text="Click", command=function)
tonradio.pack()



gui.mainloop()


