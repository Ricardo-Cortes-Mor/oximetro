# main.py
from machine import sleep, SoftI2C, Pin
from utime import ticks_diff, ticks_us, ticks_ms
from time import sleep_ms

from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import oled


def main():
    pa = oled.mostrar()
    #led_red= []
    ld_r=[]
    tmpo = []
    aux=[]
    
    # I2C software instance
    i2c = SoftI2C(sda=Pin(22),  # Here, use your I2C SDA pin
                  scl=Pin(21),  # Here, use your I2C SCL pin
                  freq=400000)  # Fast: 400kHz, slow: 100kHz

    # Examples of working I2C configurations:
    # Board             |   SDA pin  |   SCL pin
    # ------------------------------------------
    # ESP32 D1 Mini     |   22       |   21
    # TinyPico ESP32    |   21       |   22
    # Raspberry Pi Pico |   16       |   17
    # TinyS3			|	 8		 |    9

    # Sensor instance
    sensor = MAX30102(i2c=i2c)  # An I2C instance is required

    # Scan I2C bus to ensure that the sensor is connected
    if sensor.i2c_address not in i2c.scan():
        print("Sensor not found.")
        return
    elif not (sensor.check_part_id()):
        # Check that the targeted sensor is compatible
        print("I2C device ID not corresponding to MAX30102 or MAX30105.")
        return
    else:
        print("Sensor connected and recognized.")

    # It's possible to set up the sensor at once with the setup_sensor() method.
    # If no parameters are supplied, the default config is loaded:
    # Led mode: 2 (RED + IR)
    # ADC range: 16384
    # Sample rate: 400 Hz
    # Led power: maximum (50.0mA - Presence detection of ~12 inch)
    # Averaged samples: 8
    # pulse width: 411
    print("Setting up sensor with default configuration.", '\n')
    sensor.setup_sensor()

    # It is also possible to tune the configuration parameters one by one.
    # Set the sample rate to 400: 400 samples/s are collected by the sensor
    sensor.set_sample_rate(3200)
    # Set the number of samples to be averaged per each reading
    sensor.set_fifo_average(16)
    # Set LED brightness to a medium value
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)

    sleep(1)

    # The readTemperature() method allows to extract the die temperature in °C    
    print("Reading temperature in °C.", '\n')
    print(sensor.read_temperature())

    # Select whether to compute the acquisition frequency or not
    compute_frequency = True

    print("Starting data acquisition from RED & IR registers...", '\n')
    sleep(1)

    t_start = ticks_us()  # Starting time of the acquisition
    samples_n = 0  # Number of samples that have been collected
    cont=0
    while cont < 127:
        # The check() method has to be continuously polled, to check if
        # there are new readings into the sensor's FIFO queue. When new
        # readings are available, this function will put them into the storage.
        sensor.check()
        # Check if the storage contains available samples
        if sensor.available():
            t = ticks_ms()
            # Access the storage FIFO and gather the readings (integers)
            red_reading = sensor.pop_red_from_storage()
            #ir_reading = sensor.pop_ir_from_storage()
            ld_r.append(red_reading)
            tmpo.append(t)
            cont +=1
            if cont == 126:
                pa.graf(ld_r)
                #DETECTA LOS PICOS DE LA SEÑAL
                for i,j in enumerate(ld_r[:-1]):
                    if ld_r[i+1]-ld_r[i]<0 and ld_r[i]>ld_r[i-1]:
                        aux.append(ld_r.index(ld_r[i]))
                #DIFERENCIA DE TIEMPO ENTRE PICO Y PICO    
                for i in aux[:-1]:
                    dif_t = tmpo[i+i] - tmpo[i]         
                    if dif_t != 0:
                        bpm = 60 // (dif_t*1e-3)
                        print(tmpo[i+1],tmpo[i])
                        pa.pulso(sensor.read_temperature(),bpm)
                        sleep_ms(500)
                #
                ld_r=[]
                cont = 0
                
            
if __name__ == '__main__':
    main()