import typing

from pydantic import BaseModel, create_model

from server_params.common_entities import ServerResponse


def set_annotation(annotation: typing.Union[tuple, BaseModel],
                   description: str):
    class_params = {}
    annotations = ServerResponse.__annotations__
    class_params.update(ServerResponse().__dict__)
    class_params.pop("content")
    class_params.update({"description": description})
    if type(annotation) is tuple:
        annotations.update({"content": typing.List[annotation[0]]})
    else:
        annotations.update({"content": annotation})
    class_params.update({"__annotations__": annotations})
    return type("AnnotationClass", (BaseModel,), class_params)


def hint_factory(annotation: typing.Union[tuple, dict, typing.Type[BaseModel]],
                 description: str = ""):
    if type(annotation) is dict:
        annotation_model = create_model('AnnotationModel', **{
            key: (value, None) for key, value in annotation.items()})
        return set_annotation(annotation_model,
                              description=description)
    else:
        return set_annotation(annotation,
                              description=description)
