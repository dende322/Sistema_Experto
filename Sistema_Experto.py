from tkinter import *
from tkinter import ttk
import clips

sistemaExperto= clips.Environment()
sistemaExperto.clear()
ventana = Tk()
bandera = False

ToleranciaAlRiesgo = StringVar()
Temporalidad = StringVar()
ObjetivoFinanciero = StringVar()
ConocimientoFinanciero = StringVar()
CapacidadFinanciera = StringVar()
nombre = StringVar()
edad = IntVar()
correo = StringVar()
tipo = StringVar()
herramientas_n = IntVar()
herramientas = []

ToleranciaAlRiesgo.set(None)
Temporalidad.set(None)
ObjetivoFinanciero.set(None)
ConocimientoFinanciero.set(None)
CapacidadFinanciera.set(None)
nombre.set("")
edad.set(0)
correo.set("")

main_frame = Frame(ventana)
my_Canvas = Canvas(main_frame)
Canvas_frame = ttk.LabelFrame(my_Canvas, padding="20 10 10 40")
Result_frame = ttk.LabelFrame(Canvas_frame, padding="20 10 20 10", style='My.TFrame')


def Sistema_Experto():
    #Inicio Plantilla de Hechos
    templateUsuario = ("(deftemplate usuario"
    "\n(slot nombre (type STRING))"
    "\n(slot edad (type INTEGER))"
    "\n(slot correo (type STRING))"
    "\n)")

    templatePregunta = ("(deftemplate pregunta"
    "\n(slot id (type INTEGER))"
    "\n(slot respuesta (type SYMBOL))"
    "\n)")

    templateHerramienta = ("(deftemplate herramienta"
    #"\n(slot id (type INTEGER))"
    "\n(slot descripcion (type STRING))"
    "\n)")

    templatePerfil = ("(deftemplate perfil"
    "\n(slot tipo (type SYMBOL))"
    "\n)")

    templateValor = ("(deftemplate puntuacion"
    "\n(slot valor (type INTEGER))"
    "\n)")
    #Fin Plantilla de Hechos


    #Funcion que retorna el puntaje de cada pregunta
    funcionAsignarPuntos = ("(deffunction asignar-puntos (?respuesta)"
        "\n(if (eq ?respuesta a)"
            "\nthen (return 1)"
            "\nelse (if (eq ?respuesta b)"
                "\nthen (return 2)"
                "\nelse (if (eq ?respuesta c)"
                    "\nthen (return 3)"
                    "\nelse (return 0)"
                "\n)"
            "\n)"
        "\n)"
    "\n)")

    #Inicio de Creación de Reglas
    #Regla para calcular el total (sumatoria) de los puntos de las preguntas
    reglaCalcularPuntos = ("(defrule calcular-puntuacion"
        "\n(pregunta (id 1) (respuesta ?r1))"
        "\n(pregunta (id 2) (respuesta ?r2))"
        "\n(pregunta (id 3) (respuesta ?r3))"
        "\n(pregunta (id 4) (respuesta ?r4))"
        "\n(pregunta (id 5) (respuesta ?r5))"
    "\n=>"
        "\n(bind ?nueva-puntuacion (+ (asignar-puntos ?r1) (asignar-puntos ?r2) (asignar-puntos ?r3) (asignar-puntos ?r4) (asignar-puntos ?r5)))"
        "\n(assert (puntuacion (valor ?nueva-puntuacion)))"
    "\n)")
    #Regla para asiganr perfil Conservador
    reglaPerfilConservador = ("(defrule perfil-conservador"
        "\n(puntuacion (valor ?p&:(>= ?p 5)&:(<= ?p 8)))"
    "\n=>"
        "\n(assert (perfil (tipo Conservador)))"
    "\n)")
    #Regla para asignar perfil Moderado
    reglaPerfilModerado = ("(defrule perfil-moderado"
        "\n(puntuacion (valor ?p&:(>= ?p 9)&:(<= ?p 12)))"
    "\n=>"
        "\n(assert (perfil (tipo Moderado)))"
    "\n)")
    #Regla para asignar perfil Agresivo
    reglaPerfilAgresivo = ("(defrule perfil-agresivo"
        "\n(puntuacion (valor ?p&:(>= ?p 13)&:(<= ?p 15)))"
    "\n=>"
        "\n(assert (perfil (tipo Agresivo)))"
    "\n)")
    #Se crean las reglas con respecto a la asignación de la herramientas financieras
    #recomendadas al usuario
    reglaHerramientasConservador = ("(defrule herramientas-conservador"
        "\n(perfil(tipo Conservador))"
    "\n=>"
        "\n(assert (herramienta (descripcion \"Bonos publicos o privados\")))"
        "\n(assert (herramienta (descripcion \"Cuentas de ahorro\")))"
        "\n(assert (herramienta (descripcion \"Pagare\")))"
        "\n(assert (herramienta (descripcion \"Titulos de deuda\")))"
        "\n(assert (herramienta (descripcion \"Depósitos a largo plazo\")))"
    "\n)")

    reglaHerramientasModerado = ("(defrule herramientas-moderado"
        "\n(perfil(tipo Moderado))"
    "\n=>"
        "\n(assert (herramienta (descripcion \"Bonos publicos o privados\")))"
        "\n(assert (herramienta (descripcion \"Acciones de empresas\")))"
        "\n(assert (herramienta (descripcion \"CDT\")))"
    "\n)")

    reglaHerramientasAgresivo = ("(defrule herramientas-agresivo"
        "\n(perfil(tipo Agresivo))"
    "\n=>"
        "\n(assert (herramienta (descripcion \"Acciones de empresas\")))"
        "\n(assert (herramienta (descripcion \"Portafolios diversificadores a largo plazo\")))"
    "\n)")
    #Fin de Creación de Reglas

    #Se crean los Hechos
    sistemaExperto.build(templateUsuario)
    sistemaExperto.build(templatePregunta)
    sistemaExperto.build(templateHerramienta)
    sistemaExperto.build(templatePerfil)
    sistemaExperto.build(templateValor)

    #Se inicia el Hecho puntuacón con valor de 0
    deffactPuntuacion = ("(deffacts inicializacion"+
        "\n(puntuacion (valor 0))"+
    "\n)")
    sistemaExperto.build(deffactPuntuacion)

    #Se crea la funcion encargada de retornar la puntuación a las preguntas
    sistemaExperto.build(funcionAsignarPuntos)

    #Se crean las reglas
    sistemaExperto.build(reglaCalcularPuntos)

    sistemaExperto.build(reglaPerfilConservador)
    sistemaExperto.build(reglaPerfilModerado)
    sistemaExperto.build(reglaPerfilAgresivo)

    sistemaExperto.build(reglaHerramientasConservador)
    sistemaExperto.build(reglaHerramientasModerado)
    sistemaExperto.build(reglaHerramientasAgresivo)

