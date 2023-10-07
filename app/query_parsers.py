from fastapi.params import Query

from app.entities import AdvertisementType, AdvertisementFilter, CommentFilter, ComplaintFilter, ComplaintType, \
    AdvertisementSort


def parse_advertisements_filtr(
    type: AdvertisementType = Query(None,
                                    title="Advertisement's type",
                                    description="Which advertisements whe should receive",),
    user_id: int = Query(None,
                         title="User's id",
                         description="Which user placed an advertisement",),) -> AdvertisementFilter:
    return AdvertisementFilter(type=type,
                               user_id=user_id)


def parse_comment_filtr(
    user_id: int = Query(None,
                         title="User's id",
                         description="Which user placed a comment",),) -> CommentFilter:
    return CommentFilter(user_id=user_id)


def parse_complaint_filtr(
    type: ComplaintType = Query(None,
                                title="Complaint's type",
                                description="Which advertisements whe should receive"),
    user_id: int = Query(None,
                         title="User's id",
                         description="Which user placed a complaint",),) -> ComplaintFilter:
    return ComplaintFilter(user_id=user_id,
                           type=type)


def parse_advertisement_sort_params(
    publication_time: str = Query(None,
                                  title="Publication time",
                                  description="When advertisement was published"),) -> AdvertisementSort:
    return AdvertisementSort(publication_time=publication_time)
