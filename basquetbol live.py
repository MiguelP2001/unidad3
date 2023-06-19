from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


# ?  CONEXION A LA BASE DE DATOS

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="valudbd"
    )
except mysql.connector.Error as e:
    messagebox.showerror("Error de conexión",
                         f"No se pudo conectar a la base de datos: {e}")
    exit()


# ?  LEER USUARIOS DE LA BD


def leer_usuarioDB():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


#!         VEMTANA DE LOGIN

ventana = tk.Tk()
ventana.title("BASQUET LIVE")
ventana.geometry("280x450+300+250")

color = '#c5e2f6'
ventana['bg'] = color


# *   DEFINIR LAS VAR DE LIMITE

logusuario_limit = StringVar()
logcontra_limit = StringVar()

regnombre_limit = StringVar()
regapellido_limit = StringVar()
regusuario_limit = StringVar()
regcontra_limit = StringVar()
regcontrarep_limit = StringVar()


#*      SALTAR ENTRE ENTRYS POR MEDIO DEL ENTER

def enterven1(event):
    login_contraseña.focus_set()

#  CREAR WIDGETS VENTANA 1

Label(ventana, bg=color, text="Login").pack()

Label(ventana, text="Usuario : ", bg=color).pack()
login_usuario = Entry(ventana, textvariable=logusuario_limit)
login_usuario.pack()
login_usuario.bind("<Return>", enterven1)

Label(ventana, text="Contraseña : ", bg=color).pack()
login_contraseña = Entry(ventana, textvariable=logcontra_limit, show="*")
login_contraseña.pack()


logusuario_limit.trace("w", lambda *args: character_limit(logusuario_limit))
logcontra_limit.trace("w", lambda *args: character_limit(logcontra_limit))


#   LIMITAR LOS ENTRY

def character_limit(x):
    if len(x.get()) > 0:
        x.set(x.get()[:10])


# ?  LOGIN

def login():
    usuario = login_usuario.get()
    contr = login_contraseña.get()
    cursor = db.cursor()
    cursor.execute("SELECT contrasenia FROM users WHERE usuario='" +
                   usuario+"' and contrasenia='"+contr+"'")

    if cursor.fetchall():
        abrirMenu()

    else:
        messagebox.showerror(title="Login incorrecto",
                             message="Usuario o contraseña incorrecto")


#!   VENTANTA DE REGISTRO

def nuevaVentana():

    newVentana = tk.Toplevel(ventana)
    newVentana.title("BASQUET LIVE")
    newVentana.geometry("300x290+800+250")
    newVentana['bg'] = color


    #*      SALTAR ENTRE ENTRYS POR MEDIO DEL ENTER    

    def enterven_registro1(event):
        entrada_apellido.focus_set()
    def enterven_registro2(event):
        entrada_usuario.focus_set()
    def enterven_registro3(event):
        entrada_contraseña.focus_set()
    def enterven_registro4(event):
        repetir_contraseña.focus_set()
    
    # CREAR WIDGETS VENTANA 2

    labeExample = tk.Label(newVentana, text="Registro : ").pack

    Label(newVentana, text="Nombre : ").pack()
    entrada_nombre = Entry(newVentana, textvariable=regnombre_limit)
    entrada_nombre.pack()
    entrada_nombre.bind("<Return>", enterven_registro1)

    Label(newVentana, text="Apellidos : ").pack()
    entrada_apellido = Entry(newVentana, textvariable=regapellido_limit)
    entrada_apellido.pack()
    entrada_apellido.bind("<Return>", enterven_registro2)

    Label(newVentana, text="Usuario : ").pack()
    entrada_usuario = Entry(newVentana, textvariable=regusuario_limit)
    entrada_usuario.pack()
    entrada_usuario.bind("<Return>", enterven_registro3)

    Label(newVentana, text="Contraseña : ").pack()
    entrada_contraseña = Entry(newVentana, textvariable=regcontra_limit, show="*")
    entrada_contraseña.pack()
    entrada_contraseña.bind("<Return>", enterven_registro4)

    Label(newVentana, text="Repita la Contraseña : ").pack()
    repetir_contraseña = Entry(newVentana, textvariable=regcontrarep_limit, show="*")
    repetir_contraseña.pack()

    regnombre_limit.trace("w", lambda *args: character_limit2(regnombre_limit))
    regapellido_limit.trace(
        "w", lambda *args: character_limit2(regapellido_limit))
    regusuario_limit.trace(
        "w", lambda *args: character_limit(regusuario_limit))
    regcontra_limit.trace("w", lambda *args: character_limit(regcontra_limit))
    regcontrarep_limit.trace(
        "w", lambda *args: character_limit(regcontrarep_limit))

    #   LIMITAR LOS ENTRY REGISTRO

    def character_limit2(x):
        if len(x.get()) > 0:
            x.set(x.get()[:16])


    #?  AGREGAR USUARIO A LA BASE DE DATOS

    def agregar_usuarioDB(nombre, apellido, usuario, contrasenia):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (nombre, apellido, usuario, contrasenia) VALUES (%s, %s, %s, %s)",
                           (nombre, apellido, usuario, contrasenia))
            db.commit()

        except mysql.connector.Error as error:
            messagebox.showerror("Error al agregar el usuario",
                                 f"No se pudo agregar el usuario: {error}")
        finally:
            cursor.close

    # ?  AGREGAR AL USUARIO A LA BD

    def agregar_user():

        cursor = db.cursor()

        # *  OBTENER DATOS DEL USER

        Nombre = entrada_nombre.get()
        Apellido = entrada_apellido.get()
        Usr_reg = entrada_usuario.get()
        Contra_reg = entrada_contraseña.get()
        Contra_reg_2 = repetir_contraseña.get()

        # *  VALIDAR NULL

        if not Nombre or not Apellido or not Usr_reg or not Contra_reg or not Contra_reg_2:
            messagebox.showerror("Error al agregar el usuario",
                                 "Por favor ingrese todos los datos del usuario")
            return

        # *  VALIDAR QUE LA CONTRA CON LA REPETICION SEAN IGUALES

        if (Contra_reg == Contra_reg_2):

            cursor.execute("INSERT INTO users (nombre, apellido, usuario, contrasenia) VALUES (%s, %s, %s, %s)",
                           (Nombre, Apellido, Usr_reg, Contra_reg))
            db.commit()
            messagebox.showinfo(title="Registro Correcto", message="Hola " +
                                Nombre+" "+Apellido+" ¡¡ \nSu registro fue exitoso.")
            newVentana.destroy()
        else:
            messagebox.showerror(title="Contraseña Incorrecta",
                                 message="Error¡¡¡ \nLas contraseñas no coinciden.")
            entrada_contraseña.delete(0, END)
            repetir_contraseña.delete(0, END)

        # *  AGREGAR EL NUEVO USUARIO

        agregar_usuarioDB(Nombre, Apellido, Usr_reg, Contra_reg)

    buttons = tk.Button(newVentana, text="Registrar ¡",
                        command=agregar_user, bg=color).pack(side="bottom")


