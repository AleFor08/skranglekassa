from functions import *

app = Flask(
    __name__,
    template_folder='../SRC/HTML/',
    static_folder='../SRC/'
)

CORS(app)

print(app)
print(app.template_folder)

if __name__ == "__main__":
    app.run(debug=True)

# Eskil code
@app.route("/chat", methods=["POST"])
def chat():

	# check if ai is available
	if not noai:
		data = request.json
		userInput = data.get("userInput", "") # Get user input from request

		# Validate user input
		if not userInput:
			return jsonify({"error": "No input provided"}), 400 
		AIOutput = ai.get_ai_response(userInput, database) # Get AI response using the function from ai_logic.py
		return jsonify({"aiOutput": AIOutput})# Return AI response as JSON
	else:
		return jsonify({"aiOutput": "Beklager! Ai fungerer foreløpig ikke grunnet serverfeil."}), 503 # Service Unavailable error
# End of Eskil code

@app.route("/contact")
def contactPage():
	print("Contact page")
	return render_template("contact.html")


@app.route("/login")
def loginPage():
	print("Login page")
	return render_template("login.html")


@app.route("/signup")
def signupPage():
	print("Signup page")
	return render_template("signup.html")


@app.route("/allproducts")
def allProductsPage():
	print("All products")

	_, c = connect() #	connect to sql database

#	
	c.execute("""
		SELECT * FROM oppforinger
		ORDER BY sist_endret;
	""")

#	add c.fetchall() ++ code here	

	return render_template("allproducts.html")


@app.route("/newproduct")
def newProductPage():
	print("New product page")
	return render_template("newproduct.html")


@app.route("/product")
def productPage():
	 
	print("Product page")

	return render_template("product.html")


@app.route("/productimage")
def productImage():
	 
	print("Image page")

	return render_template("productimage.html")

@app.route("/user")
def userPage():
	 
	print("user page")
#	if  == True:
#		return render_template("user.html")
#	else: 
#		return jsonify({"message": "Login to view page"}), 401


@app.route("/logout")
def logoutPage():
	 
	

	return render_template("logout.html")


@app.route("/signup", methods=["POST"])
def signup():
	 
	print("signup")
	try:
		data = retrieve()
		print("retrieved")
	except Exception as err:
		print("Retrieve error:", err)
		return jsonify({"message": "could not recieve data"}), 449 # Retry With (bad user input)

	firstname = data.get("fname")
	lastname = data.get("lname")
	bdate = data.get("birthdate")
	email = data.get("email")
	bdate = data.get("birthdate")
	hashed = encrypt(data.get("cpassword"))

	try:
		db, c = connect()
		print("connected")

		c.execute("INSERT INTO brukere (fornavn, etternavn, epost, passord, fodselsdato) VALUES (%s, %s, %s, %s, %s)", (firstname, lastname, email, hashed, bdate))
		print("Executed insertion")

		db.commit()
		print("Committed")

		return jsonify({"message": "User created successfully"}), 201 # Created
	
	except mysql.IntegrityError as err:
		print("Database error:", err)
		return jsonify({"message": "User with some similar credentials already exists"}), 409
	
	except mysql.connector.Error as err:
		print("Database error:", err)
		return jsonify({"message": "Database error"}), 400 
	
	except Exception as err:
		print("Other error:", err)
		return jsonify({"message": "Unexpected error"}), 500 # Internal Server Error
	
	finally:
		c.close()
		db.close()


@app.route("/login", methods=["POST"])
def login():
	 
	print("login")
	try:
		data = retrieve()
	except Exception as err:
		print("Retrieve error:", err)
		return jsonify({"message": "could not receive data"}), 449 # Retry With (bad user input)
	
	email = str(data.get("email"))
	password = data.get("password")

	print(email, password)

	try:
		_, c = connect()

	except mysql.connector.Error as err:
		print("Database error:", err)
		return jsonify({"message": "Database connection error"})
	except Exception as err:
		print("Other error:", err)
		return jsonify({"message": "Unexpected database error"}), 500 # Internal Server Error
	
#	try:
#		query = "SELECT passord FROM brukere WHERE epost = %s;"
#		c.execute(query, (email,))
#		row = c.fetchone()

#		if bcrypt.checkpw(password.encode("utf-8"), row[0]):
#			loggedIn = True
#			print("logged in!")
#			return jsonify({"message": "Login successful"}), 200
#		else:
#			 = False
#			print("Not logged in..")
#			return jsonify({"message": "Login failed"}), 401
#		
#	except TypeError as err:
#		print(err)
#		return jsonify({"message": "Database error"}), 422
#	
#	except Exception as err:
#		print(err)
#		return jsonify({"message": "Database error"}), 500


@app.route("/")
def home():
	 
		print(app.url_map, )
#	if  == False:
		return render_template(
			"index.html", 
			contactPage_url=url_for("contactPage"),
			signupPage_url=url_for("signupPage"),
			loginPage_url=url_for("loginPage"),
			allProductsPage_url=url_for("allProductsPage"),
			newProductPage_url=url_for("newProductPage"),
			image_url=url_for("productImage"),
			productPage_url=url_for("productPage"),
			userPage_url=url_for("userPage"),
			logoutPage_url=url_for("logoutPage")
			)
#	
#	elif  == True:
#		return render_template("home.html")
#	else:
#		print("How are you here?")
#		return jsonify({"message": "How are you here?"}), 418 # I'm a teapot
