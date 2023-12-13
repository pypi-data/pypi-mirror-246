"""Cancel a finetuning run"""

from typing import List, Union

from mcli import Finetune, stop_finetuning_runs

from databricks_genai.api.config import configure_request


@configure_request
def cancel(
    finetuning_runs: Union[str, Finetune, List[str], List[Finetune]]
) -> List[Finetune]:
    """Cancel a finetuning run without deleting it"""

    if not finetuning_runs:
        raise Exception('Must provide finetuning run(s) to cancel')

    if isinstance(finetuning_runs, (str, Finetune)):
        finetuning_runs = [finetuning_runs]

    return stop_finetuning_runs(finetuning_runs=finetuning_runs)
