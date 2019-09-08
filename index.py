from flask import Flask,render_template,redirect,url_for,request,session
import pymysql
import time
import datetime
import os
from datetime import date
import pandas as pd
from pyramid.arima import auto_arima
from datetime import datetime
db = pymysql.connect(host='localhost',user='root',password='',db='sales_prediction')
cursor = db.cursor()
import numpy as np

# now = datetime.now().strftime('%c')
# print(now)
# exit()
time1 = int(round(time.time()*1000))

abs_path = os.getcwd()
app = Flask(__name__)
app.secret_key = "Enter a Random Secert key"
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/SignUp')
def signup():
    return render_template('signup.html')

@app.route('/SignUp/Submited/',methods=["POST","GET"])
def signup_submited():
        time1 = int(round(time.time() * 1000))
        reg_id = "Admin" + str(time1)
        now = datetime.now().strftime('%c')
        reg_id1 = "User" + str(time1)
        if request.method == "POST":
            uname = request.form['uname']
            emailid = request.form['emailid']
            password1 = request.form['password1']
            phnumber = request.form['phnumber']
            date = request.form['date']
            address = request.form['address']
            city = request.form['city']
            selected = request.form['selected']
            sql = "select email,phone_number from reg where (email='%s' or phone_number ='%s') and user_type='%s'"%(emailid,phnumber,selected)
            cursor.execute(sql)
            signup_results = cursor.fetchall()
            if(len(signup_results)>0):
                if(signup_results[0][0]==emailid):
                    print("entered emailid is already exits")
                    return render_template('signup.html',msg="emailid_exits")
                elif(signup_results[0][0]==phnumber):
                    print("entered phone number is already exits")
                    return render_template('signup.html', msg="phonenumber_exits")
            else:
                if(selected == "admin"):
                    sql = "insert into reg(reg_id,username,email,password,phone_number,dob,address,city,user_type,reg_timedate) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                            %(reg_id,uname,emailid,password1,phnumber,date,address,city,selected,now)
                    cursor.execute(sql)
                    db.commit()
                    return render_template('signup.html',msg="successfully_registered")
                if(selected == "user"):
                    sql = "insert into reg(reg_id,username,email,password,phone_number,dob,address,city,user_type,reg_timedate) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                            % (reg_id1,uname, emailid, password1, phnumber, date, address, city, selected,now)
                    cursor.execute(sql)
                    db.commit()
                    return render_template('signup.html', msg="successfully_registered")
        return render_template('signup.html')

@app.route('/Login')
def signin():
    return render_template('signin.html')

@app.route('/Login/Submited/',methods=["POST","GET"])
def login_submitted():
    if request.method == "POST":
        emailid = request.form['emailid']
        password1 = request.form['password1']
        selected = request.form['selected']
        sql = "select password from reg where email = '%s' and user_type = '%s'"%(emailid,selected)
        cursor.execute(sql)
        login_results = cursor.fetchall()
        print(login_results,emailid,selected)
        if(len(login_results)>0):
            if(selected == "admin"):
                if(login_results[0][0] == password1):
                    session['admin_email'] = emailid
                    return redirect(url_for('admin_homepage'))
                else:
                    return render_template('signin.html',msg="invalid_password")
            if (selected == "user"):
                if (login_results[0][0] == password1):
                    session['user_email'] = emailid
                    return redirect(url_for('user_homepage'))
                else:
                    return render_template('signin.html',msg="invalid_password")
        else:
            return render_template('signin.html',msg="invalid_emailid")
        return render_template('signin.html')
    return render_template('signin.html')

@app.route('/Upload_Stock')
def upload_stock():
    return render_template('upload_stock.html')

@app.route('/Upload_Stock/Stock_Submitted/',methods=["POST","GET"])
def stock_submitted():
    # print("entered")
    time2 = int(round(time.time() * 1000))
    product_id = "PD" + str(time2)
    now = datetime.now().strftime('%c')
    if request.method == "POST":
        # print("entered1")
        producttype = request.form['producttype']
        productname = request.form['productname']
        quantityadd = int(request.form['quantityadd'])
        price = request.form['price']
        discount = int(request.form['discount'])
        imagefile = request.files['imagefile']
        # print(imagefile)
        selected = request.form['selected']
        # print(stockid,producttype,productname,quantityadd,price,discount,imagefile,selected)
        target = os.path.join(abs_path, 'static/images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        filename = str(time2) + imagefile.filename
        adding_file = ''.join([target, filename])
        imagefile.save(adding_file)
        sql = "insert into stock(stock_id,product_type,product_name,quantity,price,discount,image_name,selected,added_date) " \
              "values('%s','%s','%s','%d','%s','%d','%s','%s','%s')"%(product_id,producttype,productname,quantityadd,price,discount,filename,selected,now)
        cursor.execute(sql)
        db.commit()
        return render_template('upload_stock.html',msg="uplaoded_successfully")
    return render_template('upload_stock.html')

@app.route('/Admin-homepage')
def admin_homepage():
    return render_template('admin.html')

@app.route('/Admin-homepage/View_stock')
def view_stock():
    sql = "select image_name,product_type,price,discount,quantity from stock"
    cursor.execute(sql)
    view_stock_results = cursor.fetchall()
    return render_template('View_stock.html',results =view_stock_results,msg="view_stock")

@app.route('/Admin-homepage/View_stock/Updated/<id>/',methods=["POST","GET"])
def view_stock_upadted(id):
    if request.method == "POST":
        sql = "select * from stock where image_name = '%s'"%(id)
        cursor.execute(sql)
        Stock_update_results = cursor.fetchall()
        return render_template('View_stock.html',msg="stock_update",results = Stock_update_results)
    return render_template('View_stock.html')

@app.route('/Admin-homepage/View_Stock/Stock_upadted/<id>/<quan>/',methods=["POST","GET"])
def stock_upadted(id,quan):
    if request.method == "POST":
        quantityadd = int(request.form['quantityadd'])
        price = (request.form['price'])
        discount = int(request.form['discount'])
        quantity = quantityadd+int(quan)
        now = datetime.now().strftime('%c')
        sql = "update stock set quantity ='%d',price = '%s',discount='%d',updated_stock = '%s'where stock_id = '%s'"%(quantity,price,discount,now,id)
        cursor.execute(sql)
        db.commit()
        sql1 = "select image_name,product_type,price,discount,quantity from stock"
        cursor.execute(sql1)
        view_stock_results = cursor.fetchall()
        return render_template('View_stock.html',msg1="updated_successfully",msg="view_stock",results =view_stock_results)
    return render_template('View_stock.html')

@app.route('/User-homepage')
def user_homepage():
    sql = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('mens_clothes')
    cursor.execute(sql)
    mens_colthes_results = cursor.fetchall()
    # print(mens_colthes_results,len(mens_colthes_results))
    sql1 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('mens_accessories')
    cursor.execute(sql1)
    mens_accessories_results = cursor.fetchall()
    sql2 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('womens_clothes')
    cursor.execute(sql2)
    womens_colthes_results = cursor.fetchall()
    sql3 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('womens_accessories')
    cursor.execute(sql3)
    womens_accessories_results = cursor.fetchall()
    sql4 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('electronics_goods')
    cursor.execute(sql4)
    electronics_goods_results = cursor.fetchall()
    sql5 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('books')
    cursor.execute(sql5)
    books_results = cursor.fetchall()
    return render_template('user.html',mc_results=mens_colthes_results,ma_results=mens_accessories_results,wc_results=womens_colthes_results,wa_results=womens_accessories_results,eg_results=electronics_goods_results,b_results=books_results)

@app.route('/User-homepage/Like/products_counts/<id>',methods=["POST","GET"])
def like_products(id):
    email1 = ''
    if 'user_email' in session:
        email1 = session['user_email']
    now = datetime.now().strftime('%c')
    sql6 = "select stock_id,product_type from stock where image_name ='%s'"%(id)
    cursor.execute(sql6)
    like_products_results = cursor.fetchall()
    count1 =1
    sql7 = "insert into like_count(stockid,product_type,like_count,useremail,date_time) values('%s','%s','%d','%s','%s')"%(like_products_results[0][0],like_products_results[0][1],count1,email1,now)
    cursor.execute(sql7)
    db.commit()
    sql8 = "select stockid,product_count from overall_count where stockid = '%s'"%(like_products_results[0][0])
    cursor.execute(sql8)
    product_count_results = cursor.fetchall()
    if(len(product_count_results)>0):
        product_count = int(product_count_results[0][1]) +1
        sql = "update overall_count set product_count ='%d' where stockid ='%s'"%(product_count,product_count_results[0][0])
        cursor.execute(sql)
        db.commit()
    else:
        product_count = 1
        sql = "insert into overall_count (stockid,product_count) values('%s','%d')" % (
        like_products_results[0][0], product_count)
        cursor.execute(sql)
        db.commit()
    sql = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('mens_clothes')
    cursor.execute(sql)
    mens_colthes_results = cursor.fetchall()
    # print(mens_colthes_results,len(mens_colthes_results))
    sql1 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('mens_accessories')
    cursor.execute(sql1)
    mens_accessories_results = cursor.fetchall()
    sql2 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('womens_clothes')
    cursor.execute(sql2)
    womens_colthes_results = cursor.fetchall()
    sql3 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('womens_accessories')
    cursor.execute(sql3)
    womens_accessories_results = cursor.fetchall()
    sql4 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('electronics_goods')
    cursor.execute(sql4)
    electronics_goods_results = cursor.fetchall()
    sql5 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('books')
    cursor.execute(sql5)
    books_results = cursor.fetchall()
    return render_template('user.html',mc_results=mens_colthes_results,ma_results=mens_accessories_results,wc_results=womens_colthes_results,wa_results=womens_accessories_results,eg_results=electronics_goods_results,b_results=books_results)

@app.route('/User-homepage/Buy_Now/<id>')
def user_orderedproduct(id):
    sql = "select * from stock where image_name = '%s'" % (id)
    cursor.execute(sql)
    Stock_update_results = cursor.fetchall()
    return render_template('ordered_product.html',results=Stock_update_results)

@app.route('/User-homepage/product_ordered/<id>',methods=["POST","GET"])
def ordered_product(id):
    email1 = ''
    if 'user_email' in session:
        email1 = session['user_email']
    if request.method == "POST":
        producttype = request.form['producttype']
        price = request.form['price']
        discount = request.form['discount']
        totalprice = request.form['totalprice']
        quantityadd = request.form['quantityadd']
        now = datetime.now().strftime('%c')
        selected = request.form['selected']
        sql = "select stock_id,quantity from stock where image_name = '%s'"%(id)
        cursor.execute(sql)
        ordered_results = cursor.fetchall()
        if(int(ordered_results[0][1])>int(quantityadd)):
            sql1 = "insert into ordered_products(useremail,stockid,product_type,price,discount,total_price,quantity,date_time,selected) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                  %(email1,ordered_results[0][0],producttype,price,discount,totalprice,quantityadd,now,selected)
            cursor.execute(sql1)
            db.commit()
            sql3 = "select quantity from overall_ordered_products where stockid ='%s'"%(ordered_results[0][0])
            cursor.execute(sql3)
            overall_ordered_products_results = cursor.fetchall()
            if(len(overall_ordered_products_results)>0):
                quantityadd1 = (int(quantityadd)+int(overall_ordered_products_results[0][0]))
                overall_quantity=str(quantityadd1)
                sql6 = "update overall_ordered_products set quantity ='%s' where stockid = '%s'"%(overall_quantity,ordered_results[0][0])
                cursor.execute(sql6)
                db.commit()
            else:
                sql2 = "insert into overall_ordered_products(stockid,quantity) values('%s','%s')"%(ordered_results[0][0],quantityadd)
                cursor.execute(sql2)
                db.commit()
            a = int(ordered_results[0][1])
            new_quantity = a-int(quantityadd)
            sql2 = "update stock set quantity = '%d' where image_name = '%s'"%(new_quantity,id)
            cursor.execute(sql2)
            db.commit()
        else:
            sql = "select * from stock where image_name = '%s'" % (id)
            cursor.execute(sql)
            Stock_update_results = cursor.fetchall()
            quantity = ordered_results[0][1]
            return render_template('ordered_product.html',results=Stock_update_results,msg="out_of_stock",quantity=quantity)
        sql = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('mens_clothes')
        cursor.execute(sql)
        mens_colthes_results = cursor.fetchall()
        # print(mens_colthes_results,len(mens_colthes_results))
        sql1 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('mens_accessories')
        cursor.execute(sql1)
        mens_accessories_results = cursor.fetchall()
        sql2 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('womens_clothes')
        cursor.execute(sql2)
        womens_colthes_results = cursor.fetchall()
        sql3 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('womens_accessories')
        cursor.execute(sql3)
        womens_accessories_results = cursor.fetchall()
        sql4 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('electronics_goods')
        cursor.execute(sql4)
        electronics_goods_results = cursor.fetchall()
        sql5 = "select product_type,price,discount,image_name from stock where selected = '%s'" % ('books')
        cursor.execute(sql5)
        books_results = cursor.fetchall()
        return render_template('user.html',mc_results=mens_colthes_results,ma_results=mens_accessories_results,wc_results=womens_colthes_results,wa_results=womens_accessories_results,eg_results=electronics_goods_results,b_results=books_results)
    return render_template('user.html')

@app.route('/Prediction')
def prediction():
    return render_template('prediction.html',msg="prediction_form")

@app.route('/Prediction/submitted',methods=["POST","GET"])
def prediction_submitted():
    if request.method == "POST":
        selected_type = request.form['selected_type']
        selected_month = int(request.form['selected_month'])
        # print(selected_month,selected_type)
        def prediction(field, num_of_month_to_predict):
            model = auto_arima(field, start_p=1, start_q=1,
                               max_p=3, max_q=3, m=12,
                               start_P=0, seasonal=True,
                               d=1, D=1, trace=True,
                               error_action='ignore',
                               suppress_warnings=True,
                               stepwise=True)
            result = model.fit(field)
            pred_value = result.predict(num_of_month_to_predict)
            return pred_value

        data = pd.read_csv('sales.csv')
        field = data[selected_type]
        total_predicted = prediction(field, 12)
        predicted_month=round(total_predicted[selected_month-1])
        labels = ['Jan','Feb','Mar','April','May','June','July','August','Sep','Oct','Nov','Dec']
        values = total_predicted

        return render_template('prediction.html',msg="prediction_form",msg1="submitted",result1 = predicted_month,product_type=selected_type,msg2 = "predicted_bar",set=zip(labels,values),month=selected_month)
    return render_template('prediction.html',msg="prediction_form")

@app.route('/My ordered Products/')
def ordered_products():
    email1 = ''
    if 'user_email' in session:
        email1 = session['user_email']
        sql = "select * from ordered_products where useremail ='%s'"%(email1)
        cursor.execute(sql)
        ordered_products_results = cursor.fetchall()
        return render_template('view_user_ordered_products.html',results = ordered_products_results)
    return render_template('view_user_ordered_products.html')

@app.route('/Logout')
def logout():
    return redirect(url_for('index'))

app.run()

