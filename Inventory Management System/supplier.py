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

class supplierClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1270x618+250+125")
        self.root.title("Inventory Management System | Developed By Ansh")
        self.root.config(bg="white")
        self.root.focus_force()
        
        #===================All Variables=======================
        
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        
        self.var_sup_invoice=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        
        #======================Search Frame======================
        
        lbl_search=Label(self.root,text="Invoice No",bg="white",font=("goudy old style",15))
        lbl_search.place(x=790,y=80)
        
        txt_search=Entry(self.root,textvariable=self.var_searchtxt,font=("gody old style",15),bg="lightyellow").place(x=890,y=80,width=200,height=30)
        btn_search=Button(self.root,text="Search",command=self.search,font=("gody old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=1100,y=80,width=120,height=30)
        
        #======================Title================
        
        title=Label(self.root,text="Manage Supplier Details",font=("gody old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=50,y=10,width=1170,height=40)
        
        #======================Content==================
        #=====Row1=====
        
        lbl_suoolier_invoice=Label(self.root,text="Invoice No",font=("gody old style",15),bg="white").place(x=50,y=80) 
        txt_suoolier_invoice=Entry(self.root,textvariable=self.var_sup_invoice,font=("gody old style",15),bg="lightyellow").place(x=180,y=80,width=180)
        #=====Row2=====
        
        lbl_name=Label(self.root,text="Name",font=("gody old style",15),bg="white").place(x=50,y=120)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("gody old style",15),bg="lightyellow").place(x=180,y=120,width=180)
        
        #=====Row3=====
        
        lbl_contact=Label(self.root,text="Contact",font=("gody old style",15),bg="white").place(x=50,y=160)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("gody old style",15),bg="lightyellow").place(x=180,y=160,width=180)
        
        #=====Row4=====
        
        lbl_desc=Label(self.root,text="Description",font=("gody old style",15),bg="white").place(x=50,y=200)      
        self.txt_desc=Text(self.root,font=("gody old style",15),bg="lightyellow")
        self.txt_desc.place(x=180,y=200,width=510,height=150)
        
        #=======Button================
        
        btn_add=Button(self.root,text="Save",command=self.add,font=("gody old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=400,width=120,height=35)
        btn_update=Button(self.root,text="Update",command=self.update,font=("gody old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=310,y=400,width=120,height=35)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("gody old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=440,y=400,width=120,height=35)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("gody old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=570,y=400,width=120,height=35)

        #=======================Supplier Details View============================
        
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=800,y=140,width=420,height=400)
        
        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
        
        self.supplierTables=ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTables.xview)
        scrolly.config(command=self.supplierTables.yview)
        
        self.supplierTables.heading("invoice",text="Invoice No")
        self.supplierTables.heading("name",text="Name")
        self.supplierTables.heading("contact",text="Contact")
        self.supplierTables.heading("desc",text="Description")
        
        self.supplierTables["show"]="headings"
        
        self.supplierTables.column("invoice",width=90)
        self.supplierTables.column("name",width=100)
        self.supplierTables.column("contact",width=100)
        self.supplierTables.column("desc",width=100)
        
        self.supplierTables.pack(fill=BOTH,expand=1)
        self.supplierTables.bind("<ButtonRelease-1>",self.get_data)
        
        self.show()
        
#===============================================================================================================================
#==========================Insert============================

    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Invoice number already assigned , try Different",parent=self.root)
                else:
                    cur.execute("Insert into supplier (invoice,name,contact,desc) values(?,?,?,?)",(
                                        self.var_sup_invoice.get(),
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.txt_desc.get('1.0',END)
                                                    
                                ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Addedd Successfully",parent=self.root)  
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    #======================Show Data========================
    
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from supplier")
            rows=cur.fetchall()
            self.supplierTables.delete(*self.supplierTables.get_children())
            for row in rows:
                self.supplierTables.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    def get_data(self,ev):
        f=self.supplierTables.focus()
        content=(self.supplierTables.item(f)) 
        row=content['values']
        self.var_sup_invoice.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete('1.0',END)
        self.txt_desc.insert(END,row[3])
                                
        
    #=======================Update===========================
    
    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice Number Must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid invoice number",parent=self.root)
                else:
                    cur.execute("Update supplier set name=?,contact=?,desc=? where invoice=?",(
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.txt_desc.get('1.0',END),
                                        self.var_sup_invoice.get()         
                                ))
                    con.commit()
                    messagebox.showinfo("Success","Supplier Update Successfully",parent=self.root)  
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    #===========================Delete========================
    
    def delete(self):            
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice Number Must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where invoice=?",(self.var_sup_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice Number",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete ?",parent=self.root)
                    if op==True:    
                        cur.execute("delete from supplier where invoice=?",(self.var_sup_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Supplier Delete Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

            
    #=======================clear==========================
    
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete('1.0',END) 
        self.var_searchtxt.set("")        
        self.show()
    
    #====================Search======================
    
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchtxt.get=="":
                messagebox.showerror("Error","Invoice Number should be required",parent=self.root)
            else:
                cur.execute("select * from supplier where invoice=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.supplierTables.delete(*self.supplierTables.get_children())
                    self.supplierTables.insert('',END,values=row) 
                else:
                    messagebox.showerror("Error","No Record found...!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
if __name__=="__main__":        
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()