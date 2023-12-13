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

from enum import Enum


class EDirection(Enum):
    """ FortranVariable directions """
    READ = 1
    WRITE = 2
    BOTH = 3
    NONE = 4

    def merge(self, direction):
        match self:
            case self.NONE:
                return direction

            case self.BOTH:
                return self.BOTH

            case self.READ:
                match direction:
                    case self.NONE:
                        return self.READ
                    case self.BOTH:
                        return self.BOTH
                    case self.READ:
                        return self.READ
                    case self.WRITE:
                        return self.BOTH

            case self.WRITE:
                match direction:
                    case self.NONE:
                        return self.READ
                    case self.BOTH:
                        return self.BOTH
                    case self.READ:
                        return self.BOTH
                    case self.WRITE:
                        return self.READ
