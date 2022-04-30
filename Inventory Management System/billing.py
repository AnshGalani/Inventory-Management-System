from tkinter import*
from turtle import update
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile

class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x800+0+0")
        self.root.title("Inventory Management System | Developed By Ansh")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        
        #====================Title=============
        
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="Inventory Mangement System",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #===================Button Logout=================
        
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1350,y=10,height=50,width=150)

        #=========Clock=============
        
        self.lbl_clock=Label(self.root,text="Welcome to Inventory Mangement System\t\t\t Date: dd-mm-yyyy\t\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        #============Product Frame================
        
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=450,height=650)
        
        #====================Title===================
        
        pTitle=Label(ProductFrame1,text="All Product",font=("goudy old style",26,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        
        #=================Product Search Frame==================
        self.var_serach=StringVar()
        
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=50,width=438,height=90)
        
        lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        
        lbl_search=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        txt_search=Entry(ProductFrame2,textvariable=self.var_serach,font=("times new roman",15),bg="lightyellow").place(x=128,y=48,width=160,height=22)
       
        #====================Button======================
    
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=320,y=45,width=100,height=25)
        btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=320,y=10,width=100,height=25)
        
        #===============Product Detail Frame====================
        
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=145,width=438,height=470)
        
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
        
        self.product_table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        
        self.product_table.heading("pid",text="P ID")
        self.product_table.heading("name",text="Name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("qty",text="Quantity")
        self.product_table.heading("status",text="Status")
        self.product_table["show"]="headings"
        self.product_table.column("pid",width=40)
        self.product_table.column("name",width=100)
        self.product_table.column("price",width=100)
        self.product_table.column("qty",width=50)
        self.product_table.column("status",width=90)
        
        self.product_table.pack(fill=BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)
        
        lbl_note=Label(ProductFrame1,text="Note: ' Enter 0 Qunatity To Remove Product From The Cart '",font=("goudy old style",12),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)
        
        #=====================Cutomer Frame========================
        
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=500,y=110,width=530,height=70)
        
        cTitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)
        
        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)
        txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=35,width=180)
       
        lbl_contact=Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=270,y=35)
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=380,y=35,width=140)
        
        #===============Cal Cart Frame====================
        
        Cal_cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_cart_Frame.place(x=500,y=190,width=530,height=450)
        
        #===============Calculator Frame====================
        
        self.var_cal_input=StringVar()
        
        Cal_Frame=Frame(Cal_cart_Frame,bd=8,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=430)
        
        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state="readonly",justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)
        
        btn_7=Button(Cal_Frame,text='7',font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=23,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text='8',font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=23,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text='9',font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=23,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=23,cursor="hand2").grid(row=1,column=3)
        
        btn_4=Button(Cal_Frame,text='4',font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=23,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text='5',font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=23,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text='6',font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=23,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=23,cursor="hand2").grid(row=2,column=3)
    
        btn_1=Button(Cal_Frame,text='1',font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=23,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text='2',font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=23,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text='3',font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=23,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=23,cursor="hand2").grid(row=3,column=3)
        
        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=23,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='C',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=23,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=23,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=23,cursor="hand2").grid(row=4,column=3)
        
        #===============Cart Frame====================
        
        cart_Frame=Frame(Cal_cart_Frame,bd=3,relief=RIDGE)
        cart_Frame.place(x=280,y=8,width=245,height=432)
        
        self.cartTitle=Label(cart_Frame,text="Cart \t Total Product: [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)
        
        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)
        
        self.CartTable=ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("pid",text="P ID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Quantity")
        self.CartTable["show"]="headings"
        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=90)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=70)
        
        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        
        #===============Add Cart Widgets Frame====================
        
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()
        
        Add_CartwidgetsFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        Add_CartwidgetsFrame.place(x=500,y=645,width=530,height=120)
        
        lbl_p_name=Label(Add_CartwidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(Add_CartwidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)
        
        lbl_p_price=Label(Add_CartwidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(Add_CartwidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)
        
        lbl_p_qty=Label(Add_CartwidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_qty=Entry(Add_CartwidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)
        
        self.lbl_instock=Label(Add_CartwidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=80)
        
        btn_clear_cart=Button(Add_CartwidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=80,width=150,height=30)
        btn_add_cart=Button(Add_CartwidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=80,width=180,height=30)
        
        #============Billing Area==================
        
        billFreame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFreame.place(x=1080,y=110,width=450,height=500)
        
        bTitle=Label(billFreame,text="Customer Bill",font=("goudy old style",26,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        
        scrolly=Scrollbar(billFreame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        
        self.text_bill_area=Text(billFreame,yscrollcommand=scrolly.set)
        self.text_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.text_bill_area.yview)
        
        #=====================Billing Lable=====================
        
        billMenuFreame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        billMenuFreame.place(x=1080,y=615,width=450,height=150)
        
        self.lbl_amnt=Label(billMenuFreame,text="Bill Amount\n[0]",font=("goudy old style",13,"bold"),bg="#3f51b5",fg="white",bd=2)
        self.lbl_amnt.place(x=4,y=7,width=125,height=70)
        
        self.lbl_discount=Label(billMenuFreame,text="Discount\n[5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white",bd=2)
        self.lbl_discount.place(x=138,y=7,width=125,height=70)
        
        self.lbl_net_pay=Label(billMenuFreame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white",bd=2)
        self.lbl_net_pay.place(x=272,y=7,width=170,height=70)
        
       #====================Billing Button================
        
        btn_print=Button(billMenuFreame,text="Print",cursor="hand2",command=self.print_bill,font=("goudy old style",15,"bold"),bg="lightgreen",fg="white",bd=2)
        btn_print.place(x=4,y=90,width=125,height=50)
        
        btn_clear_all=Button(billMenuFreame,text="Clear All",command=self.clear_all,cursor="hand2",font=("goudy old style",15,"bold"),bg="gray",fg="white",bd=2)
        btn_clear_all.place(x=138,y=90,width=125,height=50)
        
        btn_generate=Button(billMenuFreame,text="Generate Bill/Save Bill",command=self.generate_bill,cursor="hand2",font=("goudy old style",13,"bold"),bg="#009688",fg="white",bd=2)
        btn_generate.place(x=272,y=90,width=170,height=50)
        
        #================Footer=========================
        
        footer=Label(self.root,text="IMS-Inventory Management System | Developed By Ansh\nFor Any Technical Issue Contact: anshgalani@yahoo.com",font=("times new roman",11,"bold"),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        
        self.show()
        #self.bill_top()
        self.update_date_time()
#=========================all function==================
        
    def get_input(self,num):
        xnum=self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)
        
    def clear_cal(self):
        self.var_cal_input.set('')   
        
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))  
      
    #================show All===============
    
    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
            
    #=====================Search======================   
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_serach.get()=="":
                messagebox.showerror("Error","Please Insert Product Name",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_serach.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END,values=row) 
                else:
                    messagebox.showerror("Error","No Record found...!",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    
    def get_data(self,ev):
        f=self.product_table.focus()
        content=(self.product_table.item(f)) 
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
        
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f)) 
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        
    #==================Add Update Cart==================    
        
    def add_update_cart(self):
        if self.var_pid.get()=='':
           messagebox.showerror('Error',"Please Select Product from the list",parent=self.root) 
        elif self.var_qty.get()=='':
            messagebox.showerror('Error',"Quanty Is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Out of Stock ",parent=self.root)
        
        else:
            price_cal=self.var_price.get()
            qty_cal=self.var_qty.get()
            cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
            
            #=============Update Cart================
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present\nDo you want to update| remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal #Price
                        self.cart_list[index_][3]=self.var_qty.get() #qty
            else:           
                self.cart_list.append(cart_data)
                
            self.show_cart()
            self.bill_update()
            
    #==================Bill Update================
       
    def bill_update(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amount(Rs.)\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay(Rs.)\n{str(self.net_pay)}')
        
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")
        
    #===============Show Cart======================
       
    def show_cart(self):       
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
           
    #===============Generate Bill====================
    
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add Product to the Cart!!!",parent=self.root)
        else:
            #===========Bill Top=============
            self.bill_top()
            #===========Bill Middle==========
            self.bill_middle()
            #===========Bill Bottom==========
            self.bill_bottom()  
            
            fp=open(f'bill/{str(self.invoice)}.txt','w')    
            fp.write( self.text_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Bill has been Generated/Save",parent=self.root)
            
            self.chk_print=1
            
    #================================================================       
    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))  
        bill_top_temp=f'''
\t\t\tXYZ Inventory 
\tEmail: anshgalani@yahoo.com , Surat-395006
{str("="*53)}
 Customer Name: {self.var_cname.get()}
 Phone No. : {self.var_contact.get()}
 Bill No. : {str(self.invoice)}\t\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*53)}
 Product Name\t\tQTY\tRate\t\tValue 
{str("="*53)}
        '''
        self.text_bill_area.delete('1.0',END)
        self.text_bill_area.insert('1.0',bill_top_temp)
        
    #==================================================================     
    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*53)}     
 Bill Amount\t\t\t\t\tRs.{self.bill_amnt}
 Discount\t\t\t\t\tRs.{self.discount}
 Net Pay\t\t\t\t\tRs.{self.net_pay}
{str("="*53)}\n   
 \t\tThank You visit again
        '''
        self.text_bill_area.insert(END,bill_bottom_temp)    
        
    #==================================================================        
    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            price_one=self.var_price.get()
            for row in self.cart_list:
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'
                
                price=float(row[2])*int(row[3])
                price=str(price)
                self.text_bill_area.insert(END,"\n "+name+"\t\t"+row[3]+"\t"+price_one+"\t\tRs."+price)
                
                #===============Update Qty in product table===============
                
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid
                ))
                con.commit()
            con.close()
            self.show()    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)                
            
    #=============Clear Cart================
    
    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set('')
        
    #=============Clear All===============
    
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.text_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.clear_cart()
        self.show()
        self.show_cart()
        self.var_serach.set('')
    
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Mangement System\t\t\t Date: {str(date_)}\t\t\t Time: {str(time_)}",font=("times new roman",15),bg="#4d636d",fg="white")  
        self.lbl_clock.after(200,self.update_date_time) 
         
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo('Print',"Please wait while printing",parent=self.root)   
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.text_bill_area.get('1.0',END))
            os.startfile(new_file,'print')  
        else:
            messagebox.showerror('Print',"Please Generate Bill , to print the receipt",parent=self.root) 
            
    #================Logout=================
    def logout(self):
        self.root.destroy()
        os.system("python login.py")      
            
if __name__=="__main__":        
    root=Tk()
    obj=BillClass(root)
    root.mainloop()