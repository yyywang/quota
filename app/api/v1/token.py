# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/28.
"""
from flask_jwt_extended import get_current_user
from lin import manager
from lin.jwt import get_tokens, login_required
from lin.redprint import Redprint
from app.libs.enums import ClientTypeEnum
from app.libs.utils import json_res
from app.validators.auth import ClientForm

api = Redprint('token')

@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: manager.user_model.verify,
        ClientTypeEnum.USER_MINA: manager.user_model.verify_mina
    }
    user = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )

    access_token, refresh_token = get_tokens(user)
    return json_res(access_token=access_token, refresh_token=refresh_token)


@api.route('/secret')
@login_required
def get_token_info():
    """获取令牌信息"""
    user = get_current_user()
    return json_res(uid=user.id, is_admin=user.is_admin)