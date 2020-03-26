# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/24.
"""
from lin.exception import NotFound
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, Boolean


class BannerStatus(Base):
    id = Column(Integer, primary_key=True)
    status = Column(Boolean, default=True) # 是否打开轮播图

    @classmethod
    def open(cls):
        status = cls.query.filter_by(delete_time=None).first()
        if status is None:
            raise NotFound()
        status.update(status=True, commit=True)

    @classmethod
    def close(cls):
        status = cls.query.filter_by(delete_time=None).first()
        if status is None:
            raise NotFound()
        status.update(status=False, commit=True)

    @classmethod
    def get_status(cls):
        status = cls.query.filter_by(delete_time=None).first()
        return status.status