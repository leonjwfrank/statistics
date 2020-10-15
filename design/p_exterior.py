"""
通过一些仪表盘和控件，engineer，工程师可以调整控制系统背后的复杂系统，保持系统允许，隐藏系统背后的复杂性
compiler 模块词法分析器，解析器，ast树生成器等外观
"""
# 5,结构化-外观模式

import time


class Engine(object):
    """An Engine class 发动机"""

    def __init__(self, name, bhp, rpm, volume, cylinders=4.0, type='petrol'):
        self.name = name
        self.bhp = bhp
        self.rpm = rpm
        self.volume = volume
        self.cylinders = cylinders
        self.type = type
        self.status = 0

    def __str__(self):
        return f"<{self.__class__.__name__} info:{self.__dict__}>"

    def start(self):
        """Start-up the engine"""
        print(f"Engine started")
        self.status = 1

    def stop(self):
        """Stop the engine"""
        print('Engine stopped')
        self.status = 0


class Transmission(object):
    """Transmission class  传输控制，转动控制"""

    def __init__(self, gears, torque):
        self.gears = gears
        self.torque = torque
        # start with neutral
        self.gear_pos = 0

    def __str__(self):
        return f"<{self.__class__.__name__} gears:{self.gears}, torque:{self.torque}, gear_pos:{self.gear_pos}>"

    def shift_up(self):
        """Shift up gears"""
        if self.gear_pos == self.gears:
            print('Can not shift up anymore')
        else:
            self.gear_pos += 1
            print(f"Shifted up to gear", self.gear_pos)

    def shift_down(self):
        """Shift down gears"""
        if self.gear_pos == -1:
            print(f"In reverse, can not shift down")
        else:
            self.gear_pos -= 1
            print('Shifted down to gear', self.gear_pos)

    def shift_reverse(self):
        """Shift in reverse 齿轮逆转"""
        print('Reverse shifting')
        self.gear_pos = -1

    def shift_to(self, gear):
        """Shift to a gear position 齿轮到变速位"""
        self.gear_pos = gear
        print('Shifted to gear', self.gear_pos)


# 其他子系统，如刹车，泊车，轮子，悬架，框架等
class Brake(object):
    """刹车类 A brake class"""

    def __init__(self, number, type='disc'):
        self.type = type
        self.number = number

    def __str__(self):
        return f"<{self.__class__.__name__}:type:{self.type}, number:{self.number}>"

    def engage(self):
        """Engage the break"""
        print(f"{self.__class__.__name__} {self.number} engaged!")

    def release(self):
        """Release the break"""
        print(f"{self.__class__.__name__} {self.number} released")


class ParkingBrake(Brake):
    """A parking brake class"""

    def __init__(self, type='drum'):
        super(ParkingBrake, self).__init__(type=type, number=1)

    def __str__(self):
        return f"{self.__dict__}"


class Suspension(object):
    """A suspension class"""

    def __init__(self, load, type='mcpherson'):
        self.type = type
        self.load = load


class Wheel(object):
    """A Wheel class"""

    def __init__(self, meterial, diameter, pitch):
        self.meterial = meterial
        self.diameter = diameter
        self.pitch = pitch


class WheelAssembly(object):
    """A wheel class"""

    def __init__(self, brake, suspension):
        self.brake = brake
        self.suspension = suspension
        self.wheels = Wheel('alloy', 'M12', 1.25)

    def apply_brakes(self):
        """Apply brakes"""
        print(f"Apply brakes")
        self.brake.engage()


class Frame(object):
    """A frame class for an automobile"""

    def __init__(self, length, width):
        self.length = length
        self.width = width

    def __str__(self):
        return f"<{self.__class__.__name__} length:{self.length}, width:{self.width}>"


# Car 类 组合子系统
class Car(object):
    """A car building with many sub system"""

    def __init__(self, model, manufacturer):
        self.engine = Engine('Maruti', 'K-series', 85, 5000, cylinders=1.3)
        self.frame = Frame(385, 170)
        self.wheel_assemblies = []
        for i in range(4):
            self.wheel_assemblies.append(WheelAssembly(Brake(i + 1), Suspension(1000)))
        self.transmission = Transmission(5, 115)
        self.model = model
        self.manufacturer = manufacturer
        self.park_brake = ParkingBrake()
        # Ignition engaged
        self.ignition = False
        self.status = None

    # @property
    # def status(self):
    #     return self._status
    #
    # @status.setter
    # def status(self, s):
    #     self._status = s

    def __str__(self):
        return f"{self.__class__.__name__} engine:{self.engine}, frame:{self.frame}, transmission:{self.transmission}, park_brake:{str(self.park_brake)}"

    def start(self):
        """Start the car"""
        print('Starting the car')
        self.ignition = True
        self.park_brake.release()
        self.engine.start()
        self.transmission.shift_up()
        print('Car started')
        self.status = self.engine.status

    def stop(self):
        """Stop the car"""
        print(f"Stopping the car")
        # Apply brakes to reduce speed
        for wheel_a in self.wheel_assemblies:
            wheel_a.apply_brakes()
        # Move to 2nd gear and then 1st
        self.transmission.shift_to(2)
        self.transmission.shift_to(1)
        self.engine.stop()
        # Shift to neutral
        self.transmission.shift_to(0)
        # Engage parking brake
        self.park_brake.engage()
        print("Car stopped")
        self.status = self.engine.status


if __name__ == '__main__':
    car_bc = Car('Swift', 'Suzuki')
    print(f"car_bc:{car_bc}")
    car_bc.start()
    print(f"car status:{car_bc.status}")

    print(f"started car:{car_bc}")
    car_bc.stop()
    print(f"car status:{car_bc.status}")
    print(f"stopped car:{car_bc}")
