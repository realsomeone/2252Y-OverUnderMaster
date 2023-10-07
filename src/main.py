# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       arnaldoalicea                                                #
# 	Created:      9/5/2023, 4:10:45 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #
# region --------conf--------
# Library imports
from vex import *
auton = '' # selección de autonomo fisico :)

# Brain should be defined by default
brain=Brain()

frontleft = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
frontright = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
backleft = Motor(Ports.PORT3,GearSetting.RATIO_6_1,True)
backright = Motor(Ports.PORT4,GearSetting.RATIO_6_1,False)
rightside = MotorGroup(frontright,backright)
leftside = MotorGroup(frontleft,backleft)
intake = Motor(Ports.PORT5,GearSetting.RATIO_18_1,True)
catapult = Motor(Ports.PORT6,GearSetting.RATIO_18_1,False)
wings1 = DigitalOut(brain.three_wire_port.a)
wings2 = DigitalOut(brain.three_wire_port.b)
catsens = Limit(brain.three_wire_port.c)
autonSel = Optical(Ports.PORT9)
matchload = Motor(Ports.PORT8,GearSetting.RATIO_18_1,False)

player=Controller()

def wings(exp=True):
  wings1.set(exp)
  wings2.set(exp)
def windup():
  catapult.spin(FORWARD)
  while not catsens.pressing():
    wait(5,MSEC)
  catapult.stop()
  catapult.spin_for(FORWARD,1/8,TURNS,wait=True)
def release():
  catapult.spin(FORWARD)
  while catsens.pressing():
    wait(5,MSEC)
  catapult.stop()
def detectAuton():
  autonSel.set_light(LedStateType.ON)
  autonSel.set_light_power(50)
  wait(200,MSEC)
  if autonSel.is_near_object():
      color = autonSel.brightness()
      if color >= 10:
          brain.screen.print("defen\n")
          tmp = "defen"
      elif color < 10:
          brain.screen.print("offen\n")
          tmp = 'offen'
  else:
      brain.screen.print("nada\n")
      tmp = ''
  autonSel.set_light(LedStateType.OFF)
  return tmp
def setup(value=0):
  if value == 1:
    global auton
    rightside.set_velocity(50,PERCENT)
    leftside.set_velocity(50,PERCENT)
    auton = detectAuton()
  else: 
    intake.set_velocity(100,PERCENT)#inital values de motores y whatnot
  wings(False)
  catapult.set_velocity(100,PERCENT)
# endregion
# region --------driver Funcs---------
def joystickfunc():
  leftside.spin(FORWARD)
  rightside.spin(FORWARD)
  while True:
    leftside.set_velocity(player.axis3.position()+player.axis1.position(),PERCENT)
    rightside.set_velocity(player.axis3.position()-player.axis1.position(),PERCENT)
    wait(5,MSEC)
def intakefunc():
  intake.set_velocity(100,PERCENT)
  while True:
    if player.buttonL2.pressing():
      intake.spin(FORWARD)
    elif player.buttonL1.pressing():
      intake.spin(REVERSE)
    else:
      intake.stop()
def loadfunc():
  matchload.set_velocity(50,PERCENT)
  while True:
    if player.buttonLeft.pressing():
      matchload.spin(FORWARD)
    elif player.buttonRight.pressing():
      matchload.spin(REVERSE,0.7,Turns)
    else:
      matchload.stop()
def laCATAPULTA():
  while True:
    while not player.buttonR2.pressing():
      wait(5,MSEC)
    if catsens.pressing():
      release()
    else:
      windup()
    while player.buttonR2.pressing():
      wait(5,MSEC)
def wingManager():
  while True:
    if player.buttonR1.pressing():
      wings(True)
      while player.buttonR1.pressing():
        wait(10,MSEC)
      wings(False)
    wait(10,MSEC)
def matchLoad():
  while True:
    while not player.buttonUp.pressing():
      wait(5,MSEC)
    catapult.spin(FORWARD)
    while player.buttonUp.pressing():
      wait(5,MSEC)
    catapult.stop()
# endregion
# region --------auton funcs----------
def move(dis=float(24)):
  factor=5.5
  leftside.spin_for(FORWARD,dis/factor,TURNS,wait=False)
  rightside.spin_for(FORWARD,dis/factor,TURNS,wait=True)
  wait(5,MSEC)
def turn(theta=90):
  rightside.set_velocity(30,PERCENT)
  leftside.set_velocity(30,PERCENT)
  factor=48
  leftside.spin_for(FORWARD,theta/factor,TURNS,wait=False)
  rightside.spin_for(REVERSE,theta/factor,TURNS,wait=True)
  rightside.set_velocity(50,PERCENT)
  leftside.set_velocity(50,PERCENT)
  wait(5,MSEC)
def autonTime():
  setup(1)
  if auton == 'offen':
    intake.spin_for(FORWARD,0.5,TURNS,wait=False)
    move(48)
    turn(90)
    intake.spin_for(REVERSE,1.5,TURNS,wait=False)
    wait(100,MSEC)
    move(9.4)
    intake.stop() 
    move(-29)
    wings1.set(True)
    wait(200,MSEC)
    rightside.set_velocity(75,PERCENT)
    leftside.set_velocity(75,PERCENT)
    move(28)
    wait(10,MSEC)
    rightside.set_velocity(50,PERCENT)
    leftside.set_velocity(50,PERCENT)
    wings1.set(False)
    move(-4.5)
    turn(90)
    move(46)
    turn(90)
    move(26)
    intake.spin_for(FORWARD,4,TURNS,wait=True)
    wait(15,MSEC)
    turn(-15)
    move(-1)
    catapult.spin_for(FORWARD,0.5,TURNS,wait=False)
  elif auton == 'defen':
    intake.spin_for(FORWARD,0.5,TURNS,wait=False)
    move(48)
    turn(-90)
    intake.spin_for(REVERSE,1,TURNS,wait=False)
    wait(100,MSEC)
    intake.stop()
    move(6)
    wait(100,MSEC)
    move(-25)
    turn(47)
    intake.spin_for(FORWARD,6,TURNS,wait=False)
    move(5)
    wait(100,MSEC)
    move(-5)
    turn(-45)
    wait(500,MSEC)
    catapult.spin_for(FORWARD,1,TURNS,wait=False)
    wait(100,MSEC)
    windup()
    turn(130)
    intake.spin_for(FORWARD,6,TURNS,wait=False)
    move(5)
    wait(100,MSEC)
    move(-5)
    turn(-130)
    wait(500,MSEC)
    catapult.spin_for(FORWARD,0.5,TURNS,wait=False)
    

    

  else:
    pass
# endregion 
# region ------comp funcs---------
def startDrivers():
  setup(1)
  driverTime.broadcast()
def autoF():
  active = Thread(autonTime)
  while (comp.is_autonomous() and comp.is_enabled()):
    wait(10,MSEC)
  active.stop()
def drivF():
  active = Thread(startDrivers)
  while (comp.is_driver_control() and comp.is_enabled()):
    wait(10,MSEC)
  active.stop()
# endregion
driverTime = Event()
comp = Competition(drivF,autoF)
driverTime(joystickfunc)
driverTime(intakefunc)
driverTime(wingManager)
driverTime(laCATAPULTA)
driverTime(matchLoad)
driverTime(loadfunc)
wait(15,MSEC)

setup()