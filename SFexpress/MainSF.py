from flask import Flask, render_template, redirect, url_for, request, session
import pymysql
import json
import os
import time
from datetime import date
import decimal
import flask.json

class MyJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        if isinstance(obj, date):
            return obj.isoformat()

        return super(MyJSONEncoder, self).default(obj)


#app = Flask(__name__, static_url_path='/image')
app = Flask(__name__, static_url_path='/static')
app.json_encoder = MyJSONEncoder

db = pymysql.connect("localhost", "root", "Kamenride1234", "sf_transport")
##db = pymysql.connect("localhost","phpmyadmin","Kamenride1234","bookshop")

#def read_file(filename):
#    with open(filename, 'r') as file:
#        binarydata = file.read()
#    return binarydata

def write_file(data, filename):
    with open(filename, 'w') as file:
        print("Class", type(data))
        file.write(data)


@app.route('/')
def home():
    return render_template('Main.html')
#    return '<h1>Hello, World!</h1>'
#    return (getbooknewid())

@app.route("/tableimport0")
def tableimport0():
    return render_template('tableimport0.html')

@app.route('/tableimport1', methods=['POST', 'GET'])
def tableimport1():
    allmsg = ""
    allresult = ""

    sql1 = "TRUNCATE TABLE xcustomer"
    sql2 = """ INSERT INTO xcustomer (Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District) VALUES (%s,%s,%s,%s,%s)"""
    sql3 = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM xcustomer order by Customer_Key asc")
    sql4 = "TRUNCATE TABLE customer"
    sql5 = ("INSERT INTO customer SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM xcustomer order by Customer_Key asc")
    msg = importtable(sql1, sql2, sql3, sql4, sql5, 'xcustomer.json.txt')
    allmsg = allmsg + msg

    sql1 = "TRUNCATE TABLE xpurchase_order"
    sql2 = """ INSERT INTO xpurchase_order (Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total) VALUES (%s,%s,%s,%s,%s)"""
    sql3 = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM xpurchase_order order by Order_Key asc")
    sql4 = "TRUNCATE TABLE purchase_order"
    sql5 = ("INSERT INTO purchase_order SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM xpurchase_order order by Order_Key asc")
    msg = importtable(sql1, sql2, sql3, sql4, sql5, 'xpurchase_order.json.txt')
    allmsg = allmsg + msg

    sql1 = "TRUNCATE TABLE xorder_item"
    sql2 = """ INSERT INTO xorder_item (Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    sql3 = ("SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM xorder_item order by Order_Key asc")
    sql4 = "TRUNCATE TABLE order_item"
    sql5 = ("INSERT INTO order_item SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM xorder_item order by Order_Key asc")
    msg = importtable(sql1, sql2, sql3, sql4, sql5, 'xorder_item.json.txt')
    allmsg = allmsg + msg

    return render_template('tableimport1.html', msg=allmsg, result = allresult)

def importtable(sql1, sql2, sql3, sql4, sql5, filename):

#    error = None
    if request.method == 'POST':
        cursor = db.cursor()

        with open(os.path.dirname(__file__) + '/import/' + filename) as json_file:
            json_obj = json.load(json_file)

        cursor.execute(sql1)
#        cursor.execute("TRUNCATE TABLE xcustomer")

        for xrecord in json_obj:
#            print("Customer_Key:", xrecord["Customer_Key"])
            sql_insert_query = sql2
#            sql_insert_query = """ INSERT INTO xcustomer
#                                  (Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District) VALUES (%s,%s,%s,%s,%s)"""
            if filename == 'xcustomer.json.txt':
                insert_tuple = (xrecord["Customer_Key"], xrecord["Customer_Name"], xrecord["Customer_Gender"], xrecord["Customer_Address"], xrecord["Customer_District"])
            if filename == 'xpurchase_order.json.txt':
                insert_tuple = (xrecord["Order_Key"], xrecord["Customer_Key"], xrecord["Order_Date"], xrecord["Order_Count"], xrecord["Order_Total"])
            if filename == 'xorder_item.json.txt':
                insert_tuple = (xrecord["Order_Key"], xrecord["Item_Key"], xrecord["Item_Name"], xrecord["Item_Description"], xrecord["Item_Type"], xrecord["Item_Brand"], xrecord["Item_Size"], xrecord["Item_Cost"], xrecord["Item_Price"], xrecord["Item_Quantity"])

            result = cursor.execute(sql_insert_query, insert_tuple)
