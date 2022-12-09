from machine  import Pin, SoftI2C #SoftI2C
import ssd1306

i2c = SoftI2C(sda=Pin(22), scl=Pin(21), freq=400000)
oled_col = 128
oled_fil = 64
oled = ssd1306.SSD1306_I2C(oled_col, oled_fil, i2c)
'''
oled_col1= 128
lis=[]
for i in range(oled_col1):
    lis.append(i*22)
'''  
class mostrar():
    
    #VALORES INICIALES APREGADOS DE ACUERDO AL TAMANO DE LA OLED
    def __init__(self, li=60, ls=15, maxi=None):
        dat=[]
        self.li = li
        self.ls = ls
        self.maxi = maxi
    
    def pulso(self, temp,bpm):
        oled.fill(0)
        
        self.temp=temp
        self.bpm=bpm
        tex1 = 'T:{:.1f} C'.format(self.temp)
        tex2 = 'BPM:{}'.format(self.bpm)
        oled.text(tex1, 0, 0)
        oled.text(tex2, 80, 0)
        oled.show()
    
    def graf(self, l):
        dat = l
        self.maxi = max(dat)
        self.mini = min(dat)
        self.dif = self.maxi-self.mini
        for c,v in enumerate(dat):
            dat[c]=dat[c]-self.mini
            #OPERACION PARA HACER EL MAPEO EN LA PANTALLA OLED DE 64 X 128
            dat[c] = abs(( dat[c]*(self.li-self.ls)) // self.dif - self.li)
            
        #for j in range(127,0,-1):
        for j in range (len(dat)):
            oled.pixel(j, dat[j], 1)
            oled.show()
  
            
'''
ej=mostrar()
ej.graf(lis)
ej.pulso(223,34*3)
'''
    