Label(ventana, text=" ", bg=color).pack()
Button(text=" ENTRAR ", command=login, bg='#a6d4f2').pack()
Label(ventana, text=" ", bg=color).pack()
Label(ventana, text="No tienes una cuenta ? : ", bg=color).pack()
boton1 = Button(ventana, text="REGISTRO", bg='#a6d4f2',
                command=nuevaVentana).pack()


#!           **** MENU BASQUETBOL LIVE ****


# ?  LEER VALORES DE LA BD


def leer_valoresDB():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM horarios")
    return cursor.fetchall()



def abrirMenu():
    MenuLR = tk.Toplevel(ventana)
    ventana.withdraw()
    MenuLR.title("BASQUET LIVE")
    MenuLR.geometry("900x500")
    color = '#c5e2f6'
    MenuLR['bg'] = color


    #*      SALTAR ENTRE ENTRYS POR MEDIO DEL ENTER

    def enterven_menu1(event):
        entrada_equipo.focus_set()
    def enterven_menu2(event):
        entrada_fecha.focus_set()
    def enterven_menu3(event):
        entrada_hora.focus_set()


    #   CREAR LOS FRAMES

    frame1 = Frame(MenuLR)
    frame1.grid(rowspan=2, column=1, row=1)

    lugar_limit = StringVar()
    equipo_limit = StringVar()
    fecha_limit = StringVar()
    hora_limit = StringVar()


        
    #?  AGREGAR USUARIO A LA BASE DE DATOS
    
    def agregar_valoresDB(lugar, equipos, fecha, hora):
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO horarios (lugar, equipos, fecha, hora) VALUES (%s, %s, %s, %s)",
                            (lugar, equipos, fecha, hora))
            db.commit()

        except mysql.connector.Error as error:
            messagebox.showerror("Error al agregar las actividades",
                                f"No se pudo agregar las actividades: {error}")
        finally:
            cursor.close


        # ?  AGREGAR AL USUARIO A LA BD

    def agregar_valores():

        cursor = db.cursor()

        # *  OBTENER DATOS DEL USER

        Lugar =  entrada_lugar.get()
        Equipo = entrada_equipo.get()
        Fecha = entrada_fecha.get()
        Hora = entrada_hora.get()
      

        # *  VALIDAR NULL

        if not Lugar or not Equipo or not Fecha or not Hora:
            messagebox.showerror("Error al agregar el usuario",
                                 "Por favor llene los campos requeridos")
            return


        # *  AGREGAR EL NUEVO USUARIO

        agregar_valoresDB(Lugar, Equipo, Fecha, Hora)

    #?  MOSTRAR PRODUCTOS EN LA TABLA

    def mostrar_productos():
        cursor = db.cursor()
        sql = "SELECT * FROM horarios " 
        cursor.execute(sql)
        registro = cursor.fetchall()
        for dato in registro:                       
            tabla.insert('',END, text = dato[1], values=(dato[2], dato[3], dato[4]))

    #? ELIMINAR DATOS DE LA BASE DE DATOS

    def eliminar_valoresDB():
        cursor = db.cursor()
        select_item =tabla.selection()[0]
        linea = tabla.item(select_item)["values"][1]
        cursor.execute("DELETE FROM horarios WHERE lugar=%s",(linea,))
        tabla.delete(select_item)
        db.commit()
        cursor.close
        

    #!          VENTANA MENU WIDGETS

    Label(MenuLR, text="BIENVENIDO", font=(
        "Rockwell"), bg=color).place(x=70, y=20)

    # CREAR CAMPOS DE INICIO DE SESION
    Label(MenuLR, text="LUGAR:", font=(
        "Rockwell", 10), bg=color).place(x=20, y=60)
    entrada_lugar = Entry(MenuLR, textvariable=lugar_limit)
    entrada_lugar.place(x=120, y=60)
    entrada_lugar.bind("<Return>",enterven_menu1)

    Label(MenuLR, text="EQUIPO:", font=(
        "Rockwell", 10), bg=color).place(x=20, y=100)
    entrada_equipo = Entry(MenuLR, textvariable=equipo_limit)
    entrada_equipo.place(x=120, y=100)
    entrada_equipo.bind("<Return>",enterven_menu2)

    Label(MenuLR, text="FECHA:", font=(
        "Rockwell", 10), bg=color).place(x=20, y=140)
    entrada_fecha = Entry(MenuLR, textvariable=fecha_limit)
    entrada_fecha.place(x=120, y=140)
    entrada_fecha.bind("<Return>", enterven_menu3)

    Label(MenuLR, text="HORA:", font=(
        "Rockwell", 10), bg=color).place(x=20, y=180)
    entrada_hora = Entry(MenuLR, textvariable=hora_limit)
    entrada_hora.place(x=120, y=180)

    boton_agregar = Button(MenuLR, text="AGREGAR", font=('Arial',10,'bold'), bg='#a6d4f2',
                command=agregar_valores)
    boton_agregar.place(x=15, y=220)

    boton_mostrar = Button(MenuLR, command = mostrar_productos, text='MOSTRAR DATOS', bg='#a6d4f2', font=('Arial',10,'bold'))
    boton_mostrar.place(x=120, y=240)

    boton_eliminar = Button(MenuLR, command = eliminar_valoresDB, text=' BORRAR ', bg='#a6d4f2', font=('Arial',10,'bold'))
    boton_eliminar.place(x=15, y=260)

    #   LIMITAR LOS ENTRY

    lugar_limit.trace("w", lambda *args: character_limit3(lugar_limit))
    equipo_limit.trace("w", lambda *args: character_limit3(equipo_limit))
    fecha_limit.trace("w", lambda *args: character_limit3(fecha_limit))
    hora_limit.trace("w", lambda *args: character_limit4(hora_limit))

    def character_limit3(x):
        if len(x.get()) > 0:
            x.set(x.get()[:20])

    def character_limit4(x):
        if len(x.get()) > 0:
            x.set(x.get()[:7])

    # *      CREAR TABLA

    tabla = ttk.Treeview(MenuLR, height= 21,  columns=(
        "#1", "#2", "#3"), padding=2)
    tabla.place(x=280, y=20, width=600, height=460)

    tabla.heading("#0", text="LUGAR", anchor='center')
    tabla.heading("#1", text="EQUIPOS", anchor='center')
    tabla.heading("#2", text="FECHA", anchor='center')
    tabla.heading("#3", text="HORA", anchor='center')

    tabla.column("#0", width=150, minwidth=75, anchor='center')
    tabla.column("#1", width=150, minwidth=75, anchor='center')
    tabla.column("#2", width=150, minwidth=75, anchor='center')
    tabla.column("#3", width=146, minwidth=75, anchor='center')

    estilo = ttk.Style(frame1)
    estilo.theme_use('alt')
    estilo.configure(".", font=('Helvetica', 12, 'bold'), foreground='red2')
    estilo.configure("Treeview", font=('Helvetica', 10, 'bold'),
                     foreground='black',  background='white')
    estilo.map('Treeview', background=[
               ('selected', 'green2')], foreground=[('selected', 'black')])




ventana.mainloop()