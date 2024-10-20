from fastapi import Header, Body
from ...domain.user.model.user_model import *


def post_mentor(
    body: ProfileDTO = Body(...)
) -> (ProfileDTO):
    return body
