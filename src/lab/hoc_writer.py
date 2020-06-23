#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""

import textwrap


class Node:

    def __init__(self, name, *, nseg=1, length=25, diam=25, algorithm='hh'):
        self.name = name
        self.nseg = nseg
        self.length = length
        self.diam = diam
        self.algorithm = algorithm

    def __str__(self):
        return textwrap.dedent(f'''\
            {self.name} {{
                nseg = {self.nseg}
                L = {self.length}
                diam = {self.diam}
                insert {self.algorithm}
            }}''')


class Connection:

    def __init__(self, nodeA: Node, indexA: int, nodeB: Node, indexB: int):
        self.nameA = nodeA.name
        self.indexA = indexA
        self.nameB = nodeB.name
        self.indexB = indexB

    def __str__(self):
        return f'{self.nameA}({self.indexA}), {self.nameB}({self.indexB})'


class HocWriter:

    def __init__(self):
        self.nodes = []
        self.connections = []

    def addNode(self, node: Node):
        self.nodes.append(node)

    def connectNodes(self, nodeA: Node, indexA: int, nodeB: Node, indexB: int):
        self.connections.append(Connection(nodeA, indexA, nodeB, indexB))

    def addConnection(self, connection: Connection):
        self.connections.append(connection)

    def __str__(self):
        nodeNames = map(lambda n: n.name, self.nodes)
        s = 'create ' + ', '.join(nodeNames) + '\n'
        for conn in self.connections:
            s += 'connect ' + str(conn) + '\n'
        s += '\n'
        for node in self.nodes:
            s += str(node) + '\n'
        return s


# Example
if __name__ == '__main__':

    axonSpec = {
        'nseg': 100,
        'length': 1000,
        'diam': 2,
        'algorithm': 'pas'
    }

    soma = Node('soma', nseg=1, length=25, diam=25, algorithm='hh')
    axon = Node('axon', **axonSpec)
    dend = Node('dendrite', nseg=5, length=50, diam=2, algorithm='pas')

    hw = HocWriter()
    hw.addNode(soma)
    hw.addNode(axon)
    hw.addNode(dend)
    hw.connectNodes(axon, 0, soma, 1)
    hw.connectNodes(dend, 1, soma, 0)

    print(hw)
