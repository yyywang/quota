# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/26.
"""
from flask import jsonify
from lin.redprint import Redprint

from app.models.category import Category
from app.validators.forms import GetCategoriesForm

category_api = Redprint('categorys')

@category_api.route('')
def get_categories():
    """获取所有分类数据
    
    :params
        <int:type>: 1-短句；2-广告
    """
    form = GetCategoriesForm().validate_for_api()
    categories = Category.query.filter_by(delete_time=None, type=form.type.data)\
        .order_by(Category._create_time.desc()).all()
    returned = [item.content for item in categories]
    returned = ['全部'] + returned

    return jsonify(returned)