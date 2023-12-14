
from typing import Mapping, List, Tuple, Dict, Any, Optional, Union

import json
import logging
import datetime

from ..pipelines.expression_evaluators.expression_evaluator import Expression

from pydantic import BaseModel, Field

class BaseRef(BaseModel):

    ref:str
    refType:str

    def __init__(self, ref:str, refType:str, **kwargs):
        super().__init__(ref=ref, refType=refType, **kwargs)

    #
    #def __eq__(self, other) -> bool:
    #    return (self.refType, self.ref) == (other.refType, other.ref)



"""
Metrics related base objects, NumericMetric, DistributionMetric, ...
"""


class BaseMetric(BaseModel):

    name:str
    value:Any

    def __init__(self, name:str, value:Any):
        super().__init__(name=name, value=value)


    def get_meta(self) -> Dict[Any, Any]:
        """
        :return: a dict with the fields of the metric object
        """
        return self.model_dump()




"""
Data related base objects, Datasets and Segments
"""
class DataRef(BaseRef):
    def __init__(self, ref:str, refType:str):
        super().__init__(ref, refType)

class DataArtifactRef(DataRef):
    def __init__(self, ref:str):
        super().__init__(ref, "dataArtifact-id")

class DatasetRef(DataRef):
    def __init__(self, ref:str):
        super().__init__(ref, "dataset-id")


class SegmentFilter(BaseModel):
    recipe:str
    recipeType:str

class Segment(BaseModel):
    name:str
    filters: List[SegmentFilter] = []


# the base class for models (in software design context, not ML context)
class ArtifactMeta(BaseModel):



    def get_meta(self) -> Dict[Any, Any]:
        """
        :return: a dict with all the metadata fields of the artifact object
        """
        meta = {}

        # all props except those starting with underscore are metadata
        for k, v in self:
            if isinstance(v, BaseRef):
                meta[k] = dict(v)
            elif isinstance(v, List):
                meta[k] = [ref.model_dump(exclude_none=True) if isinstance(ref, (BaseRef, BaseMetric, TaskArtifact)) else ref for ref in v]
            elif isinstance(v, TransformExecution):
                meta[k] = v.model_dump(exclude_none=True)
            elif isinstance(v, datetime.datetime):
                # convert to utc tz and get millis since epoch
                v_utc:datetime.datetime = v.astimezone(datetime.timezone.utc)
                meta[k] = round(v_utc.timestamp() * 1000)

            elif isinstance(v, Expression):
                meta[k] = v.get_meta()

            elif isinstance(v, dict):
                meta[k] = self._get_dict_meta(v)

            elif v == None: # skip properties that are not set
                pass
            else:
                meta[k] = v


        return meta


    # converts expressions embedded in params etc.
    def _get_dict_meta(self, o):
        meta = {}

        for k, v in o.items():
            if isinstance(v, (int, float, bool, str)):
                meta[k] = v
            elif isinstance(v, list):
                meta[k] = [self._get_dict_meta(e) if isinstance(e, dict) else e for e in v]
            elif isinstance(v, dict):
                meta[k] = self._get_dict_meta(v)
            elif isinstance(v, Expression):
                meta[k] = v.get_meta()
            else:
                meta[k] = v

        return meta



    def to_json(self) -> str:
        return json.dumps(self.get_meta())



class Dataset(ArtifactMeta):

    canonicalName: str = None
    application: str = None
    target: Optional[str] = None
    format: str = None # [json, csv, parquet, avro, ]
    versionName: str = None
    schema: dict = None
    inputDatasets: List[DataRef] = None
    context: Optional[dict] = None

    id:str = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = None # this should be set only when retrieving artifacts from DB, not on instantiation


class DataSpec(ArtifactMeta):

    canonicalName: str = None
    application: str = None
    target: Optional[str] = None
    versionName: str = None
    specVersionName: str = None
    datasetId: str = None
    artifactKind: str = "batch" # batch | record

    context: Optional[dict] = None


