import matplotlib.pyplot as plt
from tkinter import messagebox



import mysql.connector as c
db = c.connect(host='localhost', database='school_records', user='root', passwd='mysql123')
mc=db.cursor()


#now we're only taking data from the database

#name is in format test_10_1

def stuname(admn, grade):
    grade='grade'+grade
    string = "select name from %s where StudID= "%grade+admn
    return (execute(string)[0])
    

def c():
    print('__'*15)

def execute(string):
    mc.execute(string)
    y=[]
    
    for i in mc:
        for j in i:
            y.append(j)
    return y
    

def multisingle(name):
    
    string="select AVG(english), AVG(maths), AVG(science), AVG(((english+maths+science)/3)) AS Average from %s" %name
    y=execute(string)
            
    x=['English', 'maths', 'Science','Average']
    title ="Average Performance by class in "+name
    plt.bar(x, y, color= "#442244", label= "marks", width=0.55 )

    plt.xlabel('Subject')
    plt.ylabel('Marks')
    plt.title(title)

    a=[]
    s="select max(english) from %s" %name
    a.append(execute(s))
    s="select max(maths) from %s" %name
    a.append(execute(s))

    s="select max(science) from %s" %name
    a.append(execute(s))
    s="select max((maths + science+ english)/3) from %s" %name
    a.append(execute(s))


 
    plt.scatter(x,a,color='#000000', label='highest marks in the subject')
    plt.legend()


    plt.show()


    
 


def gradetables(n):
    #note: n is not an integer, it is being inputed as a string 
    string="show tables;"
    mc.execute(string)
    a="test_"+n+'_'
    b=len(a)

    actual=[]
    for i in mc:
        for j in i:
            if str(j)[0:b]==a:
                actual.append(j)
    return actual



        




def multisubjdata(n):
    
    array= gradetables(n)
    by=''
    for i in range(len(array)):
        if i!=(len(array)-1):
            by=by+array[i]+', '
        else:
            by=by+array[i]
    
    
    eng=''
    for i in range(len(array)):
        if i!=(len(array)-1):
            eng=eng+'avg('+array[i]+'.english), '
        else:
            eng=eng+'avg('+array[i]+'.english)'
    eng='select '+eng+'from '+by
    
    english=execute(eng)
    
    

    maths=''
    for i in range(len(array)):
        if i!=(len(array)-1):
            maths=maths+'avg('+array[i]+'.maths), '
        else:
            maths=maths+'avg('+array[i]+'.maths)'
    maths='select '+maths+'from '+by
    
    mathss=execute(maths)


    sci=''
    for i in range(len(array)):
        if i!=(len(array)-1):
            sci=sci+'avg('+array[i]+'.science), '
        else:
            sci=sci+'avg('+array[i]+'.science)'
            
    sci='select '+sci+'from '+by
    
    science=execute(sci)

    return (english, mathss, science)



def multisubjgraph(n):
    english, mathss, science = multisubjdata(n)
    
    plt.plot(gradetables(n), english, color= "#13c5dd", label= "english", linewidth='2.0', marker='o')
    plt.plot(gradetables(n), mathss, color= "#f2a621", label= "mathss", linewidth='2.0', marker='o')
    plt.plot(gradetables(n), science, color= "#295b3e", label= "science", linewidth='2.0',marker='o')

    


    

    plt.xlabel('Test Number')
    plt.ylabel('Marks')
    plt.title("Cumulative performance by grade %s "%n)
    plt.legend()
    plt.show()



def multiavgdata(n):
    average=[]

    for i in gradetables(n):
        s='select avg((maths+science+english)/3) from %s' %i
        a=execute(s)
        average.append(a)
    

    maximum=[]
    for i in gradetables(n):
        s='select max((maths+science+english)/3) from %s' %i
        a=execute(s)
        maximum.append(a)
    return average, maximum



def multiavggraph(n):
    
    y = multiavgdata(n)[0]
    x= gradetables(n)
    plt.plot(x,y, color='y', marker='o', linewidth='2.0', label='marks')
    plt.title('Average Marks in each test by grade %s'%n)
    yscat= multiavgdata(n)[1]
    plt.scatter(x,yscat,color='#234432', label="Highest Marks in Grade")
    plt.legend()
    plt.show()



def inditest(admn, grade, test):#n is admin no(which is a string)
    
    
    
    string ='select StudID, english, maths, science, (maths+science+english), ((maths+science+english)/3) as Total from %s where StudID like '%test+admn
    x= execute(string)

    
    v= stuname(admn, grade)
    name=("Name of Student: ", v)
    data=[]
    Head=['StudID: ', 'English: ', 'maths: ', 'Science: ', 'Total: ', 'Average: ']

    for i in range(5):
        data.append((Head[i], x[i]))

    return name, data
   
    

