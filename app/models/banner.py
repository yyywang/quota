# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/24.
"""
from lin import db
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, Text

from app.libs.utils import dict_rm_none


class Banner(Base):
    id = Column(Integer, primary_key=True)
    cover_url = Column(String(190)) # 封面图片
    link_url = Column(Text) # 链接地址

    def _set_fields(self):
        self._fields = ['id', 'link_url', '_cover_url']

    @classmethod
    def create_banner(cls, data):
        """创建一个轮播图"""
        data = dict_rm_none(data)
        with db.auto_commit():
            banner = Banner()
            banner.set_attrs(data)
            db.session.add(banner)
        return True

    @classmethod
    def update_banner(cls, bid, data):
        banner = cls.query.filter_by(id=bid, delete_time=None).first_or_404()
        data = dict_rm_none(data)
        with db.auto_commit():
            banner.set_attrs(data)
        return True

    @classmethod
    def remove_banner(cls, bid):
        banner = cls.query.filter_by(id=bid, delete_time=None).first_or_404()
        banner.delete(commit=True)

    @property
    def _cover_url(self):
        return eval(repr(self.cover_url).replace(r"\\", "/"))