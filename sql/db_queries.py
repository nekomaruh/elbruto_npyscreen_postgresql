import psycopg2 as ps
import random
import globals

connection = ps.connect(user="postgres", password="postgres", database="elbruto", host="localhost", port="5432")
cursor = connection.cursor()

def createTables():

    cursor.execute('CREATE TABLE usuario(nick TEXT PRIMARY KEY NOT NULL UNIQUE,contrasena TEXT NOT NULL, nombre TEXT NOT NULL, email TEXT NOT NULL,pais TEXT NOT NULL);')
    cursor.execute('CREATE TABLE administrador(nick TEXT PRIMARY KEY NOT NULL,FOREIGN KEY(nick) REFERENCES usuario(nick));')
    cursor.execute('CREATE TABLE jugador(nick TEXT PRIMARY KEY NOT NULL,baneadosn BOOLEAN NOT NULL,cantreportes INTEGER NOT NULL,FOREIGN KEY(nick) REFERENCES usuario(nick));')
    cursor.execute('CREATE TABLE avatar(nick TEXT PRIMARY KEY NOT NULL,nivel INTEGER NOT NULL,ptosexp INTEGER NOT NULL,ptosvelocidad INTEGER NOT NULL,ptosvida INTEGER NOT NULL,ptosataque INTEGER NOT NULL,FOREIGN KEY (nick) REFERENCES jugador(nick));')
    cursor.execute('CREATE TABLE reporta(nick TEXT NOT NULL,nickreportado TEXT NOT NULL,PRIMARY KEY (nick, nickReportado),FOREIGN KEY (nick) REFERENCES jugador(nick),FOREIGN KEY (nickreportado) REFERENCES jugador(nick));')
    connection.commit()
    
    print("Tablas agregadas correctamente!")


def logIn(nick, contrasena):
    cursor.execute("select * from usuario where nick = %s and contrasena = %s;",(nick, contrasena))
    result = cursor.fetchall()
    if(len(result)==0):
        print("No se encontro usuario")
        return False
    else:
        global eb_usuario, eb_contrasena, eb_nombre, eb_correo, eb_pais
        for row in result:
            eb_usuario = row[0]
            eb_contrasena = row[1]
            eb_nombre = row[2]
            eb_correo = row[3]
            eb_pais = row[4]
        return True

def getLogedUser():
    return eb_usuario, eb_contrasena, eb_nombre, eb_correo, eb_pais

def getLogedUserAndAvatar():
    return eb_usuario, eb_nivel, eb_experiencia, eb_velocidad, eb_vida, eb_ataque

def userExists(usuario):
    sql = "select * from usuario where nick = '" + usuario + "';"
    cursor.execute(sql)
    result = cursor.fetchall()
    if(len(result)==0):
        return False
    return True

def banear(usuario):
    sql = "update jugador set baneadosn='true' where nick ='"+usuario+"';"
    cursor.execute(sql)
    connection.commit()


def userIsAdmin(usuario):
    sql = "select * from administrador where nick = '" + usuario +"';"
    cursor.execute(sql)
    result = cursor.fetchall()
    if(len(result)==0):
        return False
    return True

def getAvatarFromUser(usuario):
    sql = "select * from avatar where nick = '" + usuario + "';"
    cursor.execute(sql)
    result = cursor.fetchall()
    
    global eb_usuario, eb_nivel, eb_experiencia, eb_velocidad, eb_vida, eb_ataque
    for row in result:
        eb_usuario = row[0]
        eb_nivel = row[1]
        eb_experiencia = row[2]
        eb_velocidad = row[3]
        eb_vida = row[4]
        eb_ataque = row[5]
    return eb_usuario, eb_nivel, eb_experiencia, eb_velocidad, eb_vida, eb_ataque

def getReportados():
    sql = """select nick, cantreportes from jugador where cantreportes>0 and baneadosn='false';"""
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def wasReported(usuario, reportado):
    sql = "select exists( select nick from reporta where nick='"+usuario+"' and nickreportado='"+reportado +"');"
    cursor.execute(sql)
    result = cursor.fetchall()
    return True in result[0]

