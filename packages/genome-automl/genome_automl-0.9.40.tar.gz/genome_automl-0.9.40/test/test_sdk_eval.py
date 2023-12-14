from unittest import TestCase
from unittest.mock import patch, MagicMock

import sys
import io
import json
import pickle
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)



from ..genome_automl.core.store import StoreContext
from ..genome_automl.core.base_entity import CodeRef, DataRef, BaseMetric, TaskArtifact

from ..genome_automl.evaluations import evaluationstore
from ..genome_automl.evaluations.evaluationspec import EvaluationDimension





class TestEvaluationStoreSave(TestCase):
    @patch(evaluationstore.__name__ + '.urllib.request.urlopen')
    def test_save(self, mock_urlopen):

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = '{"id": "evaluation-run-123"}'
        cm.__enter__.return_value = cm


        mock_urlopen.side_effect = [cm]

        store = evaluationstore.EvaluationStore(StoreContext())
        evaluation = evaluationstore.EvaluationArtifact(
          canonicalName = "search/pipe-1",
          application = "search",
          code = CodeRef("ref-1", "type-1"),
          versionName = "1.0.0",
          specVersionName = "1.0.0",
          deployment = "depl-1.0.0",
          specDeployment = "spec-depl-1.0.0",
          inputModality = "tabular",
          dimension = EvaluationDimension.PERFORMANCE.value,

          status = 1,

          pipelineName = "tabular",
          pipelineStage = "step-1",
          pipelineRunId = "run-1",

          validationTarget = {"ref": "ref-1", "refType":"modelstore"},
          validationMetrics = [BaseMetric("accuracy", 0.34)],

          dataRefs = [DataRef("ref-1", "reftype-2")],

          tasks = [TaskArtifact(
              name="task-1", dataRef=DataRef("ref-1", "datastore"),
              status = 1, expectations=[{}], metrics={}
            )],

          user = "user-1",


        )
        store.save(evaluation)


        mock_urlopen.assert_called()
        # self.assertEqual(sum(2,3), 9)

        # testing metadata save being called with right extracted parameters
        evalRunMeta = json.loads(mock_urlopen.call_args_list[0][0][1])
        self.assertEqual(evalRunMeta["canonicalName"], "search/pipe-1")



    @patch(evaluationstore.__name__ + '.urllib.request.urlopen')
    def test_load_evaluation(self, mock_urlopen):

        evaluation = evaluationstore.EvaluationArtifact(
          canonicalName = "search/pipe-1",
          application = "search",
          code = CodeRef("ref-1", "type-1"),
          versionName = "1.0.0",
          specVersionName = "1.0.0",
          deployment = "depl-1.0.0",
          specDeployment = "spec-depl-1.0.0",
          inputModality = "tabular",
          dimension = EvaluationDimension.PERFORMANCE.value,

          status = 1,

          pipelineName = "tabular",
          pipelineStage = "step-1",
          pipelineRunId = "run-1",

          validationTarget = {"ref": "ref-1", "refType":"modelstore"},
          validationMetrics = [BaseMetric("accuracy", 0.34)],

          dataRefs = [DataRef("ref-1", "reftype-2")],

          tasks = [TaskArtifact(
              name="task-1", dataRef=DataRef("ref-1", "datastore"),
              status = 1, expectations=[{}], metrics={}
            )],

          user = "user-1",

        )

        evaluation.id = "eval-123"

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = json.dumps([evaluation.model_dump()])
        cm.__enter__.return_value = cm


        mock_urlopen.side_effect = [cm]


        store = evaluationstore.EvaluationStore(StoreContext())


        evaluation_resp = store.load({
          "canonicalName":"/search/pipeline",
          "application": "search"
        })

        mock_urlopen.assert_called()


        self.assertEqual(evaluation_resp["id"], "eval-123")

        # self.assertEqual(sum(2,3), 9)

        # testing metadata call with right extracted parameters
        self.assertEqual(len(mock_urlopen.call_args_list), 1)

        modelMeta = json.loads(mock_urlopen.call_args_list[0][0][1])
        self.assertEqual(modelMeta["application"], "search")
        self.assertEqual(modelMeta["canonicalName"], "/search/pipeline")
