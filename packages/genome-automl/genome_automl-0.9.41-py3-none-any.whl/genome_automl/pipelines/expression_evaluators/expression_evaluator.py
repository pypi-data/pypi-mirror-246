
from typing import Mapping, List, Tuple, Dict, Any
from pydantic import BaseModel, Field


GOOGLE_WORKFLOW_EXPRESSION_TYPE = "google_workflows"
STEP_FUNCTION_EXPRESSION_TYPE = "step_function"


class Expression(BaseModel):

    expression:str
    expression_type:str = GOOGLE_WORKFLOW_EXPRESSION_TYPE

    def get_meta(self):
        return self.model_dump()



class ExpressionEvaluator():

    def evaluate(self, expression:str, flow_context: Dict[str,Any]) -> Any:
        pass