def wasBanned(usuario):
    sql = "select exists( select nick from jugador where nick='"+usuario+"' and baneadosn='true');"
    cursor.execute(sql)
    result = cursor.fetchall()
    return True in result[0]
    
def reportUser(usuario, reportado):
    cursor.execute("""insert into reporta(nick, nickreportado)
    values(%s,%s)""",(usuario, reportado))
    connection.commit()
    sql = "update jugador set cantreportes=cantreportes+1 where nick='"+reportado+"';"
    cursor.execute(sql)
    connection.commit()

def insertarUsuario(nick, contrasena, nombre, pais):
    cursor.execute("""insert into usuario(nick, 
    contrasena, nombre, email, pais)
    values(%s,%s,%s,'null',%s)""",(nick,contrasena,nombre,pais))
    connection.commit()
    insertarJugador(nick,False,0)
    insertarAvatar(nick)

def insertarJugador(nick,baneadosn,cantreportes):
    cursor.execute("""insert into 
    jugador(nick,baneadosn,cantreportes)
    values(%s,%s,%s)""", (nick, baneadosn, cantreportes))
    connection.commit()

def encontrarPelea(nick, nivel):
    cursor.execute("""select * from avatar 
    where nick != %s 
    and nivel>=%s
    and nivel<=%s """,(nick, nivel-1, nivel+1))
    result = cursor.fetchall()
    if len(result) == 0:
        return False
    else:
        enemigo = random.randint(0,len(result)-1)
        enemigo = result[enemigo]
        global en_usuario, en_nivel, en_experiencia, en_velocidad, en_vida, en_ataque
        en_usuario = enemigo[0]
        en_nivel = enemigo[1]
        en_experiencia = enemigo[2]
        en_velocidad = enemigo[3]
        en_vida = enemigo[4]
        en_ataque = enemigo[5]
        return True

def pelear(nick, nvl, xp, vel, atk, vida):
    global en_usuario, en_nivel, en_experiencia, en_velocidad, en_vida, en_ataque
    resultado = "None"
    atacar = False
    
    # Vidas en pelea
    p_vida = vida
    pe_vida = en_vida

    # Iniciativa en pelea (Por defecto no inicia primero)
    if vel==en_velocidad: 
        # Si tienen la misma velocidad hay un 50% de empezar primero
        suerte = random.randint(0,1)
        if(suerte==0):
            atacar = True
    elif vel>en_velocidad:
        # Si la velocidad mayor, el usuario empieza primero
        atacar = True
        
    # Esquivas de jugadores
    esquiva_usuario = vel
    esquiva_enemigo = en_velocidad
    if(esquiva_enemigo>80):
        esquiva_enemigo = 80
    if(esquiva_usuario>80):
        esquiva_usuario = 80

    print("Comienza la pelea (STATS INICIALES)")
    if(atacar==True):
        print("Usuario empieza primero")
    else:
        print("Enemigo empieza primero")
    print(nick+" - "+str(nvl)+" - vida: "+str(p_vida)+" - vel: "+str(vel)+" - atk: "+ str(atk))
    print(en_usuario+" - "+str(en_nivel)+" - vida: "+str(pe_vida)+" - vel: "+str(en_velocidad)+" - atk: "+ str(en_ataque))

    while(True):
        if(atacar==True):
            print("ATACA USUARIO")
            # Aplicar esquivas
            if random.random() < esquiva_enemigo/100:
                print("Enemigo esquiva")
            else:
                print("Enemigo sufre danos")
                pe_vida = pe_vida - atk # Usuario ataca a enemigo
            atacar = False

        else:
            print("ATACA ENEMIGO")
            # Aplicar esquivas
            if random.random() < esquiva_usuario/100:
                print("Usuario esquiva")
            else:
                p_vida = p_vida - en_ataque # Enemigo ataca a usuario
            atacar = True

        print(nick+" - "+str(nvl)+" - vida: "+str(p_vida)+" - vel: "+str(vel)+" - atk: "+ str(atk))
        print(en_usuario+" - "+str(en_nivel)+" - vida: "+str(pe_vida)+" - vel: "+str(en_velocidad)+" - atk: "+ str(en_ataque))

        if(p_vida<=0 or pe_vida<=0):
            xp_ganada = 0
            if(p_vida<=0):
                resultado = "DERROTA"
                print("DERROTA")
                xp_ganada = 20
            if(pe_vida<=0):
                resultado = "VICTORIA"
                print("VICTORIA")
                xp_ganada = 100
            new_nvl, new_xp, new_atk, new_vel, new_vida = calcularSiguienteNivel(nvl,xp,xp_ganada, atk, vel, vida)
            updateAvatar(nick, new_nvl, new_xp, new_atk, new_vel, new_vida)
            # Actualizamos los datos localmente tambi{en}
            global eb_nivel, eb_experiencia, eb_velocidad, eb_vida, eb_ataque
            eb_nivel = new_nvl
            eb_experiencia = new_xp
            eb_velocidad = new_vel
            eb_vida = new_vida
            eb_ataque = new_atk
            print("Base de datos actualizada...")
            break
    
    return resultado, en_usuario, en_nivel

def updateAvatar(nick, new_nvl, new_xp, new_atk, new_vel, new_vida):
    cursor.execute("""update avatar
    set nivel = %s, ptosexp = %s,
    ptosvelocidad = %s, ptosvida = %s,
    ptosataque = %s where
    nick = %s;""", (str(new_nvl),str(new_xp), str(new_vel), str(new_vida), str(new_atk), nick))
    connection.commit()
    return

def calcularSiguienteNivel(nvl, xp, xp_ganada, atk, vel, vida):
    xp_siguiente_nivel = 100 + (nvl*50)
    xp = xp_ganada + xp

    # Si se excede la xp en el nivel actual, subir de nivel y retornar la nueva xp
    if(xp >= xp_siguiente_nivel):
        xp = xp - xp_siguiente_nivel
        nvl = nvl+1
        xp_siguiente_nivel = 100 + (nvl*50)
        stats = random.randint(1,3)
        # Aumenta los stats al subir de nivel
        if(stats==1):
            atk = atk + 1
        elif(stats==2):
            vel = vel + 3
        else:
            vida = vida + 3

    print("XP necesaria para el siguiente nivel: "+str(xp)+"/"+str(xp_siguiente_nivel))
    print("Nivel luego de la batalla: "+str(nvl))
    return nvl, xp, atk, vel, vida


def insertarAvatar(nick):
    nivel = 1
    ataque = random.randint(1, 3)
    vida = random.randint(10, 20)
    velocidad = random.randint(1, 10)
    experiencia = 0
    cursor.execute("""insert into
    avatar(nick, nivel, ptosexp, ptosvelocidad, ptosvida, ptosataque)
    values(%s,%s,%s,%s,%s,%s)""",(nick, nivel, experiencia, velocidad, vida, ataque))
    connection.commit()

if __name__ == "__main__":
    #print(wasBanned("neko"))
    #banear("neko")
    #reportUser('khal12','kyoz')
    #print(wasReported('neko','kyoz'))
    #nivel = 1
    #xp = 100
    #print(encontrarPelea("neko",nivel))
    #print(pelear("neko",nivel,xp,4,13,6))
    #print(getAvatarFromUser("neko"))
    #print(reportUser("neko","kyoz"))
    #print(userExists("neko"))
    #insertarUsuario('neko','1234','Johan Esteban Ordenes Galleguillos', 'Chile')
    #insertarUsuario('kyoz','1234','Julieta Rueda', 'Argentina')
    #insertarAvatar("neko")
    #insertarAvatar("kyoz")
    #isLoged = logIn('neko','1234')
    print(0)