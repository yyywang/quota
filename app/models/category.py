# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/24.
"""
from lin.exception import NotFound
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Category(Base):
    id = Column(Integer, primary_key=True)
    content = Column(String(20), unique=True) # 分类的名称
    quotas = relationship('Quota', back_populates='category') # 该分类下的短句
    ads = relationship('Ad', back_populates='category') # 该分类下的广告

    @classmethod
    def update_category(cls, cid, form):
        category = Category.query.filter_by(id=cid, delete_time=None).first()
        if category is None:
            raise NotFound(msg='没有找到相关分类')

        category.update(content=form.content.data, commit=True)
        return True

    @classmethod
    def remove_category(cls, cid):
        category = cls.query.filter_by(id=cid, delete_time=None).first()
        if category is None:
            raise NotFound(msg='没有找到相关分类')
        # 删除图书，软删除
        category.delete(commit=True)
        return True
