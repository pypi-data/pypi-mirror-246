from enum import Enum

from moduler.proto.commons_pb2 import ModuleType as MT


ModuleType = MT


class BaseEnum(str, Enum):
    ...
