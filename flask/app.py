import mysql.connector as mysql
import datetime

today = datetime.date.today()

from flask import *
app=Flask(__name__)
@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers[ 'Cache-control' ]='no-store,max-age=0'
    return response
app.secret_key='email'
app.secret_key='uname'
@app.route('/')
def home():
    return render_template("home.html")
@app.route('/register')
def register():
    return render_template('register1.html')
@app.route('/check_register')
def check_register():
    firstname=request.args.get('fname')
    lastname=request.args.get('lname')
    address=request.args.get("address")
    mobile=request.args.get("mobile")
    email=request.args.get('email')
    password=request.args.get('password')
    cpassword=request.args.get('cpassword')
    tupl=firstname+lastname
    print(tupl)
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("insert into customers(cname,Address,cmobile,email,password) values(%s,%s,%s,%s,%s)",(tupl,address,mobile,email,password))
    con.commit()
    con.close()
    if(cur.rowcount==0):
        msg="your Data saved Successfully"
        return render_template('login1.html')
    else:
        session["email"]=email
        return render_template("login1.html")
@app.route('/check_login1')
def check_login():
    username=request.args.get('uname')
    password=request.args.get('pswd')
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("select * from customers where email=%s and password=%s",(username,password))
    results=cur.fetchall()
    if(len(results)==0):
        msg="Invalid Username or password"
        return render_template("login1.html",msg=msg)
    else:
        session["email"]=username
        return redirect("/login1")
@app.route('/check_login2')
def check_login2():
    username=request.args.get('email')
    password=request.args.get('pswd')
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("select * from admin where email=%s and password=%s",(username,password))
    result=cur.fetchall()
    if(len(result)==0):
        msg="Invalid Username or password"
        return render_template("login2.html",msg=msg)
    else:
        session["uname"]=username
        return redirect('/login2')
@app.route('/login1')
def login1():
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    if("email" in session):
        cur.execute("select * from customers where email=%s",(session["email"],))
        results=cur.fetchall()
        for value in results:
            result1=value[1]
            result3=value[3]
        return render_template('customer-order-details.html',msg1=result1,msg3=result3,date=today)
        # return render_template('customer-order-details.html')
    else:
        return render_template("login1.html")
        
@app.route('/login2')
def login2():
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    if("uname" in session):
        return render_template("homepage2.html")
    else:
        return render_template('login2.html')
@app.route('/help')
def help():
    return render_template('help.html')
@app.route('/services')
def services():
    return render_template('services.html')
@app.route('/guest')
def guest():
    return render_template('guest.html') 
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/contactus')
def contactus():
    return render_template('contacts.html')
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
@app.route('/admin')
def admin():
    return render_template('admin.html')
@app.route('/homepage1')
def homepage():
    values=[]
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("select iname from items")
    result=cur.fetchall()
    for value in result:
        values.append(value[(0)])
    value0=values[0]
    value1=values[1]
    value2=values[2]
    return render_template('homepage1.html',value0=value0,value1=value1,value2=value2)
@app.route('/add-purchase-details')
def addpurchase():
    address=request.args.get("address")
    sname=request.args.get("sname")
    quantity=request.args.get("quantity")
    rate=request.args.get("rate")
    amount=request.args.get("amount")
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("insert into purchaseregister(purdate,address) values (%s, %s)",(today,address))
    cur.execute('SELECT LAST_INSERT_ID()')
    ppid = cur.fetchone()
    for pid in ppid:
        pid=pid
    cur.execute("select sid from stockitems where sname=%s",(sname,))
    result=cur.fetchall()
    for tuple in result:
        sid=tuple[0]
    cur.execute("insert into purchasedetails values(%s, %s, %s, %s, %s)",(sid,pid,quantity,rate,amount))
    con.commit()
    return redirect('/purchase-details')
@app.route('/purchase-details')
def purchasedetails():
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT purdate, address, sname, unit, rate, amount FROM purchaseregister pr JOIN purchasedetails pd ON pr.pid = pd.pid JOIN stockitems s ON pd.sid = s.sid and purdate=curdate() ")
    result=cur.fetchall()
    return render_template('purchase-det2.html',result=result)
@app.route('/customer-orders')
def customerorders():
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT cname,Address,odate,iname,quantity,amount,ddate from corders,customers,items,codetails where corders.cid=customers.cid and corders.oid=codetails.oid and codetails.iid=items.iid and odate = curdate()")
    result=cur.fetchall()
    return render_template('customer-orders.html',date=today,result=result)
