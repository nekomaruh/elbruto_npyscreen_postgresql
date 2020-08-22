import npyscreen as nps
import db_queries as db
import globals as g
import sys
import save

class Menu(nps.FormWithMenus):
    def create(self):
        self.menu = self.new_menu(name="Main Menu", shortcut='m')
        self.menu.addItem("Item 1", self.press_1, "1")
        self.menu.addItem("Item 2", self.press_2, "2")
        self.menu.addItem("Exit Form", self.exit_form, "^X")
    def press_1(self):
        nps.notify_confirm("Has presionado 1","Item 1", editw=1)
    def press_2(self):
        nps.notify_confirm("Has presionado 2","Item 2", editw=1)
    def exit_form(self):
        self.parentApp.switchForm(None)


class Login(nps.ActionForm):
    def create(self):
        self.usuario = self.add(nps.TitleText, name='Usuario:')
        self.contrasena = self.add(nps.TitlePassword, name='Contraseña:')
        self.add(nps.ButtonPress, name="Regístrate", when_pressed_function=self.sign_up)
    def on_ok(self):
        userExists = db.userExists(self.usuario.value)
        if(userExists):
            isLoged = db.logIn(self.usuario.value, self.contrasena.value)
            if(isLoged):
                isAdmin = db.userIsAdmin(self.usuario.value)
                if(isAdmin):
                    # Cargar la cuenta de administrador
                    usuario, contrasena, nombre, correo, pais = db.getLogedUser()
                    self.parentApp.getForm('PERFIL_ADMIN').usuario.value = usuario
                    self.contrasena.value = ""
                    self.parentApp.change_form('PERFIL_ADMIN')
                else:
                    # Cargar la cuenta del jugador
                    isBanned = db.wasBanned(self.usuario.value)
                    if(isBanned):
                        nps.notify_wait("Has sido baneado permanentemente del juego", "Lo sentimos")
                    else:
                        usuario, nivel, experiencia, velocidad, vida, ataque = db.getAvatarFromUser(self.usuario.value)
                        maxExpNivel = 100 + (nivel*50)
                        self.parentApp.getForm('PERFIL').usuario.value = usuario
                        self.parentApp.getForm('PERFIL').ataque.value = str(ataque)
                        self.parentApp.getForm('PERFIL').vida.value = str(vida)
                        self.parentApp.getForm('PERFIL').velocidad.value = str(velocidad)
                        self.parentApp.getForm('PERFIL').nivel.value = str(nivel)
                        self.parentApp.getForm('PERFIL').xp = experiencia
                        self.parentApp.getForm('PERFIL').experiencia.value = str(experiencia) + "/" + str(maxExpNivel)
                        self.contrasena.value = ""
                        self.parentApp.change_form('PERFIL')
            else:
                nps.notify_wait("Usuario o contraseña incorrectos", "Error")
        else:
            nps.notify_wait("No se ha encontrado el usuario en la base de datos", "Error")
    def sign_up(self):
        self.contrasena.value = ""
        self.parentApp.change_form('REGISTRO')
    def on_cancel(self):
        self.parentApp.change_form(None) # Sale del programa

class Registro(nps.ActionForm):
    def create(self):
        self.usuario = self.add(nps.TitleText, name="Usuario:")
        self.contrasena = self.add(nps.TitlePassword, name="Contraseña:")
        self.contrasena_v = self.add(nps.TitlePassword, name="Verifique la contraseña:")
        self.nombre = self.add(nps.TitleText, name="Nombre:")
        self.pais = self.add(nps.TitleText, name="País:")
    def on_ok(self):
        exists = db.userExists(self.usuario.value)
        if(exists):
            nps.notify_wait("Ya existe el usuario en la base de datos", "Error")
        else:
            if(self.contrasena.value == self.contrasena_v.value):
                db.insertarUsuario(self.usuario.value,self.contrasena.value, self.nombre.value, self.pais.value)
                nps.notify_wait("Usuario ingresado con éxito, espere un momento...", "¡Felicidades!")
                self.usuario.value = ""
                self.contrasena.value = ""
                self.contrasena_v.value = ""
                self.nombre.value = ""
                self.pais.value = ""
                self.parentApp.change_form('MAIN')
            else:
                nps.notify_wait("Las contraseñas no coinciden", "Error")
    def on_cancel(self):
        self.parentApp.change_form('MAIN')

class Perfil(nps.FormBaseNew):
    def create(self):
        self.xp = 0
        self.usuario = self.add(nps.TitleFixedText, name="Usuario")
        self.ataque = self.add(nps.TitleFixedText, name="Ataque:")
        self.vida = self.add(nps.TitleFixedText, name="Vida:")
        self.velocidad = self.add(nps.TitleFixedText, name="Velocidad:")
        self.nivel = self.add(nps.TitleFixedText, name="Nivel:")
        self.experiencia = self.add(nps.TitleFixedText, name="Puntos de experiencia:")
        self.add(nps.ButtonPress, name="Cerrar sesión", when_pressed_function=self.close_session)
        self.add(nps.ButtonPress, name="Reportar a otro jugador", when_pressed_function=self.report_player)
        self.add(nps.ButtonPress, name="Pelear", when_pressed_function=self.fight)
    def close_session(self):
        self.parentApp.change_form('MAIN')
    def report_player(self):
        self.parentApp.getForm('REPORTAR').usuario = self.usuario.value
        self.parentApp.change_form('REPORTAR')
    def fight(self):
        encontrado = db.encontrarPelea(self.usuario.value,int(self.nivel.value))
        if not encontrado:
            nps.notify_wait("No se encontraron enemigos para tu nivel", "Error")
        else:
            b_usr = self.usuario.value
            b_nvl = int(self.nivel.value)
            b_vel = int(self.velocidad.value)
            b_vid = int(self.vida.value)

            resultado, enemigo, nvl_enemigo = db.pelear(b_usr,b_nvl,self.xp,b_vel,b_vel,b_vid)

            self.parentApp.getForm('PELEA').vs.value = self.usuario.value + "(nivel "+self.nivel.value+") vs "+enemigo+" (nivel "+str(nvl_enemigo)+")"
            self.parentApp.getForm('PELEA').resultado.value = resultado
            if(resultado=="VICTORIA"):
                self.parentApp.getForm('PELEA').xp_ganada.value = "100 xp"
            else:
                self.parentApp.getForm('PELEA').xp_ganada.value = "20 xp"
            self.parentApp.change_form('PELEA')
        


