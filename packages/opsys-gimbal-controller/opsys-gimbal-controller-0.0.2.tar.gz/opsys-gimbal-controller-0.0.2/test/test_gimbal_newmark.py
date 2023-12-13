import unittest
from unittest.mock import patch, MagicMock
from opsys_gimbal_controller.gimbal_controller import GimbalController


GIMBAL_TYPE = 'Newmark'


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(GimbalController, 'connect_gimbal')
    def test_connect_gimbal(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        gimbal.connect_gimbal()
        gimbal_mock.assert_called_once_with()

    @ patch.object(GimbalController, 'disconnect_gimbal')
    def test_disconnect_gimbal(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        gimbal.disconnect_gimbal()
        gimbal_mock.assert_called_once_with()

    @ patch.object(GimbalController, 'setup_configs')
    def test_setup_configs(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        gimbal.setup_configs()
        gimbal_mock.assert_called_once_with()

    @ patch.object(GimbalController, 'get_position')
    def test_get_position(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        gimbal.get_position()
        gimbal_mock.assert_called_once_with()

    @ patch.object(GimbalController, 'set_gimbal_home')
    def test_set_gimbal_home(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        gimbal.set_gimbal_home()
        gimbal_mock.assert_called_once_with()

    @ patch.object(GimbalController, 'move_gimbal_abs')
    def test_move_gimbal_abs(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        angle = 50
        gimbal.move_gimbal_abs(axis=axis, angle=angle)
        gimbal_mock.assert_called_once_with(axis='X', angle=50)

    @ patch.object(GimbalController, 'move_gimbal_rel')
    def test_move_gimbal_rel(self, gimbal_mock: MagicMock):
        gimbal = GimbalController(motor_type=GIMBAL_TYPE)
        axis = 'X'
        angle = 50
        gimbal.move_gimbal_rel(axis=axis, angle=angle)
        gimbal_mock.assert_called_once_with(axis='X', angle=50)


if __name__ == '__main__':
    unittest.main()
