import sys
import logging
import warnings

try:
    from sklearn.base import BaseEstimator
except ImportError:
    warnings.warn('sklearn could not be imported', ImportWarning)


try:
    from pyspark.ml.regression import DecisionTreeRegressionModel
    from pyspark.ml.classification import DecisionTreeClassificationModel
except ImportError:
    warnings.warn('pyspark.ml could not be imported', ImportWarning)


try:
    import xgboost
except ImportError:
    warnings.warn('xgboost could not be imported', ImportWarning)


from typing import Mapping, List, Tuple, Dict, Type, Any


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)



class ModelMetaExtractor():

    def extract(self, estimator:Any) -> Dict[Any, Any]:
        pass

    def _get_estimator_type(self, estimator:Any) -> str:
        return str(estimator.__class__).lower()



# sklearn
class SKMetaExtractor(ModelMetaExtractor):


    def _modelClass(self, estimator):

        modelClass = None
        artifact = estimator

        if "ensemble" in self._get_estimator_type(estimator):
            modelClass = "ensemble"
        elif "tree" in self._get_estimator_type(estimator):
            modelClass = "tree"
        elif "linear" in self._get_estimator_type(estimator):
            modelClass = "linear"
        elif "svm." in self._get_estimator_type(estimator):
            modelClass = "svm"
        elif "pipeline" in self._get_estimator_type(estimator):
            modelClass = "pipeline" if not modelClass else modelClass
            logging.info("sklearn pipeline transform-class: " + str(type(estimator)))

            for transformation in estimator:
                if isinstance(transformation, BaseEstimator):
                    cls, child_transform = self._modelClass(transformation)
                    if cls:
                        modelClass = cls
                        artifact = child_transform
                        logging.info("pipeline model-class: " + str(modelClass))


        return (modelClass, artifact)



    def extract(self, estimator:Any) -> Dict[Any, Any]:
        meta = {}

        modelClass, child_estimator = self._modelClass(estimator)
        ensembleRank = len(child_estimator.estimators_) if "ensemble" == modelClass else 1
        estimatorClassName = str(type(child_estimator).__name__.split(".")[-1])


        meta["__estimator_category__"] = modelClass
        meta["__num_estimators__"] = ensembleRank
        meta["__estimator_class_name__"] = estimatorClassName
        return meta



    def getTreeFromEnsemble(self, estimator, treeIndex):
        return estimator.estimators_[treeIndex]


# pyspark
class SparkMetaExtractor(ModelMetaExtractor):

    def _modelClass(self, estimator):

        modelClass = None
        artifact = estimator

        if "forest" in self._get_estimator_type(estimator):
            modelClass = "ensemble"
        elif "gbt" in self._get_estimator_type(estimator):
            modelClass = "ensemble"
        elif "tree" in self._get_estimator_type(estimator):
            modelClass = "tree"
        elif "linear" in self._get_estimator_type(estimator):
            modelClass = "linear"


        return (modelClass, artifact)



    def extract(self, estimator:Any) -> Dict[Any, Any]:
        meta = {}

        modelClass, child_estimator = self._modelClass(estimator)
        ensembleRank = child_estimator._call_java('getNumTrees') if "ensemble" == modelClass else 1
        estimatorClassName = str(type(child_estimator).__name__.split(".")[-1])

        meta["__estimator_category__"] = modelClass
        meta["__num_estimators__"] = ensembleRank
        meta["__estimator_class_name__"] = estimatorClassName
        return meta


    def getTreeFromEnsemble(self, estimator, treeIndex):
        javaTreeModel = estimator._call_java('trees')[treeIndex]

        if "regression" in str(type(estimator)).lower():
            return DecisionTreeRegressionModel(javaTreeModel)

        # classification
        return DecisionTreeClassificationModel(javaTreeModel)






# xg boost
class XGMetaExtractor(ModelMetaExtractor):

    def extract(self, estimator:Any) -> Dict[Any, Any]:
        meta = {}
        meta["__estimator_category__"] = "ensemble"
        boosted_trees = estimator.get_dump()
        ensembleRank = len(boosted_trees)
        meta["__num_estimators__"] = ensembleRank
        meta["__estimator_class_name__"] = "XGBoost"
        return meta


# tensorflow
class TFMetaExtractor(ModelMetaExtractor):

    def extract(self, estimator:Any) -> Dict[Any, Any]:
        meta = {}
        meta["__estimator_category__"] = "neural-network"
        meta["__estimator_class_name__"] = "NeuralNetwork"
        return meta


# lightgbm
class LightGBMMetaExtractor(ModelMetaExtractor):

    def extract(self, estimator:Any) -> Dict[Any, Any]:
        meta = {}
        meta["__estimator_category__"] = "ensemble"
        meta["__estimator_class_name__"] = "LightGBM"
        meta["__num_estimators__"] = 1
        return meta


# cat boost
class CatBoostMetaExtractor(ModelMetaExtractor):

    def extract(self, estimator:Any) -> Dict[Any, Any]:
        meta = {}
        meta["__estimator_category__"] = "ensemble"
        meta["__estimator_class_name__"] = "CatBoost"
        meta["__num_estimators__"] = 1

        return meta


class ExtractorFactory:

    @staticmethod
    def get_parameter_extractor(model_type: Type[Any]) -> ModelMetaExtractor:

        extractor:ModelMetaExtractor = None

        if "sklearn" in str(model_type).lower():
            extractor = SKMetaExtractor()
        elif "pyspark" in str(model_type).lower():
            extractor = SparkMetaExtractor()
        elif "xgboost" in str(model_type).lower():
            extractor = XGMetaExtractor()
        elif "lightgbm" in str(model_type).lower():
            extractor = LightGBMMetaExtractor()
        elif "catboost" in str(model_type).lower():
            extractor = CatBoostMetaExtractor()

        elif "keras" in str(model_type).lower():
            extractor = TFMetaExtractor()
        elif "tensorflow" in str(model_type).lower():
            extractor = TFMetaExtractor()

        return extractor