#            cursor.execute("INSERT INTO xcustomer (Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District) VALUES (%s,%s,%s,%s,%s)", (xrecord["Customer_Key"], xrecord["Customer_Name"], xrecord["Customer_Gender"], xrecord["Customer_Address"], xrecord["Customer_District"]))
        cursor.execute(sql4)
        cursor.execute(sql5)
        db.commit()

        cursor = db.cursor()
        sql = sql3
#        sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM xcustomer order by Customer_Key asc")
        cursor.execute(sql)
        db.commit()
#       db.close()
        json_data=[]
        result = cursor.fetchall()
#        for row in result:
#            json_data.append(dict(zip(row_headers,row)))
#            Customer_Name = row[0]
#            Customer_Phone_no = row[1]
#        return (Customer_Name)
        msg = "Import successfully added"
#        msg = tmp_orderimport_Data
#        return render_template('tableimport1.html')
#        return render_template('tableimport1.html', msg=msg, result = result)
        return render_template('tableimport1.html', msg=msg)
    else:
        return 'End'

@app.route("/tableexport0")
def tableexport0():
    return render_template('tableexport0.html')

@app.route('/tableexport1', methods=['POST', 'GET'])
def tableexport1():
    allmsg = ""
    allresult = ""

    sql1 = ("TRUNCATE TABLE xcustomer")
    sql2 = ("INSERT INTO xcustomer SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer order by Customer_Key asc")
    sql3 = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer order by Customer_Key asc")
    msg, result = exporttable(sql1, sql2, sql3, 'xcustomer.json.txt')
    allmsg = allmsg + msg

    sql1 = ("TRUNCATE TABLE xpurchase_order")
    sql2 = ("INSERT INTO xpurchase_order SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order order by Order_Key asc")
    sql3 = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order order by Order_Key asc")
    msg, result = exporttable(sql1, sql2, sql3, 'xpurchase_order.json.txt')
    allmsg = allmsg + msg

    sql1 = ("TRUNCATE TABLE xorder_item")
    sql2 = ("INSERT INTO xorder_item SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM order_item order by Order_Key, Item_Key asc")
    sql3 = ("SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM order_item order by Order_Key, Item_Key asc")
    msg, result = exporttable(sql1, sql2, sql3, 'xorder_item.json.txt')
    allmsg = allmsg + msg

    return render_template('tableexport1.html', msg=allmsg, result = allresult)

def exporttable(sql1, sql2, sql3, filename):
    error = None
    if request.method == 'POST':
#        tmp_Customer_Name = request.form['Customer_Name']
        cursor = db.cursor()
#        sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer order by Customer_Key asc")
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        db.commit()
        row_headers=[x[0] for x in cursor.description] #this will extract row headers
#       db.close()
        json_data=[]
        result = cursor.fetchall()
        for row in result:
            json_data.append(dict(zip(row_headers,row)))
#            Customer_Name = row[0]
#            Customer_Phone_no = row[1]
#        return (Customer_Name)


        msg = json.dumps(json_data, cls=MyJSONEncoder)
#        msg = "abc"
        write_file(json.dumps(json_data, cls=MyJSONEncoder), os.path.dirname(__file__) + '/export/' + filename)
#        return render_template('orderexport1.html', msg=msg, result = result)
#    else:
#        return 'End'
        return msg, result


@app.route("/customeraddrec0")
def customeraddrec0():
    return render_template('customeraddrec0.html')

@app.route('/customeraddrec1', methods=['POST', 'GET'])
def customeraddrec1():
    if request.method == 'POST':
        try:
            tmp_Customer_Key = request.form['Customer_Key']
            tmp_Customer_Name = request.form['Customer_Name']
            tmp_Customer_Gender = request.form['Customer_Gender']
            tmp_Customer_Address = request.form['Customer_Address']
            tmp_Customer_District = request.form['Customer_District']

            tmp_Customer_Key = getcustomernewid()
            cursor = db.cursor()
            sql = (
                        "INSERT INTO customer (Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District) VALUES ('" + tmp_Customer_Key + "','" + tmp_Customer_Name + "','" + tmp_Customer_Gender + "','" + tmp_Customer_Address + "','" + tmp_Customer_District + "')")
            #            sql = ("INSERT INTO officer (Officer_Key, Officer_Login_Key, Officer_Password, Officer_Name, Officer_Sex, Officer_DOE, Officer_Address, Officer_Login_Key) VALUES ('"+tmp_Officer_Key+"','5a','5b','5c','5','1990-01-02','5e','5f')")
            #            sql = ("INSERT INTO officer (Officer_Key, Officer_Login_Key, Officer_Password, Officer_Name, Officer_Sex, Officer_DOE, Officer_Address, Officer_Login_Key) VALUES ('"+tmp_Officer_Key+"','5','5a','5b','5','1998-11-07','5e','5f')")
            cursor.execute(sql)
            db.commit()
            msg = "Record successfully added"
        except:
            db.rollback()
            msg = "error in insert operation"
            msg = sql

        finally:
            #           return (sql)
            sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer where Customer_Key = '" + tmp_Customer_Key + "'")
            cursor.execute(sql)
            db.commit()
            result = cursor.fetchall()

            return render_template('customeraddrec1.html', msg=msg, result=result)
            cursor.close()


