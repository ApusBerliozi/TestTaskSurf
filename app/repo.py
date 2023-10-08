import typing
from contextlib import contextmanager
from uuid import UUID
from fastapi import HTTPException

from sqlalchemy.orm import sessionmaker, Session

from app.entities import NewUser, AdvertisementSort, AdvertisementFilter, Advertisement, User, Comment, CommentFilter, \
    Complaint, ComplaintFilter, Credentials
from app.models import UserModel, AdvertisementModel, CommentModel, ComplaintModel
from libs.password_workflow import hash_password
from server_params.common_entities import Paginator
from server_params.db import db_engine


UserSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
AdvertisementSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
ComplaintSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
CommentSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


@contextmanager
def db_connection(session: sessionmaker[Session]):
    db = session()
    try:
        yield db
    finally:
        db.close()


def create_user(user: NewUser) -> UUID:
    with db_connection(UserSession) as db:
        user = UserModel(name=user.name,
                         login=user.login,
                         password=hash_password(user.password),
                         surname=user.surname)
        db.add(user)
        db.commit()
    return user.uuid


def get_user(credentials: Credentials) -> UUID:
    with db_connection(UserSession) as db:
        user = db.query(UserModel).\
            filter(UserModel.login == credentials.login,
                   UserModel.password == hash_password(credentials.password)).\
            first()
        if user:
            return user.uuid
        else:
            raise HTTPException(status_code=404, detail="Item not found")


def collect_advertisements(paginator: Paginator,
                           filt: AdvertisementFilter,
                           sort_param: AdvertisementSort,) -> typing.List[Advertisement]:
    offset = (paginator.page - 1) * paginator.limit
    with db_connection(AdvertisementSession) as db:
        if filt.type and sort_param.publication_time:
            advertisement_page = db.query(AdvertisementModel, UserModel).\
                join(UserModel).\
                filter(AdvertisementModel.type == filt.type).\
                order_by(AdvertisementModel.created_at).\
                limit(paginator.limit).\
                offset(offset).\
                all()
        elif filt.type and not sort_param.publication_time:
            advertisement_page = db.query(AdvertisementModel, UserModel). \
                join(UserModel). \
                filter(AdvertisementModel.type == filt.type). \
                limit(paginator.limit). \
                offset(offset). \
                all()
        else:
            advertisement_page = db.query(AdvertisementModel, UserModel). \
                join(UserModel). \
                limit(paginator.limit). \
                offset(offset). \
                all()
    return [Advertisement(id=advertisement.id,
                          user=User(
                              uuid=advertisement.uuid,
                              name=advertisement.name,
                              surname=advertisement.surname
                          ),
                          name=advertisement.caption,
                          type=advertisement.type,
                          content=advertisement.content,
                          publication_time=advertisement.created_at) for advertisement in advertisement_page]


def generate_advertisement(advertisement: Advertisement,
                           user_uuid: UUID,) -> Advertisement:
    with db_connection(AdvertisementSession) as db:
        advertisement = AdvertisementModel(caption=advertisement.name,
                                           content=advertisement.content,
                                           type=advertisement.type,
                                           user_uuid=user_uuid)
        db.add(advertisement)
        db.commit()
    return Advertisement(id=advertisement.id,
                         user=User(
                              uuid=advertisement.uuid,
                              name=advertisement.name,
                              surname=advertisement.surname
                          ),
                         name=advertisement.caption,
                         type=advertisement.type,
                         content=advertisement.content,
                         publication_time=advertisement.created_at)


def receive_advertisement(advertisement_id: int,) -> Advertisement:
    with db_connection(AdvertisementSession) as db:
        advertisement = db.query(AdvertisementModel, UserModel).\
            join(UserModel).\
            filter(AdvertisementModel.id == advertisement_id).\
            first()
    return Advertisement(id=advertisement.id,
                         user=User(
                          uuid=advertisement.uuid,
                          name=advertisement.name,
                          surname=advertisement.surname
                                    ),
                         name=advertisement.caption,
                         type=advertisement.type,
                         content=advertisement.content,
                         publication_time=advertisement.created_at)


