from cgitb import text
import imp
from re import L
from textwrap import fill
from tkinter import*
from tokenize import String
from turtle import title
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os

class employeeClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1270x618+150+110")
        self.root.title("Inventory Management System | Developed By Ansh")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #===================All Variables=======================
        
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        
        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_email=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()
        self.var_salary=StringVar()
        
        #======================Title================
        
        title=Label(self.root,text="Welcome to Inventory Management System , First Time Registeration",font=("gody old style",15),bg="#0f4d7d",fg="white").place(x=50,y=100,width=1170)
        
        #======================Content==================
        #=====Row1=====
        
        lbl_empid=Label(self.root,text="Emp ID",font=("gody old style",15),bg="white").place(x=50,y=150)
        lbl_gender=Label(self.root,text="Gender",font=("gody old style",15),bg="white").place(x=450,y=150)
        lbl_contact=Label(self.root,text="Contact",font=("gody old style",15),bg="white").place(x=900,y=150)
        
        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("gody old style",15),bg="lightyellow").place(x=150,y=150,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Male","Female","Other"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_gender.place(x=600,y=150,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("gody old style",15),bg="lightyellow").place(x=1040,y=150,width=180)
        
        #=====Row2=====
        
        lbl_name=Label(self.root,text="Name",font=("gody old style",15),bg="white").place(x=50,y=190)
        lbl_dob=Label(self.root,text="D.O.B",font=("gody old style",15),bg="white").place(x=450,y=190)
        lbl_doj=Label(self.root,text="D.O.J",font=("gody old style",15),bg="white").place(x=900,y=190)
        
        txt_name=Entry(self.root,textvariable=self.var_name,font=("gody old style",15),bg="lightyellow").place(x=150,y=190,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("gody old style",15),bg="lightyellow").place(x=600,y=190,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("gody old style",15),bg="lightyellow").place(x=1040,y=190,width=180)
        
        #=====Row3=====
        
        lbl_email=Label(self.root,text="Email",font=("gody old style",15),bg="white").place(x=50,y=230)
        lbl_pass=Label(self.root,text="Password",font=("gody old style",15),bg="white").place(x=450,y=230)
        lbl_utype=Label(self.root,text="User Type",font=("gody old style",15),bg="white").place(x=900,y=230)
        
        txt_email=Entry(self.root,textvariable=self.var_email,font=("gody old style",15),bg="lightyellow").place(x=150,y=230,width=180)
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("gody old style",15),bg="lightyellow").place(x=600,y=230,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Select","Admin"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_utype.place(x=1040,y=230,width=180)
        cmb_utype.current(0)
        
        #=====Row4=====
        
        lbl_address=Label(self.root,text="Address",font=("gody old style",15),bg="white").place(x=50,y=270)
        lbl_salary=Label(self.root,text="Salary",font=("gody old style",15),bg="white").place(x=595,y=270)
               
        self.txt_address=Text(self.root,font=("gody old style",15),bg="lightyellow")
        self.txt_address.place(x=150,y=270,width=400,height=60)
        txt_salary=Entry(self.root,textvariable=self.var_salary,font=("gody old style",15),bg="lightyellow",state="readonly").place(x=680,y=270,width=180)
        self.var_salary.set("NA")
        
        #=======Button================
        
        btn_add=Button(self.root,text="Save",command=self.add,font=("gody old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=400,width=150,height=30)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("gody old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=700,y=400,width=150,height=30)
          
#===============================================================================================================================
#==========================Insert============================

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","Employee Id Must be required",parent=self.root)
            if self.var_name.get()=="" or self.var_email.get()=="" or self.var_contact.get()=="" or self.var_dob.get()=="" or self.var_doj.get()=="" or self.var_pass.get()=="" or self.var_salary.get()=="":
                messagebox.showerror("Error","All filed are required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID already assigned , try Different",parent=self.root)
                else:
                    cur.execute("Insert into employee (eid,name,email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                                        self.var_emp_id.get(),
                                        self.var_name.get(),
                                        self.var_email.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),
                                        self.var_dob.get(),
                                        self.var_doj.get(),
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.txt_address.get('1.0',END),
                                        self.var_salary.get()             
                                ))
                    con.commit()
                    messagebox.showinfo("Success","Employee Addedd Successfully",parent=self.root)  
                    self.root.destroy()
                    os.system("python login.py")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    #=======================clear==========================
    
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_utype.set("Select")
        self.txt_address.delete('1.0',END)
        self.var_salary.set("")  
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")        
        self.show()
        
if __name__=="__main__":        
    root=Tk()
    obj=employeeClass(root)
    root.mainloop()