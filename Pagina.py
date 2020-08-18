import psycopg2
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secret"
app.PERMANENT_SESSION_LIFETIME = timedelta(days=5)

con = psycopg2.connect(
	host = "ec2-54-144-177-189.compute-1.amazonaws.com",
	database = "d4rdmh19brffne",
	user = "ogynqqdluxstcp",
	password = "ba1b024bc87f692878c686360efc42f1fd87d269c8f6bf0df7021f5895f9a450")

cur = con.cursor()

@app.route('/', methods=["GET","POST"])
def principal():
	if request.method == 'POST':
		busca=request.form['busqueda']
		if busca=='A1B2C3IBRA':
			return redirect(url_for("producto"))
		elif busca=='0101NBZ613':
			return redirect(url_for("productos"))
		elif busca=='000MAN67N1':
			return redirect(url_for("servicios"))
		return redirect(url_for("principal"))
	else:
	    if "user" in session:
	    	return redirect(url_for("user"))
	    return render_template("uno.html")


@app.route('/crear', methods=["GET","POST"])
def crear_cuenta():
	if request.method == 'POST':
		nombre=request.form['nombre']
		apellido=request.form['apellido']
		correo=request.form['correo']
		telefono=request.form['telefono']
		contraseña=request.form['contraseña']
		confirmar=request.form['confirmar']
		contador=0
		contador2=0
		for n in contraseña:
			contador=contador+1
			if n==" ":
				contador=-20

		for n in correo:
			if n=="@" or n==".":
				contador2=contador2+1
			elif n==" ":
				contador2=contador2-1

		if contraseña != confirmar:
			flash("Las contraseñas no coinciden, vuelva a intentarlo")

		elif contador < 8:
			flash("La contraseña no es de 8 caracteres, vuelva a intentarlo")

		elif contador2 < 2:
			flash("Correo invalido, vuelva a intentarlo y escriba sin espacios")

		else:
			correo2 = hashlib.md5(correo.encode())
			telefono2 = hashlib.md5(telefono.encode())
			contraseña2 = hashlib.md5(contraseña.encode())

			correo3 = correo2.hexdigest()
			telefono3 = telefono2.hexdigest()
			contraseña3 = contraseña2.hexdigest()

			cur.execute("insert into clientes (nombre, apellidos, correo, telefono, contraseña) values (%s,%s,%s,%s,%s)" ,(nombre, apellido, correo3, telefono3, contraseña3))
			con.commit()
			session['user'] = nombre + ' ' + apellido
			return redirect(url_for("user"))

		return redirect(url_for("crear_cuenta"))
	else: 
		if "user" in session:
			return redirect(url_for(("user")))
		return render_template("Crear Cuenta.html")


@app.route('/sesion', methods=["GET","POST"])
def buscar_cuenta():
	if request.method == 'POST':
		usuario=request.form['usuario']
		contraseña=request.form['contraseña']

		usuario2 = hashlib.md5(usuario.encode())
		contraseña2 = hashlib.md5(contraseña.encode())

		usuario3 = usuario2.hexdigest()
		contraseña3 = contraseña2.hexdigest()

		cur.execute("select * from clientes where correo = %s and contraseña = %s", (usuario3, contraseña3))
		rows = cur.fetchall()
		for r in rows:
			if r[2]==usuario3 and r[4]==contraseña3:	
				session.permanent = True
				session['user'] = r[0] + ' ' + r[1]
				return redirect(url_for("user"))
		flash("Correo o contraseña incorrecto, vuelve a intentarlo")
		return redirect(url_for("buscar_cuenta"))
	else:	
		if "user" in session:
			return redirect(url_for("user"))
		return render_template("Sesion.html")

@app.route('/productos')
def productos():
	if "user" in session:
		user = session["user"]
		return render_template("Productos2.html", usuario=user)
	return render_template("Productos.html")

@app.route('/user', methods=["GET","POST"])
def user():
	if request.method == 'POST':
		busca=request.form['busqueda']
		if busca=='A1B2C3IBRA':
			return redirect(url_for("productos2o2"))
		elif busca=='0101NBZ613':
			return redirect(url_for("productos2"))
		elif busca=='000MAN67N1':
			return redirect(url_for("servicios2"))
		return redirect(url_for("principal"))
	else:
		if "user" in session:
			user = session["user"]
			return render_template("Usuario.html", usuario=user)
		return redirect(url_for("buscar_cuenta"))

