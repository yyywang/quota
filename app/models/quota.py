# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/23.
"""
from lin import db
from lin.exception import NotFound
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.category import Category


class Quota(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text) # html 格式
    content_text = Column(Text) # 纯文本格式
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', back_populates='quotas') # 所属分类

    def _set_fields(self):
        self._fields = ['id', 'content', 'content_text', 'category']

    @classmethod
    def update_quota(cls, qid, form):
        quota = Quota.query.filter_by(id=qid, delete_time=None).first()
        if quota is None:
            return NotFound(msg='语录不存在')
        quota.update(
            content=form.content.data,
            content_text=form.content.plain_text,
            category_id=form.category_id.data,
            commit=True
        )
        return True

    @classmethod
    def remove_quota(cls, qid):
        quota = cls.query.filter_by(id=qid, delete_time=None).first()
        if quota is None:
            raise NotFound(msg='没有找到相关语录')
        # 删除图书，软删除
        quota.delete(commit=True)
        return True

    @classmethod
    def set_category(cls, quota_id, category_id):
        category = Category.query.filter_by(id=category_id, delete_time=None).first_or_404()
        quota = Quota.query.filter_by(id=quota_id, delete_time=None).first_or_404()
        with db.auto_commit():
            category.quotas.append(quota)
