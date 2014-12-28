"""
    Author: Bartosz Henryk Iwaniuk (b.iwaniuk@campus.tu-berlin.de)

    Class to interpolate values in a given impedance table, specifically for the HCZ-J3 Humidity Sensor
    For this example see: http://www.produktinfo.conrad.com/datenblaetter/1100000-1199999/001170516-da-01-en-FEUCHTIGKEITS_SENSOR_HCZ_J3A_N_.pdf
"""

import math

class HCZJ3translator:
    impedanceTable = [
        [20000.0, 20000.0, 9900.0, 4400.0, 1900.0, 810.0, 420.0, 211.0, 109.0, 63.0, 37.0, 22.0, 14.0, 9.0, 6.0, 4.0, 0.0],  # < 5 °C
        [20000.0, 20000.0, 9900.0, 4400.0, 1900.0, 810.0, 420.0, 211.0, 109.0, 63.0, 37.0, 22.0, 14.0, 9.0, 6.0, 4.0, 0.0],  # 5 °C
        [20000.0, 20000.0, 6900.0, 3100.0, 1400.0, 600.0, 300.0, 150.0, 83.0,  48.0, 28.0, 17.0, 12.0, 7.3, 4.8, 3.2, 0.0],  # 10 °C
        [20000.0, 20000.0, 4600.0, 2000.0, 900.0,  430.0, 220.0, 110.0, 62.0,  37.0, 22.0, 14.0, 9.4,  6.0, 3.9, 2.7, 0.0],  # 15 °C
        [20000.0,  7200.0, 3200.0, 1500.0, 670.0,  310.0, 160.0, 83.0,  48.0,  29.0, 18.0, 12.0, 7.8,  5.0, 3.3, 2.2, 0.0],  # 20 °C
        [20000.0,  5000.0, 2300.0,  920.0, 450.0,  220.0, 120.0, 66.0,  37.0,  23.0, 14.0, 9.6,  6.5,  4.2, 2.8, 1.9, 0.0],  # 25 °C
        [20000.0,  3600.0, 1700.0,  770.0, 360.0,  170.0, 90.0,  51.0,  29.0,  18.0, 12.0, 8.0,  5.5,  3.8, 2.5, 1.7, 0.0],  # 30 °C
        [20000.0,  2500.0, 1100.0,  530.0, 250.0,  130.0, 71.0,  40.0,  23.0,  15.0, 10.0, 6.8,  4.7,  3.3, 2.2, 1.5, 0.0],  # 35 °C
        [20000.0,  1800.0,  920.0,  430.0, 210.0,  96.0,  55.0,  31.0,  19.0,  12.0, 8.1,  5.8,  4.1,  2.9, 2.0, 1.4, 0.0],  # 40 °C
        [20000.0,  1300.0,  600.0,  280.0, 140.0,  74.0,  43.0,  25.0,  15.0,  10.3, 6.9,  4.9,  3.4,  2.4, 1.7, 1.2, 0.0],  # 45 °C
        [20000.0,  1100.0,  520.0,  250.0, 114.0,  61.0,  35.0,  20.0,  13.0,  8.7,  5.9,  4.3,  3.0,  2.0, 1.4, 1.1, 0.0],  # 50 °C
        [20000.0,  1100.0,  520.0,  250.0, 114.0,  61.0,  35.0,  20.0,  13.0,  8.7,  5.9,  4.3,  3.0,  2.0, 1.4, 1.1, 0.0]   # > 50 °C
        ]

    def __getLine (self, temp):
        return math.floor(min(max(temp, 0), 50) / 5.0)

    def __getTempRatio (self, temp):
        return (min(max(temp, 0), 50) / 5.0) % 1

    def __getImpedanceRatio (self, impedance, line, anker):
        return (impedance - self.impedanceTable[line][anker]) / (self.impedanceTable[line][anker-1] - self.impedanceTable[line][anker])

    def __getAnker (self, line, impedance):
        anker = 16
        for i in range(0, 16):
            if impedance >= self.impedanceTable[line][15-i]:
                anker = 15-i
            else:
                break
        return anker

    def getRH (self, temp, impedance):
        """
        :param temp: Environmental temperature as given by temp sensor
        :param impedance: impedance calculated form sensor output
        :return: Relative humidity based on interpolated reference values.
        """
        impedance = min(max(impedance, 0), 20000)
        tempRatio = self.__getTempRatio(temp)
        line = self.__getLine(temp)
        anker1 = self.__getAnker(line, impedance)
        anker1_RH = 15 + (anker1 * 5)  # 5% RH is one step in the impedance table
        anker2 = self.__getAnker(line+1, impedance)
        anker2_RH = 15 + (anker2 * 5)
        ratio1 = self.__getImpedanceRatio(impedance, line, anker1)
        ratio1_RH = anker1_RH - (5 * ratio1)
        ratio2 =  self.__getImpedanceRatio(impedance, line+1, anker1)
        ratio2_RH = anker2_RH - (5 * ratio2)

        return ratio2_RH * tempRatio + ratio1_RH * (1 - tempRatio)


Sensor = HCZJ3translator()
print(Sensor.getRH(5, 1900))
print(Sensor.getRH(7.5, 700))
print(Sensor.getRH(20, 7200))
print(Sensor.getRH(50, 1.1))
print(Sensor.getRH(25, 23))
