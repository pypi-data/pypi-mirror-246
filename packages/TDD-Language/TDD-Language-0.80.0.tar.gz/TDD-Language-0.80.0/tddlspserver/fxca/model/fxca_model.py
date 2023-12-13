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

from typing import List


class FortranSubroutine:
    """
    Subroutine statement
    """

    # TODO use dependencies?

    name: str
    arguments: List[str]
    variables: List[str]


class FortranFunction:
    """
    Function statement
    """

    # TODO intern variables?

    name: str
    arguments: List[str]
    result: str
    variables: List[str]


class FortranProgram:
    """
    Program statement
    """

    name: str
    variables: List[str]
    dependencies: List[str]
