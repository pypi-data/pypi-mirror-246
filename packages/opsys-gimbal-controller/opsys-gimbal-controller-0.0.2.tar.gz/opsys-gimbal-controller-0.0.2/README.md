# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is gimbal controller implementation for Newmark/Thorlabs gimbals with ATEN RS-232 to USB adapter

### How do I get set up? ###

* pip install opsys-gimbal-controller

### Unit Testing

* python -m unittest -v

### Pyinstaller

* Directories containing DLLs should be imported by pyinstaller during executable generation.
* The following functionality should be added inside pyinstaller spec file:
```
def get_dirs(root_folder, hint):
    target_dirs = []
    for root, dirs, files in os.walk(root_folder):
        for dir in dirs:
            if '.env' in os.path.join(root, dir) and hint in dir:
                target_dirs.append(os.path.join(root, dir))
    return target_dirs

root_folder_path = os.getcwd()
# same to be done with thorlabs, if required
dirs = get_dirs(root_folder_path, 'newmark')
datas_dirs = [(f'{_dir}\*', './opsys_gimbal_controller/newmark/') for _dir in dirs]
```
* ```datas_dirs``` should be added at ```datas``` variable:
```
pathex=[],
binaries=binaries_file,
datas=datas_dirs,
```

### Usage Example
```
from opsys_gimbal_controller.gimbal_controller import GimbalController

gimbal = GimbalController(motor_type="Newmark")

gimbal.connect_gimbal()
gimbal.setup_configs()
gimbal.set_gimbal_home()
gimbal.move_gimbal_abs(axis='X', angle=-30)
gimbal.disconnect_gimbal()
```