class Reportar(nps.ActionForm):
    def create(self):
        self.usuario = "None"
        self.reportado = self.add(nps.TitleText, name='Ingrese el usuario que desea reportar:')
    def on_ok(self):
        # Reportar en la base de datos
        if(self.usuario == self.reportado.value):
            nps.notify_wait("No puedes reportarte a tí mismo", "Error")
        else:
            exists = db.userExists(self.reportado.value)
            if(exists):
                wasReported = db.wasReported(self.usuario, self.reportado.value)
                if(wasReported):
                    nps.notify_wait("Ya has reportado a este usuario anteriormente "+str(wasReported)+" que triste", "Error")
                else:
                    db.reportUser(self.usuario, self.reportado.value)
                    nps.notify_wait("Usuario reportado con éxito", "Información")
            else:
                nps.notify_wait("No existe este usuario en la base de datos", "Error")
        self.parentApp.change_form('PERFIL')
    def on_cancel(self):
        self.parentApp.change_form('PERFIL')

class Pelea(nps.ActionForm):
    def create(self):
        self.vs = self.add(nps.TitleFixedText, name="Se enfrentó ")
        self.resultado = self.add(nps.TitleFixedText, name="Resultado: ")
        self.xp_ganada = self.add(nps.TitleFixedText, name="Gana: ")
    def on_ok(self):
        usuario, nivel, experiencia, velocidad, vida, ataque = db.getLogedUserAndAvatar()
        maxExpNivel = 100 + (nivel*50)
        save.saveInFile(usuario)
        self.parentApp.getForm('PERFIL').usuario.value = usuario
        self.parentApp.getForm('PERFIL').ataque.value = str(ataque)
        self.parentApp.getForm('PERFIL').vida.value = str(vida)
        self.parentApp.getForm('PERFIL').velocidad.value = str(velocidad)
        self.parentApp.getForm('PERFIL').nivel.value = str(nivel)
        self.parentApp.getForm('PERFIL').xp = experiencia
        self.parentApp.getForm('PERFIL').experiencia.value = str(experiencia) + "/" + str(maxExpNivel)
        self.parentApp.change_form('PERFIL')

class PerfilAdmin(nps.FormBaseNew):
    def create(self):
        self.listaReportados = db.getReportados()
        self.usuario = self.add(nps.TitleFixedText, name="Bienvenido")
        self.add(nps.TitleFixedText, name="Lista de jugadores: ")
        if(len(self.listaReportados) == 0):
            self.add(nps.TitleFixedText, "No hay jugadores reportados")
        else:
            for r in self.listaReportados:
                self.add(nps.TitleFixedText, name=r[0]+" - Cantidad de reportes: "+str(r[1]))
        self.add(nps.ButtonPress, name="Banear jugador", when_pressed_function=self.ban)
        self.add(nps.ButtonPress, name="Cerrar sesión", when_pressed_function=self.close_session)
    def ban(self):
        # Mostrar nuevo form
        self.parentApp.change_form('BANEAR_ADMIN')
    def close_session(self):
        self.parentApp.change_form('MAIN')

class Banear(nps.ActionForm):
    def create(self):
        self.baneado = self.add(nps.TitleText, name="Ingrese el nombre del jugador que quiere banear: ")
    def on_cancel(self):
        self.parentApp.change_form('PERFIL_ADMIN')
    def on_ok(self):
        exists = db.userExists(self.baneado.value)
        if(exists):
            wasBanned = db.wasBanned(self.baneado.value)
            if wasBanned:
                nps.notify_wait("Ya ha sido baneado este jugador anteriormente, si aún aparece en la lista, se actualizará cuando cierres la aplicación", "Información")
            else:
                db.banear(self.baneado.value)
                nps.notify_wait("Usuario '" +self.baneado.value + "' baneado con éxito", "Información")
                PerfilAdmin.create
        else:
            nps.notify_wait("No existe el usuario ingresado", "Información")
        self.baneado.value = ""
        self.parentApp.change_form('PERFIL_ADMIN')


class ElBrutoApp(nps.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN',Login, name='El Bruto - Login')
        self.addForm('REGISTRO',Registro, name='El Bruto - Registro')
        self.addForm('PERFIL',Perfil,name="El Bruto - Perfil")
        self.addForm('REPORTAR',Reportar,name="El Bruto - Reportar")
        self.addForm('PELEA',Pelea,name="El Bruto - Pelea")
        self.addForm('PERFIL_ADMIN',PerfilAdmin,name="El Bruto (Administrador) - Perfil")
        self.addForm('BANEAR_ADMIN',Banear,name="El Bruto (Administrador) - Banear Jugador")
    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()


if __name__ == "__main__":
    #globals.initGlobals()
    #isLoged = db.logIn("neko", "1234")
    app = ElBrutoApp()
    app.run()