class DataArtifact(DataSpec):

    pipelineName: str = None
    pipelineRunId: str = None
    pipelineStage: str = None
    format: str = None # [json, csv, parquet, avro, ]

    inputDataArtifacts: List[DataRef] = Field(alias="dataRefs", default=None) # input artifacts that produced this data artifact

    artifactRef: DataRef = None # pointer to raw files in storage

    startTime: datetime.datetime = None #lower time bound of the data contained in this artifact
    endTime: datetime.datetime = None #upper time bound of the data contained in this artifact

    context: Optional[dict] = None
    metrics: Optional[dict] = None


    #internal fields
    artifactType:str = "dataArtifact"
    id:str = None


    def __init__(self, **data):

        super().__init__(**data)

        self.artifactType = "dataArtifact"

        self.id = None # this should be set only when retrieving artifacts from DB, not on instantiation





class NumericMetric(BaseMetric):
    def __init__(self, name:str, value:float):
        super().__init__(name, value)


class TaskSpec(ArtifactMeta):

    name: str = None
    dataRef: DataRef = None
    segment: Optional[Segment] = None
    prototypeRef: Optional[BaseRef] = None

    expectations: List[dict] = None
    context: Optional[dict] = None


    def get_meta(self):
        """
        :return: a dict with all the metadata fields of the task object
        """

        return self.model_dump()



class TaskArtifact(TaskSpec):

    status:int = 0
    metrics:dict = None
    message: Optional[str] = None



"""
Transformation related base objects, CodeRef
"""

class CodeRef(BaseRef):

    version:str = "1.0.0"

    def __init__(self, ref:str, refType:str, version:str = "1.0.0"):
        super().__init__(ref, refType)
        self.version = version


class TransformExecution(BaseModel):

    instance_type:str # e2-highcpu-2 etc
    provision_type: str # SPOT, STANDARD
    execution_type:str = "batch" # Batch, Sagemaker, EMR, ...
    count:int = 1
    options: Optional[Dict[Any, Any]] = None # will be sent to execution engine as is


class TransformSpec(ArtifactMeta):

    canonicalName: Union[str, Expression] = None
    application: Union[str, Expression] = None
    target: Optional[str] = None

    code: Union[CodeRef, Expression] = None
    inferenceCode: Optional[Union[CodeRef, Expression]] = None

    execution: Union[TransformExecution, Expression] = None


    parameters: Optional[dict] = None

    framework: Union[str, Expression] = None # [tensorflow, keras, sklearn, xgboost, pyspark]
    frameworkOnlyInference: Union[bool, Expression] = False # only the framework version is required to predict, no other code
    inputModality: Union[str, Expression] = None # image | text | tabular | mixed

    versionName: Union[str, Expression] = None # version name of the whole config for this model
    specVersionName: Union[str, Expression] = None # version name of the code/template for this model

    tags: Optional[Union[dict, Expression]] = None
    context: Optional[Union[dict, Expression]] = None

    artifactType:str = "transformSpec"

    def __init__(self,**data):
        super().__init__(**data)
        self.artifactType = "transformSpec"



class ModelArtifact(TransformSpec):


    pipelineName: str = None
    pipelineRunId: str = None
    pipelineStage: str = None

    deployment: str = None # whole config/spec deployment, which changes even if template is same
    specDeployment: str = None # template config/spec deployment

    inputDataArtifacts: List[DataRef] = Field(alias="dataRefs", default=None) # input artifacts that produced this artifact

    artifactBlob: BaseRef = None # pointer to raw files in storage

    checkpoint: Optional[str] = None # checkpoint name
    epoch: Optional[int] = None

    startTime: datetime.datetime = None #lower time bound of the data contained in this artifact
    endTime: datetime.datetime = None #upper time bound of the data contained in this artifact

    metrics: Optional[dict] = None


    id:str = None


    def __init__(self, **data):
        super().__init__(**data)
        self.artifactType = "modelArtifact"
        self.id = None # this should be set only when retrieving artifacts from DB, not on instantiation