@app.route('/check-insert-offline-order')
def checkinsertofflineorder():
    cname=request.args.get('new_cname')
    address=request.args.get('new_address')
    mobile=request.args.get('new_mobile')
    pname=request.args.get('new_name')
    ddate=request.args.get('new_ddate')
    qty=request.args.get('new_quantity')
    amount=request.args.get('new_amount')
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("insert into customers(cname, Address, cmobile) values (%s, %s, %s)", (cname, address, mobile))
    cur.execute('SELECT LAST_INSERT_ID()')
    ccid = cur.fetchone()
    for cid in ccid:
        cid=cid
    con.commit()
    cur.execute('select iid from items where iname=%s',(pname,))
    iiid=cur.fetchall()
    for tuple in iiid:
        for iid in tuple:
            id=iid
    cur.execute("insert into corders(odate, cid, ddate) values (%s, %s, %s)", (today, cid, ddate))
    cur.execute('SELECT LAST_INSERT_ID()')
    ooid = cur.fetchone()
    for oid in ooid:
        oid=oid
    con.commit()
    cur.execute("insert into codetails(oid,iid,quantity,amount) values (%s, %s, %s, %s)", (oid,iid,qty,amount))
    con.commit()
    return redirect('/customer-orders')
@app.route('/customer-order')
def customerorder():
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("select cname,address from customers where email=%s",(session["email"],))
    email=cur.fetchall()
    cur.execute('SELECT oid FROM corders ORDER BY oid DESC LIMIT 1')
    ooid = cur.fetchone()
    for oid in ooid:
        oid=oid
    cur.execute('select oid,odate,ddate from corders where oid=%s',(oid,))
    odetails=cur.fetchall()
    for od in odetails:
        od=od[0]
    cur.execute("select iname,quantity,amount from codetails c,items i where c.iid=i.iid and oid=%s",(od,))
    unit=cur.fetchall()
    print(unit)
    print(email)
    return render_template('shipped.html',email=email,unit=unit,odetails=odetails)
@app.route('/check-insert-order')
def checkinsertorder():
    pname=request.args.get('new_name')
    ddate=request.args.get('new_ddate')
    qty=request.args.get('new_quantity')
    amount=request.args.get('new_amount')
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute('select iid from items where iname=%s',(pname,))
    iiid=cur.fetchall()
    for tuple in iiid:
        for iid in tuple:
            id=iid
    cur.execute("select cid from customers where email=%s",(session["email"],))
    email=cur.fetchall()
    for tuple in email:
        for cid in tuple:
            cid=cid
    cur.execute("insert into corders(odate, cid, ddate) values (%s, %s, %s)", (today, cid, ddate))
    cur.execute('SELECT LAST_INSERT_ID()')
    ooid = cur.fetchone()
    for oid in ooid:
        oid=oid
    con.commit()
    cur.execute("insert into codetails(oid,iid,quantity,amount) values (%s, %s, %s, %s)", (oid,iid,qty,amount))
    con.commit()
    return redirect('/customer-order')
@app.route('/vieworders')
def vieworders():
    status=[]
    date=[]
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT cname,Address,odate,iname,quantity,amount,ddate from corders,customers,items,codetails where corders.cid=customers.cid and corders.oid=codetails.oid and codetails.iid=items.iid and email=%s",(session["email"],))
    results=cur.fetchall()
    for result in results:
        if(result[6]<today):
            status="Delivered"
            date.append(status)
        else:
            status="Pending" 
            date.append(status)
    return render_template('vieworders.html',details=results,date=date)
@app.route('/orders')
def orders():
    return redirect("/login1")
@app.route('/homepage2')
def customerordessssr():
    return render_template('homepage2.html')
@app.route('/seeorders')
def seeorders():
    return render_template('seeorders.html')
@app.route('/seepurchases')
def sees():
    return render_template('seepurchases.html')
@app.route('/seepayments')
def seepayments():
    return render_template('seepayments.html')
@app.route('/payments')
def checkpayments():
    oid=[]
    data=[]
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT c.oid FROM corders c LEFT JOIN payements p ON c.oid = p.oid WHERE p.oid IS NULL")
    result=cur.fetchall()

    for tuple in result:
        oid.append(tuple[0])

    for id in oid:
        cur.execute("select odate,cname,iname,quantity,amount from customers cr,items, corders c,codetails cs where c.cid=cr.cid and c.oid=cs.oid and cs.iid=items.iid and c.oid=%s",(id,))
        rows=cur.fetchone()
        if rows:
            data.append(rows)   
    
    
    return render_template('payments.html',orders=data,)
@app.route("/save")
def save():
    oid=[]
    pdate=request.args.get("pdate")
    print(pdate)
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT c.oid FROM corders c LEFT JOIN payements p ON c.oid = p.oid WHERE p.oid IS NULL")
    result=cur.fetchall()
    for tuple in result:
        oid.append(tuple[0])
    print(oid)
    for id in oid:
        cur.execute("insert into payements(oid) values(%s)",(id,))
        cur.execute("insert into payements(paydate) values(%s)",(pdate,))
    con.commit()
    return redirect('/payments')
