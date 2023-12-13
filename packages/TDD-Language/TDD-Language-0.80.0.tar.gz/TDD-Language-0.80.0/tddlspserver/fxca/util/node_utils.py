""" Accessor functions for nodes of Fortran parse objects from xml(http://fxtran.net/#syntax)"""

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

from typing import Any, Callable, List


class NodeUtils():
    _ROOT_PROGRAM: str = "main"

    #  methods.
    @classmethod
    def name_of_called_function(cls, function_call_node) -> str:
        return NodeUtils.get_successor_node(function_call_node, "0,0").getTextContent().toLowerCase(Locale.getDefault())

    @classmethod
    def name_of_called_operation(cls, operation_call_node) -> str:
        return NodeUtils.get_successor_node(operation_call_node, "1").getTextContent().toLowerCase(Locale.getDefault())

    # TODO check None == ...
    @classmethod
    def has_name(cls, name: str) -> Callable[[Any], bool]:
        return lambda node: False if node is None else name == node.getNodeName()

    @classmethod
    def has_text_content(cls, content: str) -> Callable[[Any], bool]:
        return lambda node: content == node.getTextContent()

    # TODO predicate.test
    @classmethod
    def child_satisfies(cls, path: str, predicate: Callable[[Any], Any]) -> Callable[[Any], bool]:
        return lambda node: predicate.test(NodeUtils.get_successor_node(node, path))

    @classmethod
    def node_type(cls, node_type) -> str:
        match node_type:
            case Node.ELEMENT_NODE:
                return "Element Node"
            case Node.ATTRIBUTE_NODE:
                return "Attribute Node"
            case Node.TEXT_NODE:
                return "Text Node"
            case Node.CDATA_SECTION_NODE:
                return "CDATA Section Node"
            case Node.ENTITY_REFERENCE_NODE:
                return "Entity Reference Node"
            case Node.ENTITY_NODE:
                return "Entity Node"
            case Node.PROCESSING_INSTRUCTION_NODE:
                return "Processing Instruction Node"
            case Node.COMMENT_NODE:
                return "Comment Node"
            case Node.DOCUMENT_NODE:
                return "Document Node"
            case Node.DOCUMENT_TYPE_NODE:
                return "Document Type Node"
            case Node.DOCUMENT_FRAGMENT_NODE:
                return "Document Fragment Node"
            case Node.NOTATION_NODE:
                return "Notation Node"
            case _:
                return "Unknown Node Type"

    @classmethod
    def print_node(cls, node, depth):
        spaces: List[str] = [" "] * depth

        number_of_printed_nodes: int = 1
        print("".join(spaces) + "[node type] " + NodeUtils.node_type(node.getNodeType()))
        print("".join(spaces) + "[node name] " + node.getNodeName())
        print("".join(spaces) + "[node value] " + node.getNodeValue())
        print("".join(spaces) + "[node text content] " + node.getTextContent())
        print("".join(spaces) + "[node #kids] " + node.getChildNodes().getLength())
        i = 0
        while i < node.getChildNodes().getLength():
            number_of_printed_nodes += NodeUtils.print_node(child, depth + 1)
            i += 1
        return number_of_printed_nodes

    @classmethod
    def get_successor_node(cls, node, path):
        """ generated source for method getSuccessorNode """
        first_number = StringUtils.substringBefore(path, ",")
        next_path = StringUtils.substringAfter(path, ",")
        child_index = Integer.parseInt(first_number)
        children = node.getChildNodes()
        if children.getLength() < child_index:
            System.err.println("No children found for node " + node)
            return None
        if next_path.isEmpty():
            return node.getChildNodes().item(child_index)
        else:
            return NodeUtils.get_successor_node(node.getChildNodes().item(child_index), next_path)

    @classmethod
    def find_child_first(cls, parent, condition):
        """ generated source for method findChildFirst """
        node = parent.getFirstChild()
        while node is not None:
            if condition.test(node):
                return node
            node = node.getNextSibling()
        return None

    @classmethod
    @overloaded
    def find_first(cls, parent, next_node, condition, include_self):
        """ generated source for method findFirst """
        return NodeUtils.find_first(parent, next_node, condition, include_self, None)

    @classmethod
    @find_first.register(object, Node, Function, Predicate, bool, List)
    def find_first_0(cls, parent, next_node, condition, include_self, parantheses_types):
        """ generated source for method findFirst_0 """
        result = NodeUtils.findAll(parent, next_node, condition, include_self, parantheses_types, 1)
        return None if result.isEmpty() else result.get(0)

    @classmethod
    def has_connected_with(cls, parent, nextNode, condition, includeSelf):
        """ generated source for method hasConnectedWith """
        return NodeUtils.find_first(parent, nextNode, condition, includeSelf) is not None

    @classmethod
    def add_all_descendents_to(cls, node, predicate, include_self, selected_nodes):
        """ generated source for method addAllDescendentsTo """
        if predicate.test(node) and include_self:
            selected_nodes.add(node)
        i = 0
        while i < node.getChildNodes().getLength():
            NodeUtils.add_all_descendents_to(child, predicate, True, selected_nodes)
            i += 1
        return selected_nodes

    @classmethod
    @overloaded
    def get_name_of_operation(cls, node):
        """ generated source for method getNameOfOperation """
        if Predicates.isSubroutineStatement.test(node):
            return NodeUtils.get_name_of_operation(node, Predicates.isSubroutineName)
        elif Predicates.isFunctionStatement.test(node):
            return NodeUtils.get_name_of_operation(node, Predicates.isFunctionName)
        elif Predicates.isEntryStatement.test(node):
            return NodeUtils.get_name_of_operation(node, Predicates.isEntryName)
        elif Predicates.isProgramStatement.test(node):
            return NodeUtils._ROOT_PROGRAM
        raise IllegalArgumentException("Node is not a function, subroutine, entry or program statement.")

    @classmethod
    @get_name_of_operation.register(object, Node, Predicate)
    def get_name_of_operation_0(cls, node, predicate):
        """ generated source for method getNameOfOperation_0 """
        name_nodes = NodeUtils.allDescendents(node, predicate, True)
        return NodeUtils.get_name(name_nodes.iterator().next())

    @classmethod
    def get_name(cls, node):
        """ generated source for method getName """
        big_n_node = node.getFirstChild()
        little_n_node = big_n_node.getFirstChild()
        return little_n_node.getTextContent().toLowerCase(Locale.getDefault())

    @classmethod
    def get_callee_name_from_call(cls, call_statement_node):
        """ generated source for method getCalleeNameFromCall """
        return NodeUtils.get_name(call_statement_node.getFirstChild().getNextSibling())

    @classmethod
    def get_assignment_expression(cls, stmt):
        """ generated source for method getAssignmentExpression """
        e = stmt
        elems = e.getElementsByTagName("E-2")
        return elems.item(0)

    @classmethod
    def get_assigment_variable(cls, statement):
        """ generated source for method getAssigmentVariable """
        e = statement
        elems = e.getElementsByTagName("E-1")
        return elems.item(0)

    @classmethod
    def get_name_of_containing_operation(cls, node):
        """ generated source for method getNameOfContainingOperation """
        containing_operation_statement = NodeUtils.findContainingStatement(node, Predicates.isOperationStatement, Predicates.paranthesisTypes)
        return NodeUtils._ROOT_PROGRAM if containing_operation_statement is None else NodeUtils.get_name_of_operation(containing_operation_statement)

    @classmethod
    def satisfies_assumptions(cls, node):
        """ generated source for method satisfiesAssumptions """
        if node is None:
            return True
        type_ = node.getNodeType()
        if (type_ == Node.TEXT_NODE) and (node.getChildNodes().getLength() > 0):
            raise IllegalArgumentException("text node with children")
        if "call-stmt" == node.getNodeName() and (node.getChildNodes().getLength() < 2):
            NodeUtils.print_node(node, 0)
            raise IllegalArgumentException("call statement with < 2 children")
        if Predicates.isNamedExpression.test(node):
            if not Predicates.isBigN.test(firstChild):
                raise IllegalArgumentException(String.format("Expected <N> in named expression, but found %s as first child.", first_child.getNodeName()))
            if not Predicates.isSmallN.test(firstGrandChild):
                raise IllegalArgumentException(
                    String.format(
                        "Expected <n> in named expression, but found %s as first gand child.", first_grand_child.getNodeName()
                    )
                )
            if firstGrandChild.getChildNodes().getLength() > 1:
                NodeUtils.print_node(firstGrandChild, 0)
                raise IllegalArgumentException("named expression with unexpected chlildren length list of first grandchild.")
        return True