def AsiganarPreguntas():
    try:
        sistemaExperto.assert_string(f"(pregunta (id 1) (respuesta {ToleranciaAlRiesgo.get()}))")
        sistemaExperto.assert_string(f"(pregunta (id 2) (respuesta {Temporalidad.get()}))")
        sistemaExperto.assert_string(f"(pregunta (id 3) (respuesta {ObjetivoFinanciero.get()}))")
        sistemaExperto.assert_string(f"(pregunta (id 4) (respuesta {ConocimientoFinanciero.get()}))")
        sistemaExperto.assert_string(f"(pregunta (id 5) (respuesta {CapacidadFinanciera.get()}))")
        sistemaExperto.assert_string(f"(usuario (nombre \"{nombre.get()}\") (edad {edad.get()}) (correo \"{correo.get()}\"))")
        
        sistemaExperto.run()
        ObtenerInformacion()

    except ValueError:
        print(ValueError)
        pass

def ObtenerInformacion():
    tipo_value = ""
    descripcion_value = []
    for fact in sistemaExperto.facts():
        factString = str(fact)
        # Check if factString contains "tipo" before splitting to avoid IndexError
        if "tipo" in factString:
        # Adjust split to handle potential variations in the string
            tipo_value = factString.split("(tipo ")[1].split(")")[0]
        if "descripcion" in factString:
            descripcion_value.append(factString.split("(descripcion \"")[1].split("\")")[0])
        if "valor" in factString:
            puntos = factString.split("(valor ")[1].split(")")[0]

    tipo.set(tipo_value)
    herramientas_n.set(len(descripcion_value))
    GenerarInforme(descripcion_value, puntos)

def LimpiarInformarcion():
    ToleranciaAlRiesgo.set(None)
    Temporalidad.set(None)
    ObjetivoFinanciero.set(None)
    ConocimientoFinanciero.set(None)
    CapacidadFinanciera.set(None)
    nombre.set("")
    edad.set(0)
    correo.set("")
    for widget in Result_frame.winfo_children():
        widget.destroy()
    #Reinicia los Hechos
    sistemaExperto.reset()