def indisubjdata(admn,grade):

    
    n=admn
    
    #SELECT test_10_1.english ,test_10_2.english FROM test_10_1 ,
    #test_10_2 WHERE  test_10_1.StudID= test_10_2.StudID AND test_10_1.StudID='3';
    
    english=[]
    maths=[]
    sci=[]
    for i in gradetables(grade):
        s="select english from %s where StudID like "%i +n
        a=execute(s)
        english.append(a)

    for i in gradetables(grade):
        s="select maths from %s where StudID like "%i +n
        a=execute(s)
        maths.append(a)

    for i in gradetables(grade):
        s="select science from %s where StudID like "%i +n
        a=execute(s)
        sci.append(a)

    return (english, maths, sci, grade)




def indisubjgraph(admn, grade):
    english, mathss, science, n = indisubjdata(admn, grade)
    
    
    plt.plot(gradetables(n), english, color= "#13c5dd", label= "english", marker='o', linewidth='2.0')
    plt.plot(gradetables(n), mathss, color= "#f2a621", label= "mathss", marker='o', linewidth='2.0')
    plt.plot(gradetables(n), science, color= "#295b3e", label= "science",marker='o', linewidth='2.0')


    

    plt.xlabel('Test Number')
    plt.ylabel('Marks')
    plt.title("Subject Wise Performance in Tests by  %s"%stuname(admn,grade))
    plt.legend()
    plt.show()
    

    
def indiavgdata(admn, grade):
    
    average=[]
    n=grade

    for i in gradetables(n):
        s='select ((maths+science+english)/3) from %s where StudID like '%i+admn
        a=execute(s)
        average.append(a)
    

    maximum=[]
    for i in gradetables(n):
        s='select max((maths+science+english)/3) from %s' %i
        a=execute(s)
        maximum.append(a)
        
    return average, maximum, gradetables(n)

def indiavggraph(admn, grade):

    y, yscat, x = indiavgdata(admn, grade)
    
  
    plt.plot(x,y, color='y', label='marks',marker='o', linewidth='2.0')

    plt.scatter(x,yscat,color='#234432', label='Highest Marks in Grade')
    plt.title("Average marks of %s in tests"%stuname(admn,grade))

    plt.legend()
    plt.show()

def tableexists(n):
    if n[:5]=='test_':
        
        st="SHOW TABLES LIKE '%s'" %n
        mc.execute(st)
        data=[]

        for i in mc:
            data.append(i)
        
        if data==[]:
            return False
        else:
            return True
    else:
        return False
    
def gradeexists(n):
    if n.isdigit() and int(n)>=1 and int(n)<=12:
        st="SHOW TABLES LIKE 'grade%s'" %n
        mc.execute(st)
        data=[]

        for i in mc:
            data.append(i)
        
        if data==[]:
            return False
        else:
            return True
    else:
        return False

        
        
        
    
        

def adminexists(a, n):
    st="SELECT StudID from grade%s where StudID = '"%n+a+"'"
    mc.execute(st)
    data=[]

    for i in mc:
        data.append(i)
    if data==[]:
        return False
    else:
        return True

def admintestexists(a, n):
    st="SELECT StudID from %s where StudID = '"%n+a+"'"
    mc.execute(st)
    data=[]

    for i in mc:
        data.append(i)
    if data==[]:
        return False
    else:
        return True

    
    
    
def update(test, admn, subj, score):
    if tableexists(test):
        if subj in ['english', 'maths', 'science']:
            
        
            if admintestexists(admn, test):
                stdata="select * from %s where StudID="%test+admn
                old=execute(stdata)
                
                
                
                st="UPDATE %s set "%test+ "%s = "%subj + str(score) + " where StudID = '%s'"%admn;
                
                
                mc.execute(st)
                db.commit()
                
                
            
                new=execute(stdata)
                
                return old, new

                
        

            
            
            else:
                responseadmni= messagebox.showwarning("WARNING", "Admn. No has not written the test. \nPlease Re-Enter a valid input")

        else:
                responsesunj=messagebox.showwarning("WARNING", "Subject should be \n'english', 'maths' or 'science'. \nPlease Re-Enter a valid input")
                        
    else:
        responsetest= messagebox.showwarning("WARNING", "TEST NOT FOUND. \nPlease Re-Enter a valid input")
    
        




##multisingle('test_10_1')
##multisubjgraph('10')
##multiavggraph('10')
##indisubjgraph('4')
##indiavggraph('2')
    
##stuname('3','10')



     
    

#width=0.55   
#marker='o'
#linewidth='2.0'
#english :#13c5dd
#maths: #f2a621
#science: #295b3e
#scat:color=#234432
#avgcolorline='y'
