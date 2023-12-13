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

from typing import Set, final

from common_block import CommonBlock
from containment_hash_map import ContainmentHashMap
from fortran_module import FortranModule
from fortran_parameter import FortranParameter
from fortran_variable import FortranVariable


class FortranOperation:
    """ source for class FortranOperation """

    @final
    @property
    def name(self) -> str:
        return self._name

    @final
    @property
    def common_blocks(self) -> ContainmentHashMap[str, CommonBlock]:
        return self._common_blocks

    @final
    @property
    def variables(self) -> ContainmentHashMap[str, FortranVariable]:
        return self._variables

    @final
    @property
    def parameters(self) -> ContainmentHashMap[str, FortranParameter]:
        return self._parameters

    @final
    @property
    def used_modules(self) -> Set[str]:
        return self._used_modules

    # TODO add node if needed
    # @final
    # @property
    # def node (self) -> Node:
    #     return self._node

    @property
    def module(self) -> FortranModule:
        return self._module

    @module.setter
    def module(self, module):
        self._module = module

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def implicit(self) -> bool:
        return self._implicit

    @implicit.setter
    def implicit(self, implicit):
        self._implicit = implicit

    @final
    @property
    def variable_arguments(self) -> bool:
        return self._variable_arguments

    @final
    @property
    def function(self) -> bool:
        return self._function

    def __init__(self, name, node, function, variable_arguments=False):
        self._name = name
        # self._node = node
        self._variable_arguments = variable_arguments
        self._function = function

        self._common_blocks = ContainmentHashMap(self)
        self._variables = ContainmentHashMap(self)
        self._parameters = ContainmentHashMap(self)
        self._used_modules = set()

        self._implicit = None
        self._module = None
        self._parent = None

    def __str__(self):
        """ toString method """
        return f"op {self.name}"
