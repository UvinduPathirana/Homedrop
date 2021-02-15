from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import render_template
from flask_mysqldb import MySQL
from markupsafe import escape


application = Flask(__name__,  static_url_path='',
                    static_folder='static', template_folder='templates')
 
# local
# application.config['MYSQL_HOST'] = 'localhost'
# application.config['MYSQL_USER'] = 'root'
# application.config['MYSQL_PASSWORD'] = 'Uv1ndu2006'
# application.config['MYSQL_DB'] = 'home_delivary'

# production
application.config['MYSQL_HOST'] = 'database-1.c5qdsuoy5mft.ap-south-1.rds.amazonaws.com'
application.config['MYSQL_USER'] = 'admin'
application.config['MYSQL_PASSWORD'] = ''
application.config['MYSQL_DB'] = 'home_delivary'


mysql = MySQL(application)


@application.route('/', methods=['GET', 'POST'])
def hello_world():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * from vendors join vendorimage on (vendors.id = vendorimage.vendorid)")
    vendor = cur.fetchall()
    cur.connection.commit()
    cur.close()
    return render_template('index.html', vendorlocations=locations, vendorcategories=categories, vendor=vendor)


@application.route('/flyer/<id>',  methods=['GET', 'POST'])
def flyer(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM vendors join vendorimage on ( vendors.id = vendorimage.vendorid) where vendors.id = " + id)
    vendors = cur.fetchall()
    cur.execute(
        "SELECT * FROM home_delivary.vendorphonenumbers where vendorphonenumbers.vendorid = " + id)
    vendorphonenumbers = cur.fetchall()
    cur.connection.commit()
    cur.close()
    return render_template('flyer.html', vendorlocations=locations, vendorcategories=categories, vendors=vendors, vendorphonenumebrs=vendorphonenumbers)


@application.route('/categories/<id>',  methods=['GET', 'POST'])
def category(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * from vendors join vendorimage on (vendors.id = vendorimage.vendorid) WHERE vendors.category = " + id)
    vendor = cur.fetchall()
    cur.connection.commit()
    cur.close()
    return render_template('index.html', vendorlocations=locations, vendorcategories=categories, vendor=vendor)


@application.route('/locations/<id>',  methods=['GET', 'POST'])
def location(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * from vendors join vendorimage on (vendors.id = vendorimage.vendorid) left join vendorlocations on (vendors.id = vendorlocations.vendorid) WHERE vendorlocations.locationid = " + id)
    vendor = cur.fetchall()
    cur.connection.commit()
    cur.close()
    return render_template('index.html', vendorlocations=locations, vendorcategories=categories, vendor=vendor)


@application.route('/categories/<categoryid>/locations/<locationid>',  methods=['GET', 'POST'])
def categoriesl(categoryid, locationid):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM locations")
    locations = cur.fetchall()
    cur.execute("SELECT * FROM categories")
    categories = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * from vendors join vendorimage on (vendors.id = vendorimage.vendorid) left join vendorlocations on (vendors.id = vendorlocations.vendorid) where vendors.category = " + categoryid + " and vendorlocations.locationid = " + locationid)
    locations = cur.fetchall()
    cur.connection.commit()
    cur.close()
    return render_template('locations.html', vendorlocations=locations, vendorcategories=categories, locations=locations)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
