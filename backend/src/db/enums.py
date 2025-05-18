import enum


class ChannelType(enum.StrEnum):
    PRIVATE = "private"
    PUBLIC = "public"


class UserType(enum.StrEnum):
    HUMAN = "human"
    ROBOT = "robot"
