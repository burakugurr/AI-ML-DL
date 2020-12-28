from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.lang import Builder
######################

__author__ = "Burak Ugur"
__copyright__ = "Copyright 2020, The ML Project"
__credits__ = ["Burak Ugur"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Burak Ugur"
__email__ = "burak.ugur@hacettepe.edu.tr"
__status__ = "Learning"
######################


class phone(GridLayout):
    def __init__(self,**kwargs):
        super(phone,self).__init__(**kwargs)
        self.cols=2

        self.batary = Label(text="Batarya Gücü: ")
        self.add_widget(self.batary)
        self.bataryInput = TextInput(multiline=False)
        self.add_widget(self.bataryInput)
        print(self.bataryInput.text)
        self.blue = Label(text="Bluetooth Var Mı? [1] Evet [0] Hayır ")
        self.add_widget(self.blue)
        self.blueInput = TextInput(multiline=False)
        self.add_widget(self.blueInput)

        self.cs = Label(text="Mikroişlemcinin yürütme hızı ?")
        self.add_widget(self.cs)
        self.csInput = TextInput(multiline=False)
        self.add_widget(self.csInput)

        self.ds = Label(text="Çift Sim Desteği Var mı ?")
        self.add_widget(self.ds)
        self.dsInput = TextInput(multiline=False)
        self.add_widget(self.dsInput)

        self.fc = Label(text="Ön Kamera kaç mp ? ")
        self.add_widget(self.fc)
        self.fcInput = TextInput(multiline=False)
        self.add_widget(self.fcInput)

        self.four_g = Label(text="4g Destekliyor mu ? [1] Evet [0] Hayır ")
        self.add_widget(self.four_g)
        self.four_gInput = TextInput(multiline=False)
        self.add_widget(self.four_gInput)

        self.int_memory = Label(text="Kaç GB dahili hafızası var ? ")
        self.add_widget(self.int_memory)
        self.int_memoryInput = TextInput(multiline=False)
        self.add_widget(self.int_memoryInput)

        self.m_dep = Label(text="Telefon kalınlığı ? ")
        self.add_widget(self.m_dep)
        self.m_depInput = TextInput(multiline=False)
        self.add_widget(self.m_depInput)

        self.mobile_wt = Label(text="Telefon ağırlığı ? ")
        self.add_widget(self.mobile_wt)
        self.mobile_wtInput = TextInput(multiline=False)
        self.add_widget(self.mobile_wtInput)

        self.n_cores = Label(text="İşlemci çerkidek sayısı ? ")
        self.add_widget(self.n_cores)
        self.n_coresInput = TextInput(multiline=False)
        self.add_widget(self.n_coresInput)

        self.pc = Label(text="Arka Kamera kaç mp ? ")
        self.add_widget(self.pc)
        self.pcInput = TextInput(multiline=False)
        self.add_widget(self.pcInput)

        self.px_height = Label(text="Telefon yükseklik ? ")
        self.add_widget(self.px_height)
        self.px_heightInput = TextInput(multiline=False)
        self.add_widget(self.px_heightInput)

        self.px_width = Label(text="Telefon genişlik ? ")
        self.add_widget(self.px_width)
        self.px_widthInput = TextInput(multiline=False)
        self.add_widget(self.px_widthInput)

        self.ram = Label(text="Telefon RAM boyutu ? ")
        self.add_widget(self.ram)
        self.ramInput = TextInput(multiline=False)
        self.add_widget(self.ramInput)

        self.sc_h = Label(text="Telefon ekran yüksekliği ? ")
        self.add_widget(self.sc_h)
        self.sc_hInput = TextInput(multiline=False)
        self.add_widget(self.sc_hInput)

        self.sc_w = Label(text="Telefon ekran genişliği ? ")
        self.add_widget(self.sc_w)
        self.sc_wInput = TextInput(multiline=False)
        self.add_widget(self.sc_wInput)

        self.talk_time = Label(text="Telefon konuşma süresi ? ")
        self.add_widget(self.talk_time)
        self.talk_timeInput = TextInput(multiline=False)
        self.add_widget(self.talk_timeInput)

        self.three_g = Label(text="Telefon 3G destekliyor mu ? [1] Evet [0] Hayır")
        self.add_widget(self.three_g)
        self.three_gInput = TextInput(multiline=False)
        self.add_widget(self.three_gInput)

        self.touch_screen = Label(text="Telefon dokunmatik mi ? [1] Evet [0] Hayır")
        self.add_widget(self.touch_screen)
        self.touch_screenInput = TextInput(multiline=False)
        self.add_widget(self.touch_screenInput)

        self.wifi = Label(text="Telefonda wifi var mi ? [1] Evet [0] Hayır")
        self.add_widget(self.wifi)
        self.wifiInput = TextInput(multiline=False)
        self.add_widget(self.wifiInput)
        print(type(self.wifiInput))
                ############### add BUTTON

        self.button = Button(text='Fiyatını tahmin et',
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5})
        self.button.bind(on_press=self.on_press_button)
        self.add_widget(self.button)

    def popUp(self,value):
        popupWindow = Popup(title="Predict Window", content=Label(text=("Girilen telefon tahminen "+str(value)+" dır"),size_hint=(None, None), size=(400, 400)))
        content = Button(text='Close me!')
        content.bind(on_press=popupWindow.dismiss)
        popupWindow.open()

    def on_press_button(self, instance):
        import pred
        model = pred.get_model('mobclass.pkl')
        data = pred.get_value(self.bataryInput, self.blueInput,self.csInput,self.dsInput,self.fcInput,self.four_gInput,
                              self.int_memoryInput,self.m_depInput,self.mobile_wtInput,
                              self.n_coresInput,self.pcInput, self.px_heightInput,self.px_widthInput, self.ramInput, self.sc_hInput,
                              self.sc_wInput, self.talk_timeInput, self.three_gInput,self.touch_screenInput, self.wifiInput)
        # predict model
        predictVal = pred.get_predict(model,data)
        if(predictVal==0):
            predictVal="Düşük Fiyatlı"
        if(predictVal==1):
            predictVal = "Orta Fiyatlı"
        if(predictVal==2):
            predictVal = "Yüksek Fiyatlı"
        if(predictVal==3):
            predictVal = "Çok Yüksek Fiyatlı"
        # if you want follow value uncomment this rows
        #print(predictVal)
        phone.popUp(self=None,value=predictVal)



class MainApp(App):
    def build(self):
        return phone()




if __name__ == '__main__':
    app = MainApp()
    app.run()