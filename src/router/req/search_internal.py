from fastapi import Header, Body
from ...domain.mentor.model.mentor_model import MentorProfileDTO


def post_mentor(
    body: MentorProfileDTO = Body(...)
) -> (MentorProfileDTO):
    return body
