from .gimbal_abstract import GimbalAbstract
from .gimbal_types import GimbalTypes


class GimbalController(GimbalAbstract):
    """
    Gimbal Controller main class
    """
    
    def __init__(self, motor_type):
        """
        Initialize parameters

        Args:
            motor_type (str): gimbal motor type
        """
        self.motor_type = motor_type
        self.gimbal = None  # gimbal connection

    def connect_gimbal(self):
        """
        Connect to Gimbal

        Raises:
            Exception: in case unregistered motor type passed
            
        Returns:
            object: device connection instance
        """
        if self.motor_type.upper() == GimbalTypes.NEWMARK:
            from .newmark.newmark_controller import NewmarkController
            
            self.gimbal = NewmarkController()
            
        elif self.motor_type.upper() == GimbalTypes.THORLABS:
            from .thorlabs.thorlabs_controller import ThorlabsController
            
            self.gimbal = ThorlabsController()
            
        elif self.motor_type.upper() == GimbalTypes.MANUF:
            return
        
        else:
            raise ValueError("Can't find motor type")
        
        return self.gimbal.connect()

    def disconnect_gimbal(self):
        """
        Disconnect from Gimbal
        """
        self.gimbal.disconnect()

    def setup_configs(self):
        """
        Initialize Gimbal configuration
        """
        # Thorlabs initialized at class instance
        if self.motor_type.upper() == GimbalTypes.NEWMARK:
            self.gimbal.setup()

    def get_position(self):
        """
        Get Gimbal position

        Returns:
            tuple: x, y position
        """
        if self.motor_type.upper() == GimbalTypes.NEWMARK:
            x, y = self.gimbal.get_position()
            
        elif self.motor_type.upper() == GimbalTypes.THORLABS:
            y = 0  # single axis
            x = self.gimbal.get_position()
            
        return x, y

    def set_gimbal_home(self):
        """
        Gimbal Homing
        """
        self.gimbal.home()

    def move_gimbal_abs(self, axis, angle):
        """
        Move Gimbal absolute

        Args:
            axis (str): Movement axis (X/Y)
            angle (float): Movement angle
        """
        if self.motor_type.upper() == GimbalTypes.NEWMARK:
            self.gimbal.move_gimbal(axis, angle, 'A')  # A = Absolute
            
        elif self.motor_type.upper() == GimbalTypes.THORLABS:
            self.gimbal.move_gimbal(angle)

    def move_gimbal_rel(self, axis, angle):
        """
        Move Gimbal relative

        Args:
            axis (str): Movement axis (X/Y)
            angle (float): Movement angle
        """
        if self.motor_type.upper() == GimbalTypes.NEWMARK:
            self.gimbal.move_gimbal(axis, angle, 'R')  # R = Relative
            
        elif self.motor_type.upper() == GimbalTypes.THORLABS:
            self.gimbal.move_gimbal(angle)
