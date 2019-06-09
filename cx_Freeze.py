import cx_Freeze
from cx_Freeze import *

setup(
        name = "hello",
        options={"build_exe": {"packages":["pygame"],
                               "included_files":["UFO.bmp","UFO_Monster.bmp","boss_Atack.jpg","boss.png","background_1.png","bullet.png","boom.png","shot.wav","explosion.wav","mybgm.wav","D2coding.ttf","Meteor.png"]}},
        version = "0.1",
        executables = [
    cx_Freeze.Executable('Main.py'),
    cx_Freeze.Executable('Boss_class.py'),
    cx_Freeze.Executable('Boss_class_Attack.py'),
    cx_Freeze.Executable('Meteor.py'),
    cx_Freeze.Executable('UFO_class.py'),
    cx_Freeze.Executable('UFO_Monster.py')
    ]
)