def delete_advertisement(advertisement_id: int,) -> None:
    with db_connection(AdvertisementSession) as db:
        advertisement = db.query(AdvertisementModel).\
            filter(AdvertisementModel.id == advertisement_id).\
            first()
        if advertisement:
            db.delete(advertisement)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Item not found")


def collect_adv_comments(advertisement_id: int,
                         filtr: CommentFilter,
                         paginator: Paginator) -> typing.List[Comment]:
    offset = (paginator.page - 1) * paginator.limit
    with db_connection(CommentSession) as db:
        if filtr.user_id:
            comments = db. \
                       query(CommentModel, UserModel).\
                       join(UserModel).\
                       filter(CommentModel.advertisement_id == advertisement_id).\
                       limit(paginator.limit).\
                       offset(offset).\
                       all()
        else:
            comments = db. \
                query(CommentModel, UserModel). \
                join(UserModel).\
                limit(paginator.limit). \
                offset(offset). \
                all()
    return [Comment(id=comment.id,
                    user=User(
                          uuid=comment.uuid,
                          name=comment.name,
                          surname=comment.surname
                                    ),
                    content=comment.content) for comment in comments]


def remove_comment(comment_id: int,) -> None:
    with db_connection(CommentSession) as db:
        comment = db.query(CommentModel).\
            filter(CommentModel.id == comment_id). \
            first()
        if comment:
            db.delete(comment)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Item not found")


def generate_comment(advertisement_id: int,
                     comment: Comment,
                     user_uuid: UUID) -> Comment:
    with db_connection(CommentSession) as db:
        advertisement = CommentModel(content=comment.content,
                                     advertisement_id=advertisement_id,
                                     user_uuid=user_uuid)
        db.add(advertisement)
        db.commit()
    return Comment(id=comment.id,
                   user=User(
                          uuid=comment.uuid,
                          name=comment.name,
                          surname=comment.surname
                                    ),
                   content=comment.content)


def make_admin(user_login: str) -> UUID:
    with db_connection(UserSession) as db:
        user = db. \
               query(UserModel).\
               filter(UserModel.login == user_login).\
               first()
        if user:
            user.role = "admin"
            admin_uuid = user.uuid
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    return admin_uuid


def generate_complaint(advertisement_id: int,
                       user_uuid: UUID,
                       complaint: Complaint) -> Complaint:
    with db_connection(ComplaintSession) as db:
        complaint = ComplaintModel(content=complaint.content,
                                   advertisement_id=advertisement_id,
                                   user_uuid=user_uuid,
                                   type=complaint.type,)
        db.add(complaint)
        db.commit()
    return Complaint(id=complaint.id,
                     user=User(
                            uuid=complaint.uuid,
                            name=complaint.name,
                            surname=complaint.surname
                        ),
                     content=complaint.content,
                     type=complaint.type,
                     publication_tyme=complaint.created_at)


def collect_complaints(advertisement_id: int,
                       paginator: Paginator,
                       filtr: ComplaintFilter,) -> typing.List[Complaint]:
    offset = (paginator.page - 1) * paginator.limit
    with db_connection(ComplaintSession) as db:
        if filtr.type:
            complaints = db. \
                query(ComplaintModel, UserModel). \
                join(UserModel). \
                filter(ComplaintModel.type == ComplaintFilter.type,
                       ComplaintModel.advertisement_id == advertisement_id). \
                limit(paginator.limit). \
                offset(offset). \
                all()
        else:
            complaints = db. \
                query(ComplaintModel, UserModel). \
                join(UserModel). \
                filter(ComplaintModel.advertisement_id == advertisement_id). \
                limit(paginator.limit). \
                offset(offset). \
                all()
    return [Complaint(id=complaint.id,
                      user=User(
                            uuid=complaint.uuid,
                            name=complaint.name,
                            surname=complaint.surname
                        ),
                      content=complaint.content,
                      type=complaint.type,
                      publication_tyme=complaint.created_at) for complaint in complaints]
