from __future__ import annotations
from typing import Union
import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table

Base = declarative_base()

STR_LEN = 128


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)

    # one parent container and parent composition
    parent_id = Column(Integer, ForeignKey('item.id'))
    ingredients = Column(Integer, ForeignKey('material.id'))

    # many items can be contained within a single container subject to the containers limits
    # this relationship automatically creates the container parameter associated with the parent_id
    contents = relationship("Item", backref=backref('container', remote_side=[id]),
                            cascade="all, delete, delete-orphan")

    # all the other stuff
    data = Column(String(50))

    def __repr__(self):
        return "<Item(data='%s', id='%s')>" % (self.data, self.id)


class Material(Base):
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True)

    # many parent usecases
    use_case_id = Column(Integer, ForeignKey('material.id'))
    use_cases = relationship("Material", backref=backref('composite', remote_side=[id]),
                             cascade="all, delete, delete-orphan")

    # defining alloy composition
    ingredients = relationship("Material", backref=backref('component', remote_side=[id]))

    data = Column(String(50))

    def __repr__(self):
        return "<Material(data='%s', id='%s')>" % (self.data, self.id)

    def get_root_material(self, include_self=True):
        base_mat_list = []
        for rt_mat in self.ingredients:
            base_mat = rt_mat.get_root_material()
            if len(base_mat):
                base_mat_list += base_mat
            elif include_self:
                base_mat_list.append(self)
        return list(set(base_mat_list))

# todo create a table of materials (including alloys) that can be used as building materials for items.
# todo create a column of sub-items for compound items.
# todo establish limitations and fundamental parameters for materials and extend it to items.
