from enum import Enum

class GameMode(Enum):
    RankedSoloDuel = (10, "Ranked Solo")
    RankedTeamDoubles = (11, "Ranked Duo")
    RankedStandard = (13, "Ranked Standard")
    Tournament = (22, "Tournament")
    RankedBasketballDoubles = (27, "Ranked Basketball Doubles")
    RankedRumble = (28, "Ranked Rumble")
    RankedBreakout = (29, "Ranked Breakout")
    RankedSnowDay = (30, "Ranked SnowDay")
    AutoTournament = (34, "Auto Tournament")

    def __new__(cls, value, str_value):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.str_value = str_value
        return obj
