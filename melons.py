from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer (product page)."""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """Shopping cart page: displays the contents of the shopping cart with a list of melons, quantities, prices, and total prices held in this session."""
   
    list_of_melons = session.get('ourcart', [])
       
    # for melon_id in list_of_melons: 
    #     melon = model.get_melon_by_id(melon_id)
    #     melon_name_list.append(melon.common_name)
    #     melon_price_list.append(melon.price) 
    melon_qty = {}
    for melon_id in list_of_melons:
        if melon_qty.get(melon_id):
            melon_qty[melon_id] += 1
        else:
            melon_qty[melon_id] = 1
    print melon_qty

    melon_objects = {}
    for melon_id, qty in melon_qty.items():
        melon_obj = model.get_melon_by_id(melon_id)
        melon_objects[melon_obj] = qty

    cart_total = 0;
    for melon, qty in melon_objects.items(): 
        cart_total += melon.price * qty


    print melon_objects

    return render_template("cart.html",
            melons = melon_objects,
            total = cart_total)
    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """When a melon is added to a cart, redirect to the
    shopping cart page, and display the message
    "Successfully added to cart"""
   
    if 'ourcart' in session:
        session['ourcart'].append(id)
    else:
        session['ourcart'] = [id]    

    print session
    flash("Successfully added to cart")
    return redirect(url_for("shopping_cart"))    # function name
 
@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")

@app.route("/logout", methods=["GET"])
def show_logout():
    """When user/customer clicks on 'log out', the session (in this case the shopping cart contents), will be refreshed/deleted. Then, redirected to the main melons product page."""
    del session["givenname"]
    del session['ourcart']
    return redirect("/melons")

@app.route("/login", methods=["POST"])
def process_login():
    """See if email associated with the log in is in the Customer DB, then store them in a session."""
    
    if request.method == "POST": 
        input_email = request.form['email']
        print "input email is %r" % input_email

        customer = model.get_customer_by_email(input_email)
   
        if customer is not None:
            session["givenname"] = customer.givenname
        else:
            flash("Error, customer doesn't exist")
            return redirect(url_for("show_login"))
            
        print "********************************************"
        print session 

    return redirect(url_for("list_melons"))

@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True)