@app.route('/cerrar')
def cerrar():
	session.pop("user", None)
	return redirect(url_for("principal"))

@app.route('/usuario')
def usuario():
	if "user" in session:
		user = session["user"]
		cur.execute("select * from clientes where nombre ||' '|| apellidos = '{0}'".format(user))
		rows = cur.fetchall()
		for r in rows:
			nombre = r[0]
			apellidos = r[1]
		return render_template("info.html", usuario=user, nombre=nombre, apellidos=apellidos)
	return redirect(url_for("buscar_cuenta"))

@app.route('/producto')
def producto():
	if "user" in session:
		user = session["user"]
		return render_template("Producto2.html", usuario=user)
	return render_template("Producto.html")


@app.route('/p1')
def p1():
	if "user" in session:
		user = session["user"]
		return render_template("P1-2.html", usuario=user)
	return render_template("P1.html")

@app.route('/p2')
def p2():
	if "user" in session:
		user = session["user"]
		return render_template("P2-2.html", usuario=user)
	return render_template("P2.html")

@app.route('/p3')
def p3():
	if "user" in session:
		user = session["user"]
		return render_template("P3-2.html", usuario=user)
	return render_template("P3.html")

@app.route('/p4')
def p4():
	if "user" in session:
		user = session["user"]
		return render_template("P4-2.html", usuario=user)
	return render_template("P4.html")

@app.route('/p5')
def p5():
	if "user" in session:
		user = session["user"]
		return render_template("P5-2.html", usuario=user)
	return render_template("P5.html")

@app.route('/p6')
def p6():
	if "user" in session:
		user = session["user"]
		return render_template("P6-2.html", usuario=user)
	return render_template("P6.html")

@app.route('/p7')
def p7():
	if "user" in session:
		user = session["user"]
		return render_template("P7-2.html", usuario=user)
	return render_template("P7.html")

@app.route('/p8')
def p8():
	if "user" in session:
		user = session["user"]
		return render_template("P8-2.html", usuario=user)
	return render_template("P8.html")

@app.route('/p9')
def p9():
	if "user" in session:
		user = session["user"]
		return render_template("P9-2.html", usuario=user)
	return render_template("P9.html")

@app.route('/p10')
def p10():
	if "user" in session:
		user = session["user"]
		return render_template("P10-2.html", usuario=user)
	return render_template("P10.html")

@app.route('/p11')
def p11():
	if "user" in session:
		user = session["user"]
		return render_template("P11-2.html", usuario=user)
	return render_template("P11.html")

@app.route('/servicios')
def servicios():
	if "user" in session:
		user = session["user"]
		return redirect(url_for("servicios2"))
	return render_template("Servicios.html")

@app.route('/servicios2')
def servicios2():
	if "user" in session:
		user = session["user"]
		return render_template("Servicios2.html", usuario=user)
	return redirect(url_for("servicios"))

@app.route('/m1')
def m1():
	if "user" in session:
		user = session["user"]
		return render_template("m1-2.html", usuario=user)
	return render_template("m1.html")

@app.route('/m2')
def m2():
	if "user" in session:
		user = session["user"]
		return render_template("m2-2.html", usuario=user)
	return render_template("m2.html")

@app.route('/m3')
def m3():
	if "user" in session:
		user = session["user"]
		return render_template("m3-2.html", usuario=user)
	return render_template("m3.html")

@app.route('/m4')
def m4():
	if "user" in session:
		user = session["user"]
		return render_template("m4-2.html", usuario=user)
	return render_template("m4.html")

@app.route('/m5')
def m5():
	if "user" in session:
		user = session["user"]
		return render_template("m5-2.html", usuario=user)
	return render_template("m5.html")

@app.route('/m6')
def m6():
	if "user" in session:
		user = session["user"]
		return render_template("m6-2.html", usuario=user)
	return render_template("m6.html")

if __name__ == '__main__':
	app.run(port = 2000, debug = True)


#cur.execute("delete from infor where nombre = '%s'", (nom))
#print("Datos Eliminados")

#for r in rows:
#	print (f"Nombre: {r[0]} Apellido: {r[1]} Correo: {r[2]} Telefono: {r[3]} Contraseña: {r[4]}")


con.commit()

cur.close()

con.close()