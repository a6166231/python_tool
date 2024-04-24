#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from proto_out import bag_pb2
# import proto
# bag = bag_pb2()

from network.proto_out.person_pb2 import Person
p = Person()
p.name = "1"
p.id = 22
print(p)