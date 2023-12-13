"""Delete a finetuning run"""

from typing import List, Union

from mcli import Finetune, delete_finetuning_runs

from databricks_genai.api.config import configure_request


@configure_request
def delete(
    finetuning_runs: Union[str, Finetune, List[str], List[Finetune]]
) -> List[Finetune]:
    """Cancel and delete a finetuning run"""
    if not finetuning_runs:
        raise Exception('Must provide finetuning run(s) to delete')

    if isinstance(finetuning_runs, (str, Finetune)):
        finetuning_runs = [finetuning_runs]

    return delete_finetuning_runs(finetuning_runs=finetuning_runs)