def getcustomernewid():
    customernewid = str(int(getlastkey('customer', 'Customer_Key')) + 1)
    return (customernewid)


def getlastkey(tablename, keyname):
    querylastkeysql = 'select ' + keyname + ' from ' + tablename + ' order by ' + keyname + ' desc'
    cursor = db.cursor()
    cursor.execute(querylastkeysql)
    db.commit()
    result = cursor.fetchall()
    for row in result:
        outkeyname = row[0]
#        result.close ()
#        db.close()
        return (str(outkeyname))


def customersqlfilter(tmp_Customer_Key, tmp_Customer_Name):
    customersqlfilter = "1 = 1"
    if tmp_Customer_Key != '':
        customersqlfilter = customersqlfilter + " and Customer_Key like '%" + tmp_Customer_Key + "%'"
    if tmp_Customer_Name != '':
        customersqlfilter = customersqlfilter + " and Customer_Name like '%" + tmp_Customer_Name + "%'"
    return (customersqlfilter)



@app.route('/customerupdaterec0')
def customerupdaterec0():    
    return render_template('customerupdaterec0.html',)


@app.route('/customerupdaterec1', methods=['POST', 'GET'])
def customerupdaterec1():
    error = None
    if request.method == 'POST':
        tmp_Customer_Name = request.form['Customer_Name']
        tmp_Customer_Address = request.form['Customer_Address']
        cursor = db.cursor()
        sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer where " + customersqlfilter(tmp_Customer_Name,tmp_Customer_Address) + " order by Customer_Key asc")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return render_template('customerupdaterec1.html', result = result)

@app.route('/customerupdaterec2', methods=['POST', 'GET'])
def customerupdaterec2():
    if request.method == 'POST':
#        tmp_Customer_Key = request.form['Customer_Key']
        tmp_Customer_Key = request.form['In_Customer_Key']
#        return (tmp_Customer_Key)
        cursor = db.cursor()
        sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer where Customer_Key = '"+tmp_Customer_Key+"'")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
#        for row in result:
#            Customer_Key = row[0]
#            Customer_Name = row[1]
#        return (Customer_Name)
        return render_template('customerupdaterec2.html', result = result)
    else:
        return 'End'

@app.route('/customerupdaterec3', methods=['POST', 'GET'])
def customerupdaterec3():
    if request.method == 'POST':
        try:
            tmp_Customer_Key = request.form['Customer_Key']
            tmp_Customer_Name = request.form['Customer_Name']
            tmp_Customer_Gender = request.form['Customer_Gender']
            tmp_Customer_Address = request.form['Customer_Address']
            tmp_Customer_District = request.form['Customer_District']

            cursor = db.cursor()
            tmp_Customer_Name = request.form['Customer_Name']
            sql = ("update customer set Customer_Name = '"+tmp_Customer_Name+"', Customer_Gender = '"+tmp_Customer_Gender+"', Customer_Address = '"+tmp_Customer_Address+"', Customer_District = '"+tmp_Customer_District+"' where Customer_Key = '"+tmp_Customer_Key+"'")
            
            cursor.execute(sql)
            db.commit()
            msg = "Record successfully updated"
        except:
            db.rollback()
            msg = "error in Update operation"

        finally:
            cursor = db.cursor()
            sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer where Customer_Key = '"+tmp_Customer_Key+"'")
            cursor.execute(sql)
            db.commit()
            result = cursor.fetchall()

            return render_template('customerupdaterec3.html', msg = msg, result = result)
            cursor.close()


@app.route("/customerqueryrec0")
def customerqueryrec0():
    return render_template('customerqueryrec0.html')

