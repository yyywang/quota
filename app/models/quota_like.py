# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/26.
"""
# from lin.interface import InfoCrud as Base
# from sqlalchemy import Column, Integer, ForeignKey
# from sqlalchemy.orm import relationship
#
#
# class QuotaLike(Base):
#     """点赞语录"""
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('lin_user.id'))
#     user = relationship('User', back_populates='liked_quotas')
#     quota_id = Column(Integer, ForeignKey('quota.id'))
#     quota = relationship('Quota', back_populates='liked_quotas')