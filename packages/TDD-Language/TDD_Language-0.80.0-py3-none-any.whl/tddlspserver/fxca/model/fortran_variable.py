"""Elements for Fortran statements from fxtran parsing"""

__author__ = "sgu"

#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from e_direction import EDirection


class FortranVariable:
    """ source for class FortranVariable """

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, type_):
        self._type = type_

    @property
    def direction(self) -> EDirection:
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    @property
    def parent(self) -> object:
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    # @property
    # def sources (self) -> Set[IDataflowEndpoint]:
    #     return self._sources

    def __init__(self, name):
        # self._sources = set ()
        self._direction = EDirection.NONE
        self._name = name

        self._parent = None
        self._type = None

    def add_direction(self, value):
        match self._direction:
            case EDirection.NONE:
                self.direction = value
            case EDirection.BOTH:
                self._direction = EDirection.BOTH
            case EDirection.READ:
                match value:
                    case EDirection.NONE:
                        self._direction = EDirection.READ
                    case EDirection.BOTH:
                        self._direction = EDirection.BOTH
                    case EDirection.READ:
                        self._direction = EDirection.READ
                    case EDirection.WRITE:
                        self._direction = EDirection.BOTH
            case EDirection.WRITE:
                match value:
                    case EDirection.NONE:
                        self._direction = EDirection.READ
                    case EDirection.BOTH:
                        self._direction = EDirection.BOTH
                    case EDirection.READ:
                        self._direction = EDirection.BOTH
                    case EDirection.WRITE:
                        self._direction = EDirection.WRITE