@app.route('/customerqueryrec1', methods=['POST', 'GET'])
def customerqueryrec1():
    error = None
    if request.method == 'POST':
        tmp_Customer_Name = request.form['Customer_Name']
        tmp_Customer_Address = request.form['Customer_Address']
        cursor = db.cursor()
        sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer where " + customersqlfilter(tmp_Customer_Name,tmp_Customer_Address) + " order by Customer_Key asc")
        cursor.execute(sql)
        db.commit()
#       db.close()
        result = cursor.fetchall()
#        for row in result:
#            Customer_Name = row[0]
#            Customer_Phone_no = row[1]
#        return (Customer_Name)
        return render_template('customerqueryrec1.html', result = result)

@app.route('/customerqueryrec2', methods=['POST', 'GET'])
def customerqueryrec2():
    if request.method == 'POST':
        tmp_Customer_Key = request.form['In_Customer_Key']
        cursor = db.cursor()
        sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer where Customer_Key = '"+tmp_Customer_Key+"'")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
#        for row in result:
#            Customer_Key = row[0]
#            Customer_Name = row[1]
#        return (Customer_Name)
        return render_template('customerqueryrec2.html', result = result)
    else:
        return 'End'


@app.route('/customerdeleterec0')
def customerdeleterec0():    
    return render_template('customerdeleterec0.html',)


@app.route('/customerdeleterec1', methods=['POST', 'GET'])
def customerdeleterec1():
    error = None
    if request.method == 'POST':
        tmp_Customer_Name = request.form['Customer_Name']
        tmp_Customer_Address = request.form['Customer_Address']
        cursor = db.cursor()
        sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer where " + customersqlfilter(tmp_Customer_Name,tmp_Customer_Address) + " order by Customer_Key asc")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return render_template('customerdeleterec1.html', result = result)

@app.route('/customerdeleterec2', methods=['POST', 'GET'])
def customerdeleterec2():
    if request.method == 'POST':
        tmp_Customer_Key = request.form['In_Customer_Key']
#        return (tmp_Customer_Key)
        cursor = db.cursor()
        sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer where Customer_Key = '"+tmp_Customer_Key+"'")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return render_template('customerdeleterec2.html', result = result)
    else:
        return 'End'

@app.route('/customerdeleterec3', methods=['POST', 'GET'])
def customerdeleterec3():
    if request.method == 'POST':
        try:
            tmp_Customer_Key = request.form['Customer_Key']
            tmp_Customer_Name = request.form['Customer_Name']
            tmp_Customer_Gender = request.form['Customer_Gender']
            tmp_Customer_Address = request.form['Customer_Address']
            tmp_Customer_District = request.form['Customer_District']
            cursor = db.cursor()
            tmp_Customer_Name = request.form['Customer_Name']
            sql = ("delete from customer where Customer_Key = '"+tmp_Customer_Key+"'")
            
            cursor.execute(sql)
            db.commit()
            msg = "Record successfully deleted"
        except:
            db.rollback()
            msg = "error in Delete operation"

        finally:
            sql = ("SELECT Customer_Key, Customer_Name, Customer_Gender, Customer_Address, Customer_District FROM customer where Customer_Key = '"+tmp_Customer_Key+"'")
            cursor.execute(sql)
            db.commit()
            result = cursor.fetchall()

            return render_template('customerdeleterec3.html', msg = msg, result = result)
            cursor.close()

@app.route("/orderaddrec0")
def orderaddrec0():
    return render_template('orderaddrec0.html')

@app.route('/orderaddrec1', methods=['POST', 'GET'])
def orderaddrec1():
    if request.method == 'POST':
        try:
            tmp_Order_Key = request.form['Order_Key']
            tmp_Customer_Key = request.form['Customer_Key']
            tmp_Order_Date = request.form['Order_Date']
            tmp_Order_Count = request.form['Order_Count']
            tmp_Order_Total = request.form['Order_Total']

            tmp_Order_Key = getordernewid()
            cursor = db.cursor()
            sql = (
                        "INSERT INTO purchase_order (Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total) VALUES ('" + tmp_Order_Key + "','" + tmp_Customer_Key + "','" + tmp_Order_Date + "','" + tmp_Order_Count + "','" + tmp_Order_Total + "')")
            #            sql = ("INSERT INTO officer (Officer_Key, Officer_Login_Key, Officer_Password, Officer_Name, Officer_Sex, Officer_DOE, Officer_Address, Officer_Login_Key) VALUES ('"+tmp_Officer_Key+"','5a','5b','5c','5','1990-01-02','5e','5f')")
            #            sql = ("INSERT INTO officer (Officer_Key, Officer_Login_Key, Officer_Password, Officer_Name, Officer_Sex, Officer_DOE, Officer_Address, Officer_Login_Key) VALUES ('"+tmp_Officer_Key+"','5','5a','5b','5','1998-11-07','5e','5f')")
            cursor.execute(sql)
            db.commit()
            msg = "Record successfully added"
        except:
            db.rollback()
            msg = "error in insert operation"
            msg = sql

        finally:
            #           return (sql)
            sql = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order where Order_Key = '" + tmp_Order_Key + "'")
            cursor.execute(sql)
            db.commit()
            result = cursor.fetchall()

            return render_template('orderaddrec1.html', msg=msg, result=result)
            cursor.close()


