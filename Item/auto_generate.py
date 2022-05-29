import random

from twilight.Item.Tabulars import Item, Material
import numpy as np
import random


def generate_materials(sess, num=1):
    material_list = []
    for ind in range(num):
        new_obj = Material()
        if len(material_list):
            child_mat = random.choice(material_list)
            child_mat.ingredients.append(new_obj)
        material_list.append(new_obj)

    for nw_mat in material_list:
        nw_mat.ingredients = nw_mat.get_root_material(include_self=False)

    sess.add_all(material_list)
    sess.commit()
    print(f"{num} materials were generated.")
    return


def generate_items(sess, num=1):
    generate_materials(sess=sess, num=num)
    all_mat = sess.query(Material).all()
    obj_list = []
    for ind in range(num):
        new_obj = Item()
        if len(obj_list):
            parent_obj = random.choice(obj_list)
            parent_obj.contents.append(new_obj)
        obj_list.append(new_obj)
    sess.add_all(obj_list)
    sess.commit()
    print(f"{num} items were generated.")
    return

