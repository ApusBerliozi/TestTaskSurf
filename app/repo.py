import typing
from contextlib import contextmanager
from uuid import UUID
from fastapi import HTTPException

from sqlalchemy.orm import sessionmaker, Session

from app.entities import NewUser, AdvertisementSort, AdvertisementFilter, Advertisement, User, Comment, CommentFilter, \
    Complaint, ComplaintFilter, Credentials, NewAdvertisement, NewComplaint, NewComment
from app.models import UserModel, AdvertisementModel, CommentModel, ComplaintModel
from libs.password_workflow import hash_password, check_password
from server_params.common_entities import Paginator
from server_params.db import db_engine


@contextmanager
def db_connection():
    db = Session(db_engine)
    try:
        yield db
    finally:
        db.close()


def create_user(user: NewUser) -> str:
    with db_connection() as db:
        user = UserModel(name=user.name,
                         login=user.login,
                         password=hash_password(user.password),
                         surname=user.surname)
        try:
            db.add(user)
            db.commit()
        except:
            raise HTTPException(status_code=400, detail="User already exists")
        return str(user.uuid)


def get_user(credentials: Credentials) -> str:
    with db_connection() as db:
        user = db.query(UserModel).\
            filter(UserModel.login == credentials.login).\
            first()
        if user:
            if check_password(password=credentials.password,
                              hash=user.password):
                return str(user.uuid)
        else:
            raise HTTPException(status_code=404, detail="Item not found")


def collect_advertisements(paginator: Paginator,
                           filt: AdvertisementFilter,
                           sort_param: AdvertisementSort,) -> typing.List[dict]:
    offset = (paginator.page - 1) * paginator.limit
    with db_connection() as db:
        if filt.type and sort_param.publication_time:
            advertisement_page = db.query(AdvertisementModel, UserModel).\
                join(UserModel).\
                filter(AdvertisementModel.type == filt.type.value).\
                order_by(AdvertisementModel.created_at).\
                limit(paginator.limit).\
                offset(offset).\
                all()
        elif filt.type and not sort_param.publication_time:
            advertisement_page = db.query(AdvertisementModel, UserModel). \
                join(UserModel). \
                filter(AdvertisementModel.type == filt.type.value). \
                limit(paginator.limit). \
                offset(offset). \
                all()
        else:
            advertisement_page = db.query(AdvertisementModel, UserModel). \
                join(UserModel). \
                limit(paginator.limit). \
                offset(offset). \
                all()
        return [Advertisement(id=row[0].id,
                              user=User(
                                  uuid=str(row[1].uuid),
                                  name=row[1].name,
                                  surname=row[1].surname
                              ),
                              name=row[0].caption,
                              type=row[0].type.value,
                              content=row[0].content,
                              publication_time=row[0].created_at).__dict__ for row in advertisement_page]


def generate_advertisement(advertisement: NewAdvertisement,
                           user_uuid: UUID,) -> dict:
    with db_connection() as db:
        advertisement = AdvertisementModel(caption=advertisement.name,
                                           content=advertisement.content,
                                           type=advertisement.type.value,
                                           user_uuid=user_uuid)
        db.add(advertisement)
        db.commit()
        user = db.query(UserModel).filter(UserModel.uuid == user_uuid).first()
        return Advertisement(id=advertisement.id,
                             user=User(
                                  uuid=str(user.uuid),
                                  name=user.name,
                                  surname=user.surname
                              ),
                             name=advertisement.caption,
                             type=advertisement.type.value,
                             content=advertisement.content,
                             publication_time=advertisement.created_at).__dict__


def receive_advertisement(advertisement_id: int,) -> dict:
    with db_connection() as db:
        advertisement = db.query(AdvertisementModel, UserModel).\
            join(UserModel).\
            filter(AdvertisementModel.id == advertisement_id).\
            first()
        if advertisement:
            return Advertisement(id=advertisement[0].id,
                                 user=User(
                                  uuid=str(advertisement[1].uuid),
                                  name=advertisement[1].name,
                                  surname=advertisement[1].surname
                                            ),
                                 name=advertisement[0].caption,
                                 type=advertisement[0].type,
                                 content=advertisement[0].content,
                                 publication_time=advertisement[0].created_at).__dict__
        else:
            raise HTTPException(status_code=404, detail="Item not found")


def delete_advertisement(advertisement_id: int,) -> None:
    with db_connection() as db:
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
                         paginator: Paginator) -> typing.List[dict]:
    offset = (paginator.page - 1) * paginator.limit
    with db_connection() as db:
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
        return [Comment(id=row[0].id,
                        user=User(
                              uuid=str(row[1].uuid),
                              name=row[1].name,
                              surname=row[1].surname
                                        ),
                        content=row[0].content,
                        published_at=row[0].created_at).__dict__ for row in comments]


def remove_comment(comment_id: int,) -> None:
    with db_connection() as db:
        comment = db.query(CommentModel).\
            filter(CommentModel.id == comment_id). \
            first()
        if comment:
            db.delete(comment)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Item not found")


def generate_comment(advertisement_id: int,
                     comment: NewComment,
                     user_uuid: UUID) -> dict:
    with db_connection() as db:
        comment = CommentModel(content=comment.content,
                               advertisement_id=advertisement_id,
                               user_uuid=user_uuid)
        db.add(comment)
        db.commit()
        user = db.query(UserModel).filter(UserModel.uuid == user_uuid).first()
        return Comment(id=comment.id,
                       user=User(
                              uuid=str(user.uuid),
                              name=user.name,
                              surname=user.surname
                                        ),
                       content=comment.content,
                       published_at=comment.created_at).__dict__


def make_admin(user_login: str) -> str:
    with db_connection() as db:
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
        return str(admin_uuid)


def generate_complaint(advertisement_id: int,
                       user_uuid: UUID,
                       complaint: NewComplaint) -> dict:
    with db_connection() as db:
        complaint = ComplaintModel(content=complaint.content,
                                   advertisement_id=advertisement_id,
                                   user_uuid=user_uuid,
                                   type=complaint.type.value,)
        db.add(complaint)
        db.commit()
        user = db.query(UserModel).filter(UserModel.uuid == user_uuid).first()
        return Complaint(id=complaint.id,
                         user=User(
                                uuid=str(user.uuid),
                                name=user.name,
                                surname=user.surname
                            ),
                         content=complaint.content,
                         type=complaint.type.value,
                         publication_tyme=complaint.created_at).__dict__


def collect_complaints(advertisement_id: int,
                       paginator: Paginator,
                       filtr: ComplaintFilter,) -> typing.List[dict]:
    offset = (paginator.page - 1) * paginator.limit
    with db_connection() as db:
        if filtr.type:
            complaints = db. \
                query(ComplaintModel, UserModel). \
                join(UserModel). \
                filter(ComplaintModel.type == ComplaintFilter.type.value,
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
        return [Complaint(id=row[0].id,
                          user=User(
                                uuid=str(row[1].uuid),
                                name=row[1].name,
                                surname=row[1].surname
                            ),
                          content=row[0].content,
                          type=row[0].type.value,
                          publication_time=row[0].created_at).__dict__ for row in complaints]