def getordernewid():
    customernewid = str(int(getlastkey('purchase_order', 'Order_Key')) + 1)
    return (customernewid)


def getlastkey(tablename, keyname):
    querylastkeysql = 'select ' + keyname + ' from ' + tablename + ' order by ' + keyname + ' desc'
    cursor = db.cursor()
    cursor.execute(querylastkeysql)
    db.commit()
    result = cursor.fetchall()
    for row in result:
        outkeyname = row[0]
#        result.close ()
#        db.close()
        return (str(outkeyname))


def ordersqlfilter(tmp_Order_Key, tmp_Customer_Key):
    ordersqlfilter = "1 = 1"
    if tmp_Order_Key != '':
        ordersqlfilter = ordersqlfilter + " and Order_Key like '%" + tmp_Order_Key + "%'"
    if tmp_Customer_Key != '':
        ordersqlfilter = ordersqlfilter + " and Customer_Key like '%" + tmp_Customer_Key + "%'"
    return (ordersqlfilter)


@app.route('/orderupdaterec0')
def orderupdaterec0():    
    return render_template('orderupdaterec0.html',)


@app.route('/orderupdaterec1', methods=['POST', 'GET'])
def orderupdaterec1():
    error = None
    if request.method == 'POST':
        tmp_Order_Key = request.form['Order_Key']
        tmp_Customer_Key = request.form['Customer_Key']
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order where " + ordersqlfilter(tmp_Order_Key,tmp_Customer_Key) + " order by Order_Key asc")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return render_template('orderupdaterec1.html', result = result)

@app.route('/orderupdaterec2', methods=['POST', 'GET'])
def orderupdaterec2():
    if request.method == 'POST':
#        tmp_Customer_Key = request.form['Customer_Key']
        tmp_Order_Key = request.form['In_Order_Key']
#        return (tmp_Customer_Key)
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order where Order_Key = '"+tmp_Order_Key+"'")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
#        for row in result:
#            Customer_Key = row[0]
#            Customer_Name = row[1]
#        return (Customer_Name)
        return render_template('orderupdaterec2.html', result = result)
    else:
        return 'End'

@app.route('/orderupdaterec3', methods=['POST', 'GET'])
def orderupdaterec3():
    if request.method == 'POST':
        try:
            tmp_Order_Key = request.form['Order_Key']
            tmp_Customer_Key = request.form['Customer_Key']
            tmp_Order_Date = request.form['Order_Date']
            tmp_Order_Count = request.form['Order_Count']
            tmp_Order_Total = request.form['Order_Total']

            cursor = db.cursor()
            tmp_Customer_Key = request.form['Customer_Key']
            sql = ("update purchase_order set Customer_Key = '"+tmp_Customer_Key+"', Order_Date = '"+tmp_Order_Date+"', Order_Count = '"+tmp_Order_Count+"', Order_Total = '"+tmp_Order_Total+"' where Order_Key = '"+tmp_Order_Key+"'")
            
            cursor.execute(sql)
            db.commit()
            msg = "Record successfully updated"
        except:
            db.rollback()
            msg = "error in Update operation"

        finally:
            cursor = db.cursor()
            sql = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order where Order_Key = '"+tmp_Order_Key+"'")
            cursor.execute(sql)
            db.commit()
            result = cursor.fetchall()

            return render_template('orderupdaterec3.html', msg = msg, result = result)
            cursor.close()

@app.route("/orderqueryrec0")
def orderqueryrec0():
    return render_template('orderqueryrec0.html')

@app.route('/orderqueryrec1', methods=['POST', 'GET'])
def orderqueryrec1():
    error = None
    if request.method == 'POST':
        tmp_Order_Key = request.form['Order_Key']
        tmp_Customer_Key = request.form['Customer_Key']
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order where " + ordersqlfilter(tmp_Order_Key,tmp_Customer_Key) + " order by Order_Key asc")
        cursor.execute(sql)
        db.commit()
