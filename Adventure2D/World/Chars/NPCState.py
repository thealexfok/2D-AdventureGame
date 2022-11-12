from pickle import TRUE
import World.WorldCommon as WC
from World.Chars.Character import AnimType

class Action:
    def __init__(self, element):
        pass

    def Enter(self, char):
        pass

    def Exit(self, char):
        pass

    def Act(self, char, deltaTime):
        pass

class IdleAction(Action):
    def Enter(self, char):
        char.AnimType = AnimType.IDLE
        char.walkChannel.pause()
        pass

class ChaseAction(Action):
    def __init__(self, element):
        self.speed = float(element.get("speed"))
        super().__init__(element)
    
    def Enter(self, char):
        char.AnimType = AnimType.WALK
        char.walkChannel.unpause()
        self.target = WC.Players[0]
        char.moveDir, len = WC.ComputeDir(char.GetCenterPosition(), self.target.GetCenterPosition())
        char.hpbar.visible = True
        super().Enter(char)

    def Act(self, char, deltaTime):
        WC.MoveDir(char, char.moveDir, self.target.GetCenterPosition(), self.speed, deltaTime)
        char.moveDir, len = WC.ComputeDir(char.GetCenterPosition(), self.target.GetCenterPosition())
        super().Act(char,deltaTime)

class ReturnAction(Action):
    pass

def CreateAction(element):
    action = element.find("Action")
    if action == None:
        return
    atype = action.get("type")
    if atype == "Idle":
        return IdleAction(action)
    if atype == "Chase":
        return ChaseAction(action)
    if atype == "Return":
        return ReturnAction(action)

class Decision:
    def __init__(self, element, state):
        self.state = state
        self.trueState = element.get("trueState")
        self.falseState = element.get("falseState")

    def Decide(self, char):
        return False

class PlayerInRange(Decision):
    def __init__(self, element, state):
        super().__init__(element, state)
        self.dist = int(element.get("distance"))
        self.distSqr = self.dist * self.dist

    def Decide(self, char):
        if hasattr(self.state.action, 'target'):
            target = self.state.action.target
        else:
            target = WC.Players[0]

        playerBox = target.GetCollisionBox()
        aiBox = char.GetCollisionBox()


        xdiff = 0
        ydiff = 0

        if playerBox.x > aiBox.x + aiBox.width:
            xdiff = playerBox.x - (aiBox.x + aiBox.width)
        elif playerBox.x + playerBox.width < aiBox.x:
            xdiff = aiBox.x - (playerBox.x + playerBox.width)

        if playerBox.y > aiBox.y + aiBox.height:
            ydiff = playerBox.y - (aiBox.y + aiBox.height)
        elif playerBox.y + playerBox.height < aiBox.y:
            ydiff = aiBox.y - (playerBox.y + playerBox.height)
    
        len = xdiff * xdiff + ydiff * ydiff
        return len < self.distSqr


class HomeInRange(Decision):
    pass

class WasAttacked(Decision):
    def __init__(self, element, state):
        super().__init__(element, state)

    def Decide(self, char):
        #char.hpbar.visible = True
        return False
    # pass

class TimeIsUp(Decision):
    pass


def CreateDecision(element, state):
    type = element.get("decide")
    if type == "player_in_range":
        return PlayerInRange(element, state)
    if type == "home_in_range":
        return HomeInRange(element, state)
    if type == "was_attacked":
        print("was attacked")
        return WasAttacked(element, state)
    if type == "time_is_up":
        return TimeIsUp(element, state)
    return None

class State():
    def __init__(self,element):
        self.name = element.get("name")
        self.action = CreateAction(element)
        self.decisions = []
        for decision in element.findall("Decision"):
            self.decisions.append(CreateDecision(decision, self))
    
    def Update(self, char, deltaTime):
        self.action.Act(char, deltaTime)
        
        for decision in self.decisions:
            #if decision is not None:
            result = decision.Decide(char)
            if result:
                if decision.trueState != char.curState:
                    char.curState = decision.trueState
                    self.action.Exit(char)
                    return decision.trueState
            else:
                if decision.falseState != char.curState:
                    char.curState = decision.falseState
                    self.action.Exit(char)
                    return decision.falseState
        return None
