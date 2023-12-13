from time import sleep
import benchtop_stepper_motor as bsm
from _utils import ThorlabsConfiguration
from ctypes import byref
    

class ThorlabsController:
    """
    Thorlabs Gimbal Controller
    """
    
    def __init__(self):
        """
        Initialize parameters
        """
        self.total_steps_per_round = ThorlabsConfiguration.TOTAL_STEPS_PER_ROUND
        self.degrees_per_round = ThorlabsConfiguration.DEGREES_PER_ROUND
        self.serial_number = ThorlabsConfiguration.SERIAL_NUMBER
        self.channel = ThorlabsConfiguration.CHANNEL
        self.step_angle = ThorlabsConfiguration.STEP_ANGLE
        self.milliseconds = ThorlabsConfiguration.MILLISECONDS
        self.acceleration = ThorlabsConfiguration.ACCELERATION
        self.max_velocity = ThorlabsConfiguration.MAX_VELOCITY

    def connect(self):
        """
        Open the device for communications
        
        Returns:
            bool: True if connection established,
                  else False
        """
        if bsm.TLI_BuildDeviceList() == 0:
            if bsm.SBC_Open(self.serial_number) == 0:
                sleep(1)
                
                bsm.SBC_StartPolling(
                    self.serial_number, self.channel, self.milliseconds)
                bsm.SBC_ClearMessageQueue(self.serial_number, self.channel)
                print("Connect success")
                
                sleep(1)
                
                return True
            else:
                print("Connect Fail")
                
                return False
        else:
            print("Can't build device list.")
            
            return False

    def disconnect(self):
        """
        Disconnect and close the device
        """
        try:
            bsm.SBC_StopPolling(self.serial_number, self.channel)
            bsm.SBC_Close(self.serial_number)
            print("Disconnect and close the device")
            
        except:
            print("Failed to disconnect")

    def homing_parameters(self):
        """
        Get home parameters
        """
        if bsm.SBC_Open(self.serial_number, self.channel) == 0:
            homing_inf = bsm.MOT_HomingParameters()  # container

            print("Setting homing vel ", bsm.SBC_SetHomingVelocity(
                self.serial_number, self.channel, bsm.c_uint(50000000)))

            bsm.SBC_RequestHomingParams(self.serial_number, self.channel)
            err = bsm.SBC_GetHomingParamsBlock(
                self.serial_number, self.channel, byref(homing_inf))
            
            if err == 0:
                print("Direction: ", homing_inf.direction)
                print("Limit Sw: ", homing_inf.limitSwitch)
                print("Velocity: ", homing_inf.velocity)
                print("Offset Dist: ", homing_inf.offsetDistance)

            else:
                print(f"Error getting Homing Info Block. Error Code: {err}")

            power_inf = bsm.MOT_PowerParameters()  # container

            bsm.SBC_RequestPowerParams(self.serial_number, self.channel)
            
            err = bsm.SBC_GetPowerParams(
                self.serial_number, self.channel, byref(power_inf))
            
            if err == 0:
                print("Rest percentage: ", power_inf.restPercentage)
                print("Move percentage: ", power_inf.movePercentage)

            else:
                print(
                    f"Error getting Homing Info Block. Error Code: {err}")

    def home(self):
        """
        Set gimbal at home position only if
        not homed
        """
        is_home = (bsm.SBC_GetStatusBits(
            self.serial_number, self.channel) & 0x00000400)
        print("Is home nedded: ", is_home == 0)
        
        if is_home == 0:
            self._homing()
            
    def _homing(self):
        """
        Set gimbal homing
        """
        err = bsm.SBC_Home(self.serial_number, self.channel)
        sleep(1)
        
        if err == 0:
            bsm.SBC_StartPolling(
                self.serial_number, self.channel, self.milliseconds)
            bsm.SBC_ClearMessageQueue(self.serial_number, self.channel)
            sleep(0.2)
            
            while True:
                current_pos = self.get_position()
                
                if abs(current_pos) < ThorlabsConfiguration.ACCURACY:
                    print("Homimg completed")
                    break
                
                else:
                    print(f"Homing...{current_pos}")
                    
                sleep(1)
        else:
            print(f"Can't home. Err: {err}")
            
        # Wait to Idle state
        while not (bsm.SBC_GetStatusBits(self.serial_number, self.channel) == 0x80101400):
            sleep(0.2)
            
        # Sets the stage axis position limits
        bsm.SBC_SetStageAxisLimits(self.serial_number, self.channel, 0, 27033627)
        print("State: Idle")

    def set_jog_step_size_degrees(self):
        """
        Set jog step size

        Returns:
            int: status return code
        """
        return bsm.SBC_SetJogStepSize(self.serial_number, self.channel, round(self.step_angle * (self.total_steps_per_round / self.degrees_per_round)))

    def get_jog_step_size(self):
        """
        Get jog step size

        Returns:
            int: status return code 
        """
        return bsm.SBC_GetJogStepSize(self.serial_number, self.channel) * (self.degrees_per_round / self.total_steps_per_round)

    def get_device_unit_from_angle(self, angle):
        """
        Input degrees and return steps for gimbal

        Args:
            angle (float): angle value

        Returns:
            int: gimbal steps
        """
        return int(angle * (self.total_steps_per_round / self.degrees_per_round))

    def set_velocity_params(self, d_acceleration=10, d_max_velocity=10):
        """
        Set velocity parameters

        Args:
            d_acceleration (int, optional): Acceleration value. Defaults to 10.
            d_max_velocity (int, optional): Max Velocity value. Defaults to 10.

        Returns:
            int: status return code
        """
        if(bsm.SBC_SetVelParams(self.serial_number, self.channel, self.acceleration * d_acceleration, self.max_velocity * d_max_velocity) == 0):
            print("Set Velocity Params succeed")
            return 0
        else:
            print("Set Velocity Params failed")
            return -1

    def move_gimbal(self, angle):
        """
        Move the device to the specified position (index)

        Args:
            angle (float): Movement angle
        """
        err = bsm.SBC_Open(self.serial_number, self.channel)
        
        if err == 0:
            if (angle < self.get_position()):
                bsm.SBC_SetDirection(self.serial_number, self.channel, True)
            else:
                bsm.SBC_SetDirection(self.serial_number, self.channel, False)
                
            bsm.SBC_MoveToPosition(
                self.serial_number, self.channel, self.get_device_unit_from_angle(angle))
            print("Move to:", angle, end=' ', flush=True)
            
            # Wait to Idle state
            while not (bsm.SBC_GetStatusBits(self.serial_number, self.channel) == 0x80101400):
                print('.', end='', flush=True)
                sleep(1)
                
            print("\nStatus bits:", hex(bsm.SBC_GetStatusBits(
                self.serial_number, self.channel)), ",Stage angle:", self.get_position())
            print("State: Idle")

        sleep(1)

    def get_position(self):
        """
        Read gimbal current position

        Returns:
            int: gimbal position
        """
        bsm.SBC_RequestPosition(self.serial_number, self.channel)
        
        return bsm.SBC_GetPosition(self.serial_number, self.channel) * (self.degrees_per_round / self.total_steps_per_round)