def GenerarInforme(descripcion_value, puntos):
    #Normalizamos el puntaje para obtener valores de 0 a 10 incluyendo decimales para el sistema difuzo
    Puntaje_Normalizado = ((int(puntos)-5)/(15-5))*10
    #if(bandera):
    #    Result_frame = ttk.LabelFrame(Canvas_frame, padding="20 10 20 10", style='My.TFrame')

    Result_frame.grid(column=1, row=27, columnspan=5, rowspan=10, sticky=(N, W, E, S))
    ttk.Label(Result_frame, text="Sr/ Sra " + nombre.get() + ", a continuación se presenta tu Informe:", background='#c6c6c6').grid(column=0, row=0, columnspan=5, sticky=W, pady=(10, 0))
    ttk.Label(Result_frame, text="Perfil:", background='#c6c6c6').grid(column=0, row=1, sticky=E, pady=(0, 10))
    ttk.Label(Result_frame, textvariable=tipo, background='#c6c6c6').grid(column=1, row=1, columnspan=2, sticky=W, pady=(0, 10))
    ttk.Label(Result_frame, text="Perfil nomalizado (Escala de 0 a 10):", background='#c6c6c6').grid(column=0, row=2, columnspan=2, sticky=W, pady=(0, 10))
    ttk.Label(Result_frame, text=Puntaje_Normalizado, background='#c6c6c6').grid(column=2, row=2, sticky=E, pady=(0, 10))
    ttk.Label(Result_frame, text="Las opciones de inversión recomendadas son:", background='#c6c6c6').grid(column=0, row=3, columnspan=4, sticky=W, pady=(0, 10))
    contador = 0
    while contador < herramientas_n.get():
        row_ = (4+contador+1)
        ttk.Label(Result_frame, text=descripcion_value[contador], background='#c6c6c6').grid(column=1, row=row_, columnspan=3, sticky=W, pady=(0, 10))
        contador+=1
   