@app.route('/expences')
def expences():
    return render_template('expences.html')
@app.route('/dailyreport')
def dailyreport():
    incomes=[]
    expences=[]
    total1=0
    total2=0
    date=request.args.get("date")
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT odate,cname,iname,quantity,price, amount FROM corders INNER JOIN customers ON corders.cid = customers.cid INNER JOIN codetails ON corders.oid = codetails.oid INNER JOIN items ON codetails.iid = items.iid and odate=%s",(date,))
    orders=cur.fetchall()
    cur.execute("SELECT purdate, address, sname, unit, rate, amount FROM purchasedetails INNER JOIN purchaseregister ON purchasedetails.pid = purchaseregister.pid INNER JOIN stockitems ON purchasedetails.sid = stockitems.sid and purdate=%s",(date,))
    purchases=cur.fetchall()
    for amountss in orders:
        amount=amountss[5]
        incomes.append(amount)
    for amountss in purchases:
        amount=amountss[5]
        expences.append(amount)
    for income in incomes:
        total1=total1+income
    for expence in expences:
        total2=total2+expence
    
    total=total1-total2
    
    return render_template('dailyreport.html',orders=orders,purchases=purchases,total1=total1,total2=total2,total=total)
@app.route('/monthlyreport')
def monthlyreport():
    incomes=[]
    expences=[]
    total1=0
    total2=0
    months=request.args.get("month")
    datetime_object = datetime.datetime.strptime(months, "%Y-%m")
    month=datetime_object.month
    print(month)
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT odate,cname,iname,quantity,price, amount FROM corders INNER JOIN customers ON corders.cid = customers.cid INNER JOIN codetails ON corders.oid = codetails.oid INNER JOIN items ON codetails.iid = items.iid and month(odate)=%s",(month,))
    orders=cur.fetchall()
    cur.execute("SELECT purdate, address, sname, unit, rate, amount FROM purchasedetails INNER JOIN purchaseregister ON purchasedetails.pid = purchaseregister.pid INNER JOIN stockitems ON purchasedetails.sid = stockitems.sid and month(purdate)=%s",(month,))
    purchases=cur.fetchall()
    for amountss in orders:
        amount=amountss[5]
        incomes.append(amount)
    for amountss in purchases:
        amount=amountss[5]
        expences.append(amount)
    for income in incomes:
        total1=total1+income
    for expence in expences:
        total2=total2+expence
    
    total=total1-total2
    
    return render_template('monthlyreport.html',orders=orders,purchases=purchases,total1=total1,total2=total2,total=total)
   
@app.route('/check-see-orders')
def checkseeorders():
    date=request.args.get("date")
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT ddate,cname,Address,cmobile,iname,quantity,amount from corders,customers,items,codetails where corders.cid=customers.cid and corders.oid=codetails.oid and codetails.iid=items.iid and odate=%s",(date,))
    odate=cur.fetchall()
    if(len(odate)==0):
        msg="Data Not Found"
        return render_template("seeorders.html",msg=msg)
    else:
        for tuple in odate:
            value=tuple
        return render_template('seeorders.html',orders=odate)
@app.route('/check-see-purchases')
def seepurchases():
    purdate=request.args.get("date")
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT purdate,address,sname,unit,rate,amount from purchasedetails,purchaseregister,stockitems where purchasedetails.pid=purchaseregister.pid and purchasedetails.sid=stockitems.sid and purdate=%s",(purdate,))
    purchases=cur.fetchall()
    if(len(purchases)==0):
        msg="Data Not Found"
        return render_template("seepurchases.html",msg=msg)
    else:
        return render_template('seepurchases.html',purchases=purchases )
    return render_template('seepurchases.html')
@app.route("/check-see-payments")
def checkseepayments():
    paydate=request.args.get("date")
    print(paydate)
    con=mysql.connect(host='localhost',user='root',password='',database='project')
    cur=con.cursor()
    cur.execute("SELECT paydate,cname,iname,quantity,amount from payements,customers,items,corders,codetails where payements.oid=corders.oid and corders.cid=customers.cid and codetails.iid=items.iid and paydate=%s",(paydate,))
    purchases=cur.fetchall()
    if(len(purchases)==0):
        msg="Data Not Found"
        return render_template("seepayments.html",msg=msg)
    else:
        return render_template('seepayments.html',purchases=purchases )
    return render_template('seepayments.html')
@app.route('/logout1')
def logout1():
    if "email" in session:
        session.pop("email")
        return render_template('home.html')
    else:
        return redirect("/login1")

@app.route('/logout2')
def logout2():
    if "uname" in session:
        session.pop("uname")
        return render_template('home.html')
    else:
        return redirect("/login2")
        
