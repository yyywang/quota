# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/26.
"""
from sqlalchemy import Table, Column, Integer, ForeignKey
from lin.interface import InfoCrud as Base


# 用户点赞的语录
like_and_quota = Table('like_and_quota',
                   Base.metadata,
                   Column('user_id', Integer, ForeignKey('lin_user.id')),
                   Column('quota_id', Integer, ForeignKey('quota.id')))

collect_and_quota = Table('collect_and_quota',
                   Base.metadata,
                   Column('user_id', Integer, ForeignKey('lin_user.id')),
                   Column('quota_id', Integer, ForeignKey('quota.id')))