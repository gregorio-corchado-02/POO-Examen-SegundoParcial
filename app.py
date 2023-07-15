from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


#Inicialiazacion del servidor flask
app= Flask(__name__)

#Configuracion para base de datos
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="db_floreria"
app.secret_key='mysecretkey'

mysql= MySQL(app)

@app.route('/')
def index():
    curSelect= mysql.connection.cursor()
    curSelect.execute('select * from tbflores')
    consulta= curSelect.fetchall()
    return render_template('index.html',listAlbums=consulta)

@app.route('/guardar',methods=['POST'])
def guardar():
    if request.method == 'POST':
        nombre= request.form['txtNombre']
        cantidad= request.form['txtCantidad']
        precio= request.form['txtPrecio']
        CS = mysql.connection.cursor()
        CS.execute('insert into tbflores(Nombre,Cantidad,Precio) values(%s,%s,%s)',(nombre,cantidad,precio))
        mysql.connection.commit()
        

    flash('Album Agregado Correctamente bro')
    return redirect(url_for('index'))


@app.route('/eliminar/<id>')
def eliminar(id):
    cursoeditar = mysql.connection.cursor()
    cursoeditar.execute('select * from tbflores where ID=%s', (id, ))
    consulId = cursoeditar.fetchone()
    return render_template('EliminarAlbum.html', album = consulId)



@app.route('/eliminar/<id>',methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        curactualizar = mysql.connection.cursor()
        curactualizar.execute('delete from tbflores where ID=%s', (id, ))
        mysql.connection.commit()

    flash('Album Eliminado Correctamente bro')
    return redirect(url_for('index'))
   
if __name__== '__main__':
    app.run(port= 5000, debug=True)