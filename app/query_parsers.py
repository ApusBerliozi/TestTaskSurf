from fastapi.params import Query

from app.entities import AdvertisementType, AdvertisementFilter, CommentFilter, ComplaintFilter, ComplaintType, \
    AdvertisementSort


def parse_advertisements_filtr(
    type: AdvertisementType = Query(None,
                                    title="Advertisement's type",
                                    description="Which advertisements whe should receive",),) -> AdvertisementFilter:
    return AdvertisementFilter(type=type)





def parse_complaint_filtr(
    type: ComplaintType = Query(None,
                                title="Complaint's type",
                                description="Which advertisements whe should receive"),) -> ComplaintFilter:
    return ComplaintFilter(type=type)


def parse_advertisement_sort_params(
    publication_time: bool = Query(None,
                                   title="Publication time",
                                   description="When advertisement was published"),) -> AdvertisementSort:
    return AdvertisementSort(publication_time=publication_time)