#       db.close()
        result = cursor.fetchall()
#        for row in result:
#            Customer_Name = row[0]
#            Customer_Phone_no = row[1]
#        return (Customer_Name)
        return render_template('orderqueryrec1.html', result = result)

@app.route('/orderqueryrec2', methods=['POST', 'GET'])
def orderqueryrec2():
    if request.method == 'POST':
        tmp_Order_Key = request.form['In_Order_Key']
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order where Order_Key = '"+tmp_Order_Key+"'")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
#        for row in result:
#            Customer_Key = row[0]
#            Customer_Name = row[1]
#        return (Customer_Name)
        return render_template('orderqueryrec2.html', result = result)
    else:
        return 'End'

@app.route('/orderdeleterec0')
def orderdeleterec0():    
    return render_template('orderdeleterec0.html',)


@app.route('/orderdeleterec1', methods=['POST', 'GET'])
def orderdeleterec1():
    error = None
    if request.method == 'POST':
        tmp_Order_Key = request.form['Order_Key']
        tmp_Customer_Key = request.form['Customer_Key']
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order where " + ordersqlfilter(tmp_Order_Key,tmp_Customer_Key) + " order by Order_Key asc")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return render_template('orderdeleterec1.html', result = result)

@app.route('/orderdeleterec2', methods=['POST', 'GET'])
def orderdeleterec2():
    if request.method == 'POST':
        tmp_Order_Key = request.form['In_Order_Key']
#        return (tmp_Customer_Key)
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order where Order_Key = '"+tmp_Order_Key+"'")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return render_template('orderdeleterec2.html', result = result)
    else:
        return 'End'

@app.route('/orderdeleterec3', methods=['POST', 'GET'])
def orderdeleterec3():
    if request.method == 'POST':
        try:
            tmp_Order_Key = request.form['Order_Key']
            tmp_Customer_Key = request.form['Customer_Key']
            tmp_Order_Date = request.form['Order_Date']
            tmp_Order_Count = request.form['Order_Count']
            tmp_Order_Total = request.form['Order_Total']
            cursor = db.cursor()
            tmp_Customer_Key = request.form['Customer_Key']
            sql = ("delete from purchase_order where Order_Key = '"+tmp_Order_Key+"'")
            
            cursor.execute(sql)
            db.commit()
            msg = "Record successfully deleted"
        except:
            db.rollback()
            msg = "error in Delete operation"

        finally:
            sql = ("SELECT Order_Key, Customer_Key, Order_Date, Order_Count, Order_Total FROM purchase_order where Order_Key = '"+tmp_Order_Key+"'")
            cursor.execute(sql)
            db.commit()
            result = cursor.fetchall()

            return render_template('orderdeleterec3.html', msg = msg, result = result)
            cursor.close()

@app.route("/itemaddrec0")
def itemaddrec0():
    return render_template('itemaddrec0.html')

@app.route('/itemaddrec1', methods=['POST', 'GET'])
def itemaddrec1():
    if request.method == 'POST':
        try:
            tmp_Order_Key = request.form['Order_Key']
            tmp_Item_Key = request.form['Item_Key']
            tmp_Item_Name = request.form['Item_Name']
            tmp_Item_Description = request.form['Item_Description']
            tmp_Item_Type = request.form['Item_Type']
            tmp_Item_Brand = request.form['Item_Brand']
            tmp_Item_Size = request.form['Item_Size']
            tmp_Item_Cost = request.form['Item_Cost']
            tmp_Item_Price = request.form['Item_Price']
            tmp_Item_Quantity = request.form['Item_Quantity']

            tmp_Item_Key = getitemnewid()
            cursor = db.cursor()
            sql = (
                        "INSERT INTO order_item (Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity) VALUES ('" + tmp_Order_Key + "','" + tmp_Item_Key + "','" + tmp_Item_Name + "','" + tmp_Item_Description + "','" + tmp_Item_Type + "','" + tmp_Item_Brand + "','" + tmp_Item_Size + "','" + tmp_Item_Cost + "','" + tmp_Item_Price + "','" + tmp_Item_Quantity + "')")
            #            sql = ("INSERT INTO officer (Officer_Key, Officer_Login_Key, Officer_Password, Officer_Name, Officer_Sex, Officer_DOE, Officer_Address, Officer_Login_Key) VALUES ('"+tmp_Officer_Key+"','5a','5b','5c','5','1990-01-02','5e','5f')")
            #            sql = ("INSERT INTO officer (Officer_Key, Officer_Login_Key, Officer_Password, Officer_Name, Officer_Sex, Officer_DOE, Officer_Address, Officer_Login_Key) VALUES ('"+tmp_Officer_Key+"','5','5a','5b','5','1998-11-07','5e','5f')")
            cursor.execute(sql)
            db.commit()
            msg = "Record successfully added"
        except:
            db.rollback()
            msg = "error in insert operation"
            msg = sql

        finally:
            #           return (sql)
            sql = ("SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM order_item where Order_Key = '" + tmp_Item_Key + "'")
            cursor.execute(sql)
            db.commit()
            result = cursor.fetchall()

            return render_template('itemaddrec1.html', msg=msg, result=result)
            cursor.close()