def Interface_Grafica():
    main_frame.pack(fill=BOTH, expand=1)
    
    ventana.columnconfigure(0, weight=1)
    ventana.rowconfigure(0, weight=1)

    my_Canvas.pack(side=LEFT, expand=1, fill=BOTH, pady=(10, 30))

    my_Scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_Canvas.yview)
    my_Scrollbar.pack(side=RIGHT, fill=Y)

    my_Canvas.configure(yscrollcommand=my_Scrollbar.set)
    my_Canvas.bind('<Configure>', lambda e: my_Canvas.configure(scrollregion= my_Canvas.bbox("all")))
    Canvas_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    my_Canvas.create_window((0,0), window=Canvas_frame, anchor="nw")
    #Canva Resultado
    s = ttk.Style()
    s.configure('My.TFrame', background='#c6c6c6', color='black')

    #Canvas_Frame
    ttk.Label(Canvas_frame, text="!Hola!").grid(column=0, row=0, columnspan=2, sticky=W, pady=(0, 10))
    ttk.Label(Canvas_frame, text="Para empezar necesitamos que ingrese la siguiente uinformacion").grid(row=1, column=0, columnspan=5, sticky=W, pady=(10, 0))
    #Información Personal
    ttk.Label(Canvas_frame, text="Nombre: "). grid(column=0, row=2, sticky=(E), pady=(10, 0))
    nombre_Entry = ttk.Entry(Canvas_frame, width=30, textvariable=nombre)
    nombre_Entry.grid(column=1, row=2, pady=(10, 0))
    nombre_Entry.focus()
    ttk.Label(Canvas_frame, text="Edad: "). grid(column=0, row=3, sticky=(E), pady=(10, 0))
    nombre_Entry = ttk.Entry(Canvas_frame, width=30, textvariable=edad)
    nombre_Entry.grid(column=1, row=3, pady=(10, 0))
    ttk.Label(Canvas_frame, text="Correo: "). grid(column=0, row=4, sticky=(E), pady=(10, 0))
    nombre_Entry = ttk.Entry(Canvas_frame, width=30, textvariable=correo)
    nombre_Entry.grid(column=1, row=4, pady=(10, 0))
    #Preguntas
    #Pregunta 1
    ttk.Label(Canvas_frame, text="1. ¿Cómo percibes tu tolerancia al riego?").grid(column=0, row=5, columnspan=5, sticky=W, padx=10)
    Radiobutton(Canvas_frame, 
                text="a). Prefiero no correr riesgos, incluso si eso significa obtener rendimientos bajos.", 
                value="a", 
                variable=ToleranciaAlRiesgo,
                ).grid(column=0, row=6, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="b). Estoy dispuesto a asumir un riesgo moderado para obtener rendimientos equilibrados.", 
                value="b", 
                variable=ToleranciaAlRiesgo,
                ).grid(column=0, row=7, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="c). Estoy dispuesto a asumir un alto riesgo para obtener rendimientos potencialmente altos.", 
                value="c", 
                variable=ToleranciaAlRiesgo,
                ).grid(column=0, row=8, sticky=(W,S), padx=(30, 5), columnspan=7)
    #Pregunta 2
    ttk.Label(Canvas_frame, text="2. ¿Cuál sería el tiempo de tu inversión ideal?").grid(column=0, row=9, columnspan=5, sticky=W, padx=10)
    Radiobutton(Canvas_frame, 
                text="a). Menos de 1 año.", 
                value="a", 
                variable=Temporalidad,
                ).grid(column=0, row=10, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="b). Entre 1 y 5 años.", 
                value="b", 
                variable=Temporalidad,
                ).grid(column=0, row=11, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="c). Más de 5 años.", 
                value="c", 
                variable=Temporalidad,
                ).grid(column=0, row=12, sticky=(W,S), padx=(30, 5), columnspan=7)
    #Pregunta 3
    ttk.Label(Canvas_frame, text="3. ¿Cual es el pricipal objetivo de tu inversón?").grid(column=0, row=13, columnspan=5, sticky=W, padx=10)
    Radiobutton(Canvas_frame, 
                text="a). Preservar mi capital y evitar pérdidas.", 
                value="a", 
                variable=ObjetivoFinanciero,
                ).grid(column=0, row=14, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="b). Obtener un crecimiento moderado de mi inversión.", 
                value="b", 
                variable=ObjetivoFinanciero,
                ).grid(column=0, row=15, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="c) Maximizar el crecimiento de mi inversión, incluso si eso implica mayor riesgo.", 
                value="c", 
                variable=ObjetivoFinanciero,
                ).grid(column=0, row=16, sticky=(W,S), padx=(30, 5), columnspan=7)
    #Pregunta 4
    ttk.Label(Canvas_frame, text="4. ¿Posees algún conocimiento o experiencia con respecto al mundo de las inversiones?").grid(column=0, row=17, columnspan=7, sticky=W, padx=10)
    Radiobutton(Canvas_frame, 
                text="a). Tengo poco o ningún conocimiento sobre inversiones.", 
                value="a", 
                variable=ConocimientoFinanciero,
                ).grid(column=0, row=18, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="b). Tengo un conocimiento básico y he invertido en productos simples.", 
                value="b", 
                variable=ConocimientoFinanciero,
                ).grid(column=0, row=19, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="c). Tengo experiencia invirtiendo en productos complejos como acciones o derivados.", 
                value="c", 
                variable=ConocimientoFinanciero,
                ).grid(column=0, row=20, sticky=(W,S), padx=(30, 5), columnspan=7)
    #Pregunta 5
    ttk.Label(Canvas_frame, text="5. ¿Cuál sería tu capacidad financiera de inversión?").grid(column=0, row=21, columnspan=7 ,sticky=W, padx=10)
    Radiobutton(Canvas_frame, 
                text="a). Solo puedo invertir una pequeña parte de mis ingresos (menos del 10%).", 
                value="a", 
                variable=CapacidadFinanciera,
                ).grid(column=0, row=22, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="b). Puedo invertir una parte moderada de mis ingresos (entre 10% y 30%).", 
                value="b", 
                variable=CapacidadFinanciera,
                ).grid(column=0, row=23, sticky=(W,S), padx=(30, 5), columnspan=7)
    Radiobutton(Canvas_frame, 
                text="c). Puedo invertir una parte significativa de mis ingresos (más del 30%).", 
                value="c", 
                variable=CapacidadFinanciera,
                ).grid(column=0, row=24, sticky=(W,S), padx=(30, 5), pady=(0, 30), columnspan=7)
      
    ttk.Button(Canvas_frame, text="Generar Perfil", width=30, padding="0 10 0 10", command=AsiganarPreguntas).grid(column=0, row=25, columnspan=3, pady=2, padx=10, sticky=(W, E))
    ttk.Button(Canvas_frame, text="Limpiar", width=30, padding="0 10 0 10", command=LimpiarInformarcion).grid(column=3, row=25, columnspan=3, pady=2, padx=10, sticky=(W, E))

    ttk.Label(Canvas_frame).grid(column=0, row=26, pady=10)
    ventana.mainloop()

def main():
    Result_frame.config(height=50)
    ventana.geometry("650x600")
    ventana.title("Tu Perfil Financiero")

    Sistema_Experto()
    Interface_Grafica()

if __name__ == "__main__":
    main()

