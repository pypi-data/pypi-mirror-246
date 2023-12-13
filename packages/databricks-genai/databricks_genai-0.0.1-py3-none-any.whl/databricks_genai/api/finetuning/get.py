"""Get finetuning runs"""

from datetime import datetime
from typing import List, Optional, Union

from mcli import Finetune, RunStatus, get_finetuning_runs

from databricks_genai.api.config import configure_request


@configure_request
def get(
    finetuning_runs: Optional[Union[str, Finetune, List[str],
                                    List[Finetune]]] = None,
    *,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    user_emails: Optional[List[str]] = None,
    before: Optional[Union[str, datetime]] = None,
    after: Optional[Union[str, datetime]] = None,
    limit: int = 50,
) -> List[Finetune]:
    """Get a finetuning run"""
    if isinstance(finetuning_runs, (str, Finetune)):
        finetuning_runs = [finetuning_runs]

    return get_finetuning_runs(
        finetuning_runs=finetuning_runs,
        statuses=statuses,
        user_emails=user_emails,
        before=before,
        after=after,
        include_details=True,
        limit=limit,
    )
