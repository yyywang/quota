# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/26.
"""
from flask import jsonify
from lin.redprint import Redprint

from app.models.category import Category

category_api = Redprint('categorys')

@category_api.route('')
def get_categorys():
    """获取所有分类数据"""
    categories = Category.query.filter_by(delete_time=None).order_by(Category._create_time.desc()).all()
    returned = [item.content for item in categories]
    returned = ['全部'] + returned

    return jsonify(returned)