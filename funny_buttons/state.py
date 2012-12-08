
class Door(object):
    pass

class Context(object):
    def __init__(self):
        self.state = CloseState()
        self.door = Door()
    
    def set_state(self, state):
        self.state = state

    def action(self):
        self.state.action(self, self.door)

class DoorState(object):
    pass

class OpenState(DoorState):
    def action(self, context, door):
        self.open(door)
        context.set_state(CloseState())
    
    def open(self, door):
        print "Drzwi otwarto"

class CloseState(DoorState):
    def action(self, context, door):
        self.close(door)
        context.set_state(OpenState())
    
    def close(self, door):
        print "Drzwi zamknieto"

if __name__ == "__main__":
    c = Context()
    c.action()
    c.action()
    c.action()
    c.action()