def getitemnewid():
    itemnewid = str(int(getlastkey('order_item', 'Item_Key')) + 1)
    return (itemnewid)


def getlastkey(tablename, keyname):
    querylastkeysql = 'select ' + keyname + ' from ' + tablename + ' order by ' + keyname + ' desc'
    cursor = db.cursor()
    cursor.execute(querylastkeysql)
    db.commit()
    result = cursor.fetchall()
    for row in result:
        outkeyname = row[0]
#        result.close ()
#        db.close()
        return (str(outkeyname))


def itemsqlfilter(tmp_Item_Key, tmp_Item_Name):
    itemsqlfilter = "1 = 1"
    if tmp_Item_Key != '':
        itemsqlfilter = itemsqlfilter + " and Item_Key like '%" + tmp_Item_Key + "%'"
    if tmp_Item_Name != '':
        itemsqlfilter = itemsqlfilter + " and Item_Name like '%" + tmp_Item_Name + "%'"
    return (itemsqlfilter)



@app.route('/itemupdaterec0')
def itemupdaterec0():    
    return render_template('itemupdaterec0.html',)


@app.route('/itemupdaterec1', methods=['POST', 'GET'])
def itemupdaterec1():
    error = None
    if request.method == 'POST':
        tmp_Item_Key = request.form['Item_Key']
        tmp_Item_Name = request.form['Item_Name']
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Item_Key, Item_Name, Item_Type, Item_Brand FROM order_item where " + itemsqlfilter(tmp_Item_Key,tmp_Item_Name) + " order by Item_Key asc")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return render_template('itemupdaterec1.html', result = result)

@app.route('/itemupdaterec2', methods=['POST', 'GET'])
def itemupdaterec2():
    if request.method == 'POST':
#        tmp_Customer_Key = request.form['Customer_Key']
        tmp_Item_Key = request.form['In_Item_Key']
#        return (tmp_Customer_Key)
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM order_item where Item_Key = '"+tmp_Item_Key+"'")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
#        for row in result:
#            Customer_Key = row[0]
#            Customer_Name = row[1]
#        return (Customer_Name)
        return render_template('itemupdaterec2.html', result = result)
    else:
        return 'End'

@app.route('/itemupdaterec3', methods=['POST', 'GET'])
def itemupdaterec3():
    if request.method == 'POST':
        try:
            tmp_Order_Key = request.form['Order_Key']
            tmp_Item_Key = request.form['Item_Key']
            tmp_Item_Name = request.form['Item_Name']
            tmp_Item_Description = request.form['Item_Description']
            tmp_Item_Type = request.form['Item_Type']
            tmp_Item_Brand = request.form['Item_Brand']
            tmp_Item_Size = request.form['Item_Size']
            tmp_Item_Cost = request.form['Item_Cost']
            tmp_Item_Price = request.form['Item_Price']
            tmp_Item_Quantity = request.form['Item_Quantity']

            cursor = db.cursor()
            tmp_Item_Key = request.form['Item_Key']
            sql = ("update order_item set Order_Key = '"+tmp_Order_Key+"', Item_Key = '"+tmp_Item_Key+"', Item_Name = '"+tmp_Item_Name+"', Item_Description = '"+tmp_Item_Description+"', Item_Type = '"+tmp_Item_Type+"', Item_Brand = '"+tmp_Item_Brand+"', Item_Size = '"+tmp_Item_Size+"', Item_Cost = '"+tmp_Item_Cost+"', Item_Price = '"+tmp_Item_Price+"', Item_Quantity = '"+tmp_Item_Quantity+"' where Item_Key = '"+tmp_Item_Key+"'")
            
            cursor.execute(sql)
            db.commit()
            msg = "Record successfully updated"
        except:
            db.rollback()
            msg = "error in Update operation"

        finally:
            cursor = db.cursor()
            sql = ("SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM order_item where Item_Key = '"+tmp_Item_Key+"'")
            cursor.execute(sql)
            db.commit()
            result = cursor.fetchall()

            return render_template('itemupdaterec3.html', msg = msg, result = result)
            cursor.close()

@app.route("/itemqueryrec0")
def itemqueryrec0():
    return render_template('itemqueryrec0.html')

@app.route('/itemqueryrec1', methods=['POST', 'GET'])
def itemqueryrec1():
    error = None
    if request.method == 'POST':
        tmp_Item_Key = request.form['Item_Key']
        tmp_Item_Name = request.form['Item_Name']
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Item_Key, Item_Name, Item_Type, Item_Brand FROM order_item where " + itemsqlfilter(tmp_Item_Key,tmp_Item_Name) + " order by Item_Key asc")
        cursor.execute(sql)
        db.commit()
#       db.close()
        result = cursor.fetchall()
#        for row in result:
#            Customer_Name = row[0]
#            Customer_Phone_no = row[1]
#        return (Customer_Name)
        return render_template('itemqueryrec1.html', result = result)

@app.route('/itemqueryrec2', methods=['POST', 'GET'])
def itemqueryrec2():
    if request.method == 'POST':
        tmp_Item_Key = request.form['In_Item_Key']
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM order_item where Item_Key = '"+tmp_Item_Key+"'")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
#        for row in result:
#            Customer_Key = row[0]
#            Customer_Name = row[1]
#        return (Customer_Name)
        return render_template('itemqueryrec2.html', result = result)
    else:
        return 'End'

@app.route('/itemdeleterec0')
def itemdeleterec0():    
    return render_template('itemdeleterec0.html',)


@app.route('/itemdeleterec1', methods=['POST', 'GET'])
def itemdeleterec1():
    error = None
    if request.method == 'POST':
        tmp_Item_Key = request.form['Item_Key']
        tmp_Item_Name = request.form['Item_Name']
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Item_Key, Item_Name, Item_Type, Item_Brand FROM order_item where " + itemsqlfilter(tmp_Item_Key,tmp_Item_Name) + " order by Item_Key asc")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return render_template('itemdeleterec1.html', result = result)

@app.route('/itemdeleterec2', methods=['POST', 'GET'])
def itemdeleterec2():
    if request.method == 'POST':
        tmp_Item_Key = request.form['In_Item_Key']
#        return (tmp_Customer_Key)
        cursor = db.cursor()
        sql = ("SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM order_item where Item_Key = '"+tmp_Item_Key+"'")
        cursor.execute(sql)
        db.commit()
        result = cursor.fetchall()
        return render_template('itemdeleterec2.html', result = result)
    else:
        return 'End'

@app.route('/itemdeleterec3', methods=['POST', 'GET'])
def itemdeleterec3():
    if request.method == 'POST':
        try:
            tmp_Order_Key = request.form['Order_Key']
            tmp_Item_Key = request.form['Item_Key']
            tmp_Item_Name = request.form['Item_Name']
            tmp_Item_Description = request.form['Item_Description']
            tmp_Item_Type = request.form['Item_Type']
            tmp_Item_Brand = request.form['Item_Brand']
            tmp_Item_Size = request.form['Item_Size']
            tmp_Item_Cost = request.form['Item_Cost']
            tmp_Item_Price = request.form['Item_Price']
            tmp_Item_Quantity = request.form['Item_Quantity']
            cursor = db.cursor()
            tmp_Item_Key = request.form['Item_Key']
            sql = ("delete from order_item where Item_Key = '"+tmp_Item_Key+"'")
            
            cursor.execute(sql)
            db.commit()
            msg = "Record successfully deleted"
        except:
            db.rollback()
            msg = "error in Delete operation"

        finally:
            sql = ("SELECT Order_Key, Item_Key, Item_Name, Item_Description, Item_Type, Item_Brand, Item_Size, Item_Cost, Item_Price, Item_Quantity FROM order_item where Item_Key = '"+tmp_Item_Key+"'")
            cursor.execute(sql)
            db.commit()
            result = cursor.fetchall()

            return render_template('itemdeleterec3.html', msg = msg, result = result)
            cursor.close()


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=8000)
