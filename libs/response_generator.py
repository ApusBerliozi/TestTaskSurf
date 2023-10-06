import datetime
import typing

from pydantic import BaseModel, create_model


def class_generator(annotation: typing.Union[list, BaseModel]):
    if type(annotation) is list:
        class Response(BaseModel):
            content: typing.List[annotation[0]]
            date: str
        return Response
    else:
        class Response(BaseModel):
            content: annotation
            date: str
        return Response


def response_model_factory(annotation: typing.Union[list, dict, typing.Type[BaseModel]]):
    if type(annotation) is dict:
        annotation_model = create_model('AnnotationModel', **{
            key: (value, None) for key, value in annotation.items()})
        return class_generator(annotation_model)
    else:
        return class_generator(annotation)
