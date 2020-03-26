# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/24.
"""
from lin import db
from lin.exception import NotFound
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.libs.utils import dict_rm_none
from app.models.category import Category


class Ad(Base):
    id = Column(Integer, primary_key=True)
    cover_url = Column(String(190)) # 封面url
    link_url = Column(Text) # 跳转地址
    des = Column(String(190)) # 广告描述
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='ads') # 所属分类

    def _set_fields(self):
        self._fields = ['id', 'des', 'cover_url', 'link_url', 'category']

    @classmethod
    def remove_ad(cls, aid):
        ad = cls.query.filter_by(id=aid, delete_time=None).first()
        if ad is None:
            raise NotFound()
        ad.delete(commit=True)
        return True

    @classmethod
    def update_ad(cls, aid, data):
        ad = cls.query.filter_by(id=aid, delete_time=None).first_or_404()
        data = dict_rm_none(data)
        with db.auto_commit():
            ad.set_attrs(data)
        return True

    @classmethod
    def set_category(cls, quota_id, category_id):
        category = Category.query.filter_by(id=category_id, delete_time=None).first_or_404()
        ad = cls.query.filter_by(id=quota_id, delete_time=None).first_or_404()
        with db.auto_commit():
            category.ads.append(ad)