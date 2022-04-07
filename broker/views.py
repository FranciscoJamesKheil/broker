from numpy.core.numeric import outer
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import random, user
from werkzeug.wrappers import response
from broker.auth import login
from flask import Blueprint, app, render_template, request, flash, jsonify
from flask_login import login_required, current_user, utils
from werkzeug.utils import redirect, secure_filename
from .models import Note
from .models import User
from .models import Post
from .models import Interest
from .models import Internet
from . import db
import os
import json
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)

# landing page
@views.route('/', methods=['GET', 'POST'])
def index():
    password = "brokerAdmin!888"
    email ="admin@gmail.com"
    user = User.query.filter_by(email=email).first()
    if not user:
        new_user = User(email=email, contact="001", first_name="Broker", last_name="Admin", password=generate_password_hash(
                    password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
    return render_template("index.html", user=current_user, index = True)
# end of landing page


# about page
@views.route('/about', methods=['GET', 'POST'])
def about():
    return render_template("about.html", user=current_user, index = True)
# end about


# services page
@views.route('/services', methods=['GET', 'POST'])
def services():
    return render_template("services.html", user=current_user, index = True)
# end services


# home page
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    reverse_post = list(reversed(Post.query.all()))
    return render_template("home.html", post = reverse_post, wishlist=Interest.query.all(), ohitsme=current_user, owner = User.query.all(), user=current_user, cur_id=current_user.id, fname = current_user.first_name, lname = current_user.last_name)

@views.route('/_asf99admindashboard?hfkVi98Vidhq_asofj1490_0da09fj_@oas0nimda', methods=['GET','POST'])
@login_required
def admin_dashboard():
    countMem = 0
    for x in User.query.all():
        if x.email != 'admin@gmail.com':
            countMem = countMem+1
    return render_template("admin_dashboard.html", membersCount=countMem, user=current_user, fname=current_user.first_name, lname=current_user.last_name, members=User.query.all())


# home search page
@views.route('/home/search_location', methods=['GET', 'POST'])
@login_required
def search_location():
    location = request.form.get('search_brgy')
    for_title = Post.query.filter_by(title=location).first()
    for_content = Post.query.filter_by(content=location).first()

    record=0
    for list in Post.query.all():
        if location.lower() in list.title.lower() or location.lower() in list.content.lower():
            record = record + 1

    return render_template("home_search.html", record=record, find=location, post = Post.query.all(), wishlist=Interest.query.all(), ohitsme=current_user, owner = User.query.all(), user=current_user, cur_id=current_user.id, fname = current_user.first_name, lname = current_user.last_name)

# view rotate
@views.route('/rotate')
@login_required
def rotate():
    return render_template("rotate.html")


@views.route('/property_details/0z0OQv_1v@90a<int:id>07Xsg03awtVBQdetailsid...', methods=['GET', 'POST'])
@login_required
def details(id):
    
    post = Post.query.get_or_404(id)
    return render_template("details.html", post=post, post_it = Post.query.all(), owner= User.query.all(),user=current_user, fname = current_user.first_name, lname = current_user.last_name)
# end home page


# prediction page
@views.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    return render_template("prediction.html", user=current_user, fname=current_user.first_name, lname = current_user.last_name)

## House
@views.route('/house_predict', methods=['GET', 'POST'])
@login_required
def house():
    return render_template("house.html", user=current_user, fname=current_user.first_name, lname = current_user.last_name)

## land
@views.route('/land_predict', methods=['GET', 'POST'])
@login_required
def land():
    return render_template("land.html", user=current_user, fname=current_user.first_name, lname = current_user.last_name)

## Total
@views.route('/total_price', methods=['GET', 'POST'])
@login_required
def total():
    return render_template("total.html", user=current_user, fname=current_user.first_name, lname = current_user.last_name)

# end of prediction 


import urllib.request
from broker import create_app
app = create_app()
# upload page
UPLOAD_FOLDER = "broker/static/uploads/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@views.route('/upload_property', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form.get('title')
        content_post = request.form.get('content')
        price = request.form.get('price')
        date = request.form.get('date')
        property_pic = request.files['pic']
        property_pic1 = request.files['pic1']
        property_pic2 = request.files['pic2']

        if not property_pic and property_pic1 and property_pic2:
            flash('No file uploaded!')
            return redirect('/my_profile')

        filename = secure_filename(property_pic.filename)
        property_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        mimetype = property_pic.mimetype

        filename1 = secure_filename(property_pic1.filename)
        property_pic1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        mimetype1 = property_pic1.mimetype

        filename2 = secure_filename(property_pic2.filename)
        property_pic2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
        mimetype2 = property_pic2.mimetype

        if len(title) < 1:
            flash('Post is too short!', category='error')
        elif property_pic and allowed_file(property_pic.filename):
            new_title = Post(title=title, content=content_post, price = price, date_posted=date, img=property_pic.read(), mimetype=mimetype, name=filename,img1=property_pic1.read(), mimetype1=mimetype1, name1=filename1, img2=property_pic2.read(), mimetype2=mimetype2, name2=filename2,user_id=current_user.id)
            db.session.add(new_title)
            db.session.commit()
            flash('Post added!', category='success')
        else:
            flash("Allowed image types are: png, jpg, jpeg, gif", category='error')
            return redirect('/my_profile')

    return render_template("total.html", user=current_user, fname=current_user.first_name, lname = current_user.last_name)
# end of upload page

# profile page
@views.route('/my_profile', methods=['GET', 'POST'])
@login_required
def profile():
    post_reverse = list(reversed(Post.query.all()))
    return render_template("profile.html", user=current_user, post = post_reverse, fname=current_user.first_name, lname = current_user.last_name, email = current_user.email, contact = current_user.contact)
# end of profile page

# account page
@views.route('/account/000Ov@90a<int:id>07Xsg03awtVBQredirectid...', methods=['GET', 'POST'])
@login_required
def account(id):
    account = User.query.get_or_404(id)
    post_reverse = list(reversed(Post.query.all()))
    return render_template("account.html", account = account, owner=User.query.all(), user=current_user, ohitsme=current_user, post = post_reverse, fname=current_user.first_name, lname = current_user.last_name, email = current_user.email, contact = current_user.contact)
# end of profile page


# add wishlist
@views.route('/add_wishlist/0aBYC=<int:id>connectingUS=<int:id_user>idUVcXqp=<int:id_own>', methods=['GET','POST'])
@login_required
def add_wishlist(id,id_user,id_own):
    my_wish_id_post = id
    who_adds_the_wish = id_user
    interest = Interest.query.filter_by(post_id=my_wish_id_post).first()
    person = Interest.query.filter_by(user_id=who_adds_the_wish).first()
    
    if who_adds_the_wish == id_own:
        flash('You cannot add to wishlist of your own property..', category='error')
        return redirect('/home')
    elif interest and person:
        flash('You have been already added this property..', category='error')
        return redirect('/home')
    else:
        new_wish = Interest(post_id=my_wish_id_post, post_user=id_own, user_id=who_adds_the_wish)
        db.session.add(new_wish)
        db.session.commit()
        flash('Add to wishlist successfully!', category='success')
        return redirect('/home')
    return render_template("home.html", post = Post.query.all(), ohitsme=current_user, owner = User.query.all(), user=current_user, cur_id=current_user.id, fname = current_user.first_name, lname = current_user.last_name)


# wishlist page
@views.route('/my_wishlist', methods=['GET','POST'])
@login_required
def my_wishlist():
    reverse_list = list(reversed(Interest.query.all()))
    return render_template("wishlist.html", wishlist=reverse_list, owner=User.query.all(), post = Post.query.all(), user=current_user, ohitsme=current_user, fname=current_user.first_name, lname = current_user.last_name, email = current_user.email, contact = current_user.contact)
# end of profile page

# remove wishlist
@views.route('/remove_wishlist/<int:id>', methods=['GET','POST'])
@login_required
def remove_wishlist(id):
    list_to_delete = Interest.query.get_or_404(id)

    try:
        db.session.delete(list_to_delete)
        db.session.commit()
        flash("Wishlist remove successfully..", category='success')
        return redirect('/my_wishlist')
    except:
        flash("There was a problem deleting the wishlist...", category='error')
# end of profile page


# update post
@views.route('/update_post/<int:id>', methods=['GET','POST'])
@login_required
def update_post(id):
     post = Post.query.get_or_404(id)
     
     if request.method == "POST":
         post.title = request.form['title']
         post.content = request.form['content']
         post.price = request.form['price']
         post.date_posted = request.form['date']
         property_pic = request.files['pic']
         property_pic1 = request.files['pic1']
         property_pic2 = request.files['pic2']

         filename = secure_filename(property_pic.filename)
         filename1 = secure_filename(property_pic1.filename)
         filename2 = secure_filename(property_pic2.filename)
         property_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         property_pic1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
         property_pic2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
         mimetype = property_pic.mimetype
         mimetype1 = property_pic1.mimetype
         mimetype2 = property_pic2.mimetype

         post.img=property_pic.read()
         post.mimetype=mimetype
         post.name=filename

         post.img=property_pic1.read()
         post.mimetype=mimetype1
         post.name=filename1

         post.img=property_pic2.read()
         post.mimetype=mimetype2
         post.name=filename2
        
         try:
             db.session.commit()
             flash("Post updated successfully..", category='success')
             return redirect("/my_profile", user=current_user, fname=current_user.first_name, lname=current_user.last_name)
         except:
             return redirect("/my_profile")           
     else:
        return render_template("update_post.html", post=post, user=current_user, fname=current_user.first_name, lname=current_user.last_name)



# upload page
PROFILE_FOLDER = "broker/static/profile/"
app.config['PROFILE_FOLDER'] = PROFILE_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Upload profile picture
@views.route('/update_profile/<int:id>', methods=['GET','POST'])
@login_required
def update_profile(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.contact = request.form['contact']
        profile_pic = request.files['profile_img']
        cur_pic = request.form['cur_img']


        if profile_pic and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            mimetype = profile_pic.mimetype
            profile_pic.save(os.path.join(app.config['PROFILE_FOLDER'], filename)) 
            user.img=profile_pic.read()
            user.mimetype=mimetype
            user.name=filename
            db.session.commit()
            flash('Profile and bio updated successfully', category='success')
            return redirect("/my_profile")
        elif not profile_pic:
            if not cur_pic:
                cur_pic = 'userbw.png'
            else:
                user.name=cur_pic
                db.session.commit()
                flash('Update successfully.. to ' + user.first_name + " " + user.last_name, category='success')
            return redirect("/my_profile")
        else:
            flash('Oops, something went wrong in updatinng your data.. Please check the format of the image. Allowed image types are: png, jpg, jpeg, gif', category='error')
            return redirect('/my_profile')

    return render_template("profile.html", user=current_user, fname=current_user.first_name, lname=current_user.last_name)



# delete post
@views.route('/delete_post/<int:id>', methods=['GET','POST'])
@login_required
def delete_post(id):
    post_to_delete = Post.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post delete successfully..", category='success')
        return redirect('/my_profile')
    except:
        flash("There was a problem deleting the post...", category='error')


# settings page
@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    loginrev = list(reversed(Internet.query.all()))
    logcount = Internet.query.all()
    counthist = 0
    for x in logcount:
        if x.user_id == current_user.id:
            counthist=counthist +1
            
    return render_template("settings.html", counthist=counthist, login_record=loginrev, owner=User.query.all(), user=current_user, index=True, fname=current_user.first_name, lname = current_user.last_name)
# end settings page

@views.route('/clear_all_login/<int:id>',methods=['GET','POST'])
@login_required
def clearAll(id):
    for x in Internet.query.all():
        if Internet.query.filter_by(user_id=id).first_or_404():
            db.session.delete(x)
            db.session.commit()
            continue
        else:
            break
    
    flash("Login History cleared!",category='success')
    return redirect('/settings')

@views.route('/set_new_pass_settings',methods=['GET','POST'])
@login_required
def set_pass():
    if request.method == "POST":
        cur_pass = request.form.get('current_password')
        new_pass = request.form.get('new_password')
        id = request.form.get('myID')
        user = User.query.get_or_404(id)
        
        if user.id:
            if check_password_hash(user.password,cur_pass):
                user.password = generate_password_hash(new_pass, method='sha256')
                db.session.commit()
                flash("Password Successfully changed",category='success')
            else:
                flash("Incorrect current password. Please try again..",category='error')
    
    return redirect('/settings')

# support page
@views.route('/support', methods=['GET', 'POST'])
def support():
    return render_template("support.html", user=current_user, index=True, fname=current_user.first_name, lname = current_user.last_name)
# end support


# Implementing model to system

import pickle
import numpy as np

__locations = None
__data_columns = None

modelhouse = pickle.load(open('./broker/model/model.pkl','rb'))
@views.route('/predict_house_price', methods=['GET','POST'])
def predict_house_price(): 
    brgy = request.form['brgy']
    land_area = request.form['land_area']
    floor_area = request.form['floor_area']
    classification = request.form['classification']
    storey = request.form['storey']
    roof_framing = request.form['roof_framing']
    roofing = request.form['roofing']
    ext_walls = request.form['ext_walls']
    flooring = request.form['flooring']
    doors = request.form['doors']
    ceiling = request.form['ceiling']
    windows = request.form['windows']
    wall_finish = request.form['wall_finish']
    elect_conduit = request.form['elect_conduit']
    toilet = request.form['toilet']
    plumbing = request.form['plumbing']

    brgy1 = request.form['brgy1']
    classification1 = request.form['classification1']
    roof_framing1 = request.form['roof_framing1']
    roofing1 = request.form['roofing1']
    ext_walls1 = request.form['ext_walls1']
    flooring1 = request.form['flooring1']
    doors1 = request.form['doors1']
    ceiling1 = request.form['ceiling1']
    windows1 = request.form['windows1']
    wall_finish1 = request.form['wall_finish1']
    elect_conduit1 = request.form['elect_conduit1']
    toilet1 = request.form['toilet1']
    plumbing1 = request.form['plumbing1']

    list_of_others = [brgy,land_area,floor_area,classification,storey,roof_framing,roofing,ext_walls,flooring,
        doors,ceiling,windows,wall_finish,elect_conduit,toilet,plumbing
    ]
    list_of_sub = [brgy1,land_area,floor_area,classification1,storey,roof_framing1,roofing1,ext_walls1,flooring1,
        doors1,ceiling1,windows1,wall_finish1,elect_conduit1,toilet1,plumbing1
    ]
    final_list = []

    others = 0
    push = 0 # push data on the list

    for x in list_of_others:
        if x == 'others':
            final_list.append(list_of_sub[push])
            others = others + 1
        else:
            final_list.append(x)

        push = push + 1

    if others > 0:
        prediction = 0.00
    else:
        # convert final list to text
        brgylist = ['canelar','divisoria','putik','san jose cawa-cawa', 'san jose gusu', 'santa maria', 'tetuan']
        classlist = ['commercial', 'residential']
        framinglist = ['c-purlins','galvanized iron','lumber','open deck','reinforced concrete', 'steel','wooden']
        roofinglist = ['corr. / galvanized iron','concrete','galvanized iron','long span', 'open deck', 'plywood', 'reinforced concrete', 's-tile']
        ext_wallslist = ['adobe type', 'cement plaster','concrete hallow block (chb)', 'painted', 'wood']
        flooringlist = ['concrete','tiles', 'wood']
        doorslist = ['flush', 'glass', 'hcpd/wfpd','panel','plywood','roll up','wood']
        ceilinglist = ['plywood','reinforced concrete','unfinished', 'wood']
        windowslist = ['aluminum casement','french window', 'glass','jalousie','scfw','steel casement','wfpd','wood']
        wallfinishlist = ['adobe','cement plaster','concrete hallow block (chb)','plain cement paint','sand blast','wood']
        electconlist = ['breakers','concealed','conduit pipe','mouldflex','open','painted','pdx electrical wire','polyflex','polyvinyl chloride (pvc)','tube','unplasticized polyvinyl chloride (upvc)']
        toiletlist = ['concrete hallow block','tiles','wood']
        plumbinglist = ['galvanized iron','open','polyvinyl chloride (pvc)']


        brgy = brgylist.index(brgy)
        classification = classlist.index(classification)
        roof_framing = framinglist.index(roof_framing)
        roofing = roofinglist.index(roofing)
        ext_walls = ext_wallslist.index(ext_walls)
        flooring = flooringlist.index(flooring)
        doors = doorslist.index(doors)
        ceiling = ceilinglist.index(ceiling)
        windows = windowslist.index(windows)
        wall_finish = wallfinishlist.index(wall_finish)
        elect_conduit = electconlist.index(elect_conduit)
        toilet =  toiletlist.index(toilet)
        plumbing = plumbinglist.index(plumbing)


        global  __data_columns
        global __locations

        with open("./broker/model/columns.json", "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[0:]

        x = np.zeros(len(__data_columns))
        x[0] = brgy
        x[1] = land_area
        x[2] = floor_area
        x[3] = classification
        x[4] = storey
        x[5] = roof_framing
        x[6] = roofing
        x[7] = ext_walls
        x[8] = flooring
        x[9] = doors
        x[10] = ceiling
        x[11] = windows
        x[12] = wall_finish
        x[13] = elect_conduit
        x[14] = toilet
        x[15] = plumbing
        

        prediction = modelhouse.predict([x])[0]
    

    tablea = final_list[0]
    tableb = final_list[1]
    tablec = final_list[2]
    tabled = final_list[3]
    tablee = final_list[4]
    tablef = final_list[5]
    tableg = final_list[6]
    tableh = final_list[7]
    tablei = final_list[8]
    tablej = final_list[9]
    tablek = final_list[10]
    tablel = final_list[11]
    tablem = final_list[12]
    tablen = final_list[13]
    tableo = final_list[14]
    tablep = final_list[15]

    return render_template("total.html", a=tablea,b=tableb,c=tablec,d=tabled,e=tablee,f=tablef,g=tableg,h=tableh,i=tablei,j=tablej,k=tablek,l=tablel,m=tablem,n=tablen,o=tableo,p=tablep, prediction_alert="{:,.2f}".format(prediction), user=current_user, fname=current_user.first_name, lname=current_user.last_name)


## For land Prediction

__land_locations = None
__land_data_columns = None

model = pickle.load(open('broker/model/model_commercial.pkl','rb'))
@views.route('/predict_land_price', methods=['GET','POST'])
def predict_land_price(): 
    brgy = request.form['brgy']
    classification = request.form['classification']
    land_area = request.form['land_area']

    brgy1 = request.form['brgy1']
    classification1 = request.form['classification1']

    list_of_others = [brgy,land_area,classification]
    list_of_sub = [brgy1,land_area,classification1]
    final_list = []

    others = 0
    push = 0 # push data on the list

    for x in list_of_others:
        if x == 'others':
            final_list.append(list_of_sub[push])
            others = others + 1
        else:
            final_list.append(x)

        push = push + 1

    if others > 0:
        prediction = 0.00
    else:
        # convert final list to text
        brgylist = ['pasonanca','zone 3','zone 1','zone 2','zone 4','santa maria','tetuan','san jose gusu','san roque','tugbungan']
        classlist = ['residential','commercial']


        brgy = brgylist.index(brgy)
        classification = classlist.index(classification)

        global  __land_data_columns
        global __land_locations

        with open("./broker/model/columns_commercial.json", "r") as f:
            __land_data_columns = json.load(f)['data_columns']
            __land_locations = __land_data_columns[0:]

        x = np.zeros(len(__land_data_columns))
        x[0] = brgy
        x[1] = classification
        x[2] = land_area
        

        prediction = model.predict([x])[0]
    

    tablea = final_list[0]
    tableb = final_list[1]
    tablec = final_list[2]

    return render_template("total_land.html", a=tablea,b=tableb,c=tablec, prediction_alert="{:,.2f}".format(prediction), user=current_user, fname=current_user.first_name, lname=current_user.last_name)