import sys
import os
import newmark.gclib as gclib


sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

# constants
TOTAL_STEPS_PER_ROUND = 3600000
DEG_PER_ROUND = 360
BAUDRATE = 19200


class NewmarkController:
    """
    Newmark Gimbal Controller
    """
    
    def __init__(self):
        """
        Initialize parameters
        """
        self.g = gclib.GController()

        self.__gimbal_steps_ratio = int(TOTAL_STEPS_PER_ROUND / DEG_PER_ROUND)

    def get_device_unit_from_angle(self, angle):
        """
        Input degrees and return steps for gimbal

        Args:
            angle (float): angle value

        Returns:
            str: gimbal steps
        """
        return str(int(angle * self.__gimbal_steps_ratio))

    def home(self):
        """
        Set gimbal homing
        """
        c = self.g.GCommand  # alias the command callable
        print('Homing ...')
        c('HM; BG')  # Homing
        self.g.GMotionComplete('AB')
        c('DP 0,0')  # set Home as 0,0
        print('Homimg Done')
        
        del c  # delete the alias

    def connect(self):
        """
        Connect to gimbal
        
        Returns:
            bool: True if connection established,
                  else False
        """
        try:
            available = self.g.GAddresses()
            
            for a in sorted(available.keys()):
                port = a
                
                try:
                    self.g.GOpen(f'-a {port} -b {BAUDRATE} -s ALL')
                    
                    return True
                except:
                    pass
                
            return False
        except gclib.GclibError as e:
            print(f'Unexpected GclibError: {e}')
            self.g.GClose()  # close connections!
            
            return False

    def disconnect(self):
        """
        Disconnect from gimbal
        """
        try:
            self.g.GClose()  # close connections!
            
        except:  # if already closed/disconnected due to timeout
            pass

    def setup(self):
        """
        Config the motor
        """
        self.connect()
        
        try:
            c = self.g.GCommand  # alias the command callable
            # configures the polarity of the limit switches, home switches
            c('CN 0,0,0,0,0')
            c('SP 50000,50000')  # speed, 50000 cts/sec
            c('AC 25000,25000')  # acceleration, 50000 cts/sec^2
            print('Config Motor - limits, accelerations, speead')
            current_position = c('DE ?,?')
            
            if current_position == '0, 0':
                self.home()
                
            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Unexpected GclibError: {e}')
            self.g.GClose()  # close connections!
            
            raise

    def get_position(self):
        """
        Read gimbal current position

        Returns:
            tuple: x, y position
        """
        c = self.g.GCommand  # alias the command callable
        output = c('DE ?,?')
        xy = [pos.lstrip() for pos in output.split(',')]
        
        return int(xy[0]) / self.__gimbal_steps_ratio, int(xy[1]) / self.__gimbal_steps_ratio

    def move_gimbal(self, axis, angle, rel_or_abs):
        """
        Move gimbal absolute

        Args:
            axis (str): Movement axis (X/Y)
            angle (float): Movement angle
            rel_or_abs (str): 'R' for relative and 'A' for absolute
        """
        try:
            c = self.g.GCommand  # alias the command callable
            
            if axis == 'X':
                cmd = f'P{rel_or_abs} {self.get_device_unit_from_angle(angle)};BGA'
                
            elif axis == 'Y':
                cmd = f'P{rel_or_abs} ,{self.get_device_unit_from_angle(angle)};BGB'
                
            print(f'Moving axis {axis} to {angle}; ({cmd})')
            c(cmd)  # absolute motion move
            self.g.GMotionComplete('AB')
            print('Motion Done')
            
            del c  # delete the alias
        except gclib.GclibError as e:
            print(f'Unexpected GclibError: {e}')
            self.g.GClose()  # close connections!
            
            raise
