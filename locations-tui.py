import npyscreen



class Window(npyscreen.StandardApp):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        self.addForm("MAIN", LocationList, name="Locations Data")




class LocationList(npyscreen.ActionForm):
    def create(self):
        

    def on_ok(self):
        self.parentApp.setNextForm(None)

    def on_cancel(self):
        self.title.value = "Test"

app = Window()
app.run()
