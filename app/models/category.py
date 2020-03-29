# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/24.
"""
from lin.exception import NotFound
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship


class Category(Base):
    id = Column(Integer, primary_key=True)
    content = Column(String(20)) # 分类的名称
    quotas = relationship('Quota', back_populates='category') # 该分类下的短句
    ads = relationship('Ad', back_populates='category') # 该分类下的广告
    type = Column(SmallInteger, default=1) # 1-短句分类；2-广告分类


    def _set_fields(self):
        self._fields = ['id', 'content', 'des', 'type']

    @classmethod
    def update_category(cls, cid, form):
        category = cls.query.filter_by(id=cid, delete_time=None).first()
        if category is None:
            raise NotFound(msg='没有找到相关分类')

        category.update(content=form.content.data, type=form.type.data, commit=True)
        return True

    @classmethod
    def remove_category(cls, cid):
        category = cls.query.filter_by(id=cid, delete_time=None).first()
        if category is None:
            raise NotFound(msg='没有找到相关分类')
        # 删除图书，软删除
        category.delete(commit=True)
        return True

    @property
    def des(self):
        """此分类属于短句还是广告"""
        return '短句' if self.type == 1 else '广告'