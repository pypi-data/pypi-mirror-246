from abc import ABC, abstractmethod


class GimbalAbstract(ABC):
    @abstractmethod
    def set_gimbal_home(self):
        pass
    
    @abstractmethod
    def connect_gimbal(self):
        pass
    
    @abstractmethod
    def disconnect_gimbal(self):
        pass

    @abstractmethod
    def setup_configs(self):
        pass
    
    @abstractmethod
    def get_position(self):
        pass
    
    @abstractmethod
    def move_gimbal_abs(self, axis: str, angle: float):
        pass
    
    @abstractmethod
    def move_gimbal_rel(self, axis: str, angle: float):
        pass