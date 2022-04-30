import imp
from re import L
import sqlite3
from tkinter import*
from turtle import title
from unicodedata import category
from PIL import Image,ImageTk
from employe import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import time
from tkinter import messagebox
import os

class IMS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x800+0+0")
        self.root.title("Inventory Management System | Developed By Ansh")
        self.root.config(bg="white")
        
        #====================Title=============
        
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Mangement System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #===================Button Logout=================
        
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1350,y=10,height=50,width=150)

        #=========Clock=============
        
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Mangement System\t\t\t Date: dd-mm-yyyy\t\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        #=========Left Menu======================
        
        self.MenuLogo=Image.open("images/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,300),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        
        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=250,height=670)
        
        lab_menuLogo=Label(LeftMenu,image=self.MenuLogo)
        lab_menuLogo.pack(side=TOP,fill=X)
        
        self.icon_side=PhotoImage(file="images/side.png")
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
        
        btn_employee=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,text="Category",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Product",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(LeftMenu,text="Exit",command=self.exit,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        #====================Content======================
        
        self.lbl_employee=Label(self.root,text="Total Employee\n[0]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=400,y=120,height=160,width=300)
        
        self.lbl_supplier=Label(self.root,text="Total Suppliers\n[0]",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_supplier.place(x=750,y=120,height=160,width=300)
        
        self.lbl_category=Label(self.root,text="Total Category\n[0]",bd=5,relief=RIDGE,bg="#009688",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_category.place(x=1100,y=120,height=160,width=300)
        
        self.lbl_product=Label(self.root,text="Total Product\n[0]",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_product.place(x=550,y=350,height=160,width=300)
        
        self.lbl_sales=Label(self.root,text="Total Sales\n[0]",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=950,y=350,height=160,width=300)
        
        #==============Footer=================
        
        lbl_footer=Label(self.root,text="IMS-Inventory Mangement System | Developed By Ansh\nFor Any Technical Issue Contact: anshgalani@yahoo.com",font=("times new roman",12,"bold"),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()
        
#===========================================================================================================================

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
        
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
        
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)
        
    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win) 
        
    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win) 
        
    #==================Udate Lable============
    
    def update_content(self):
        con=sqlite3.connect(database='ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f"Total Products\n[{str(len(product))}]")
            
            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n[{str(len(supplier))}]")
       
            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f"Total Category\n[{str(len(category))}]")
       
            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_employee.config(text=f"Total Employees\n[{str(len(employee))}]")
            
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales \n[{str(bill)}]')
            
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Mangement System\t\t\t Date: {str(date_)}\t\t\t Time: {str(time_)}",font=("times new roman",15),bg="#4d636d",fg="white")  
            self.lbl_clock.after(200,self.update_content) 
        
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    #==================Logout==================
    
    def logout(self):
        self.root.destroy()
        os.system("python login.py")
        
    #==============Exit===============
    def exit(self):
        self.root.destroy()
            
if __name__=="__main__":        
    root=Tk()
    obj=IMS(root)
    root.mainloop()