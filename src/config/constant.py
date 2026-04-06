from enum import Enum


class Language(Enum):
    EN_US = 'en_US'
    ZH_TW = 'zh_TW'


class InterestCategory(Enum):
    INTERESTED_POSITION = 'INTERESTED_POSITION'
    SKILL = 'SKILL'
    TOPIC = 'TOPIC'


class ProfessionCategory(Enum):
    EXPERTISE = 'EXPERTISE'
    INDUSTRY = 'INDUSTRY'


class ExperienceCategory(Enum):
    WORK = 'WORK'
    EDUCATION = 'EDUCATION'
    LINK = 'LINK'


class SeniorityLevel(Enum):
    NO_REVEAL = 'NO REVEAL'
    JUNIOR = 'JUNIOR'
    INTERMEDIATE = 'INTERMEDIATE'
    SENIOR = 'SENIOR'
    STAFF = 'STAFF'
    MANAGER = 'MANAGER'


class RoleType(Enum):
    MENTOR = 'MENTOR'
    MENTEE = 'MENTEE'


class BookingStatus(Enum):
    PENDING = 'PENDING'
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'


class ReservationListState(Enum):
    UPCOMING = 'UPCOMING'
    PENDING = 'PENDING'
    HISTORY = 'HISTORY'


class SortingBy(Enum):
    UPDATED_TIME = 'UPDATED_TIME'
    # VIEW = 'VIEW'


class Sorting(Enum):
    ASC = 1
    DESC = -1


class MentorAction(str, Enum):
    UPSERT_MENTOR_PROFILE = "UPSERT_MENTOR_PROFILE"  # PUT /users/profile
    PUT_MENTOR_PROFILE    = "PUT_MENTOR_PROFILE"      # PUT /mentors/mentor_profile
    PATCH_MENTOR_PROFILE  = "PATCH_MENTOR_PROFILE"    # PUT|DELETE /mentors/{id}/experiences
    DELETE_MENTOR_PROFILE = "DELETE_MENTOR_PROFILE"   # future: delete mentor account
