__author__ = 'cqt'

# Functions for checking conditions and running appropriate actions

from PyQt4 import QtCore, QtGui

# Base class for conditions check functions
class Condition():
    def __init__(self):
        value = 0.0
        pass

    def description(self):
        return "Always False"

    def set_param(self, value):
        self.value = value

    def check(self, data, var):
        return False

    def type(self):
        return "Histogram"

# Always true condition
class TrueCondition(Condition):
    def description(self):
        return "Always True"

    def check(self, data, var):
        return True


# Counter 1 less than
class LessThanCondition1(Condition):
    def description(self):
        return "Counter 2 average less than"

    def check(self, data, var):
        return (data.average[1] < var)

# Counter 0 less than
class LessThanCondition0(Condition):
    def description(self):
        return "Counter 1 average less than"

    def check(self, data, var):
        return (data.average[0] < var)

# Counter 1 after threshold is less than
class LessThanConditionTh(Condition):
    def description(self):
        return "Counter 2 after threshold is less than"

    def check(self, data, var):
        return (data.above_thr[1] < var)


# Counter 1 more than
class MoreThanCondition1(Condition):
    def description(self):
        return "Counter 2 average more than"

    def check(self, data, var):
        return (data.average[1] > var)

# Counter 0 more than
class MoreThanCondition0(Condition):
    def description(self):
        return "Counter 1 average more than"

    def check(self, data, var):
        return (data.average[0] > var)


class CamPixelITooHigh(Condition):
    def description(self):
        return "Camera pixel intensity more than"

    def check_cam(self, pixel_data, Inten):
        # print "Is intensity", pixel_data, "more than", Inten
        return (pixel_data > Inten)

    def type(self):
        return "Camera"


class CamPixelITooLow(Condition):
        def description(self):
            return "Camera pixel intensity less than"

        def check_cam(self, pixel_data, Inten):
            # print "Is intensity", pixel_data, "less than", Inten
            return pixel_data < Inten

        def type(self):
            return "Camera"

# Base class to do something if condition is met
# Derived class usually do some useful actions when one of the conditions is met
class Action(QtCore.QObject):
    def __init__(self):
         super(Action, self).__init__()

    @staticmethod
    def description():
        return "Do nothing"

    def act(self):
        pass

    # service functions for common actions
    def pause(self):
        self.emit(QtCore.SIGNAL("pauseActionRequest"))

    def crystallize(self):
        self.emit(QtCore.SIGNAL("crystallizeActionRequest"))

    def decreaseB(self):
        self.emit(QtCore.SIGNAL("decreaseBActionRequest"))

    def increaseB(self):
        self.emit(QtCore.SIGNAL("increaseBActionRequest"))


# Action class that pause the program
class PauseAction(Action):
    @staticmethod
    def description():
        return "Pause"

    def act(self):
        print "Pause triggered"
        self.pause()

# Pause, wait for 5 seconds and resume
class PauseFor5Sec(Action):
    def __init__(self):
        super(PauseFor5Sec, self).__init__()
        self.timer = QtCore.QTimer() # Timer to restart an experiment

    @staticmethod
    def description():
        return "Pause for 5 sec"

    def act(self):
        print "Pause triggered"
        self.pause()
        self.timer.singleShot(5000, self.resume)

    def resume(self):
        self.pause()
        print "Resuming"

# Action class that pauses the program and starts the crystallization sequence
class CrystallizeAction(Action):
    @staticmethod
    def description():
        return "Pause & Crystallize"

    def act(self):
        self.pause()
        self.crystallize()

# Action class that decreases the B field
class DecreaseBAction(Action):
    @staticmethod
    def description():
        return "Decrease B Field"

    def act(self):
        self.decreaseB()

class IncreaseBAction(Action):
    @staticmethod
    def description():
        return "Increase B Field"

    def act(self):
        self.increaseB()



# Dictionary of possible actions that we can do
ion_actions = {str(Action.description()) : Action(),
               str(PauseAction.description()) : PauseAction(),
               str(PauseFor5Sec.description()): PauseFor5Sec(),
               str(CrystallizeAction.description()) : CrystallizeAction(),
               str(DecreaseBAction.description()) : DecreaseBAction(),
               str(IncreaseBAction.description()) : IncreaseBAction()}

# List of all possible conditions we can check
ion_conditions = [Condition(), TrueCondition(),
                  LessThanCondition0(), LessThanCondition1(),
                  MoreThanCondition0(), MoreThanCondition1(),
                  LessThanConditionTh(), CamPixelITooHigh(),CamPixelITooLow()]