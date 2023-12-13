"""Create a finetuning run"""

from typing import Optional

from mcli import Finetune, create_finetuning_run

from databricks_genai.api.config import configure_request, get_me


@configure_request
def create(
    model: str,
    train_data_path: str,
    model_registry_path: str,
    experiment_path: Optional[str] = None,
    save_folder: Optional[str] = None,
) -> Finetune:
    """Create a finetuning run"""
    databricks_username = get_me()
    experiment_tracker = {
        'integration_type': 'mlflow',
        'experiment_name': f'Users/{databricks_username}/{experiment_path}',
        'model_registry_uri': model_registry_path,
    }

    if save_folder:
        # TODO
        # save_folder='mlflow://{{mlflow_run_id}}/checkpoints/',
        print(
            'WARNING: save_folder support will be removed shortly. This field is intended for testing only'
        )
    return create_finetuning_run(
        model=model,
        train_data_path=train_data_path,
        save_folder=save_folder,
        experiment_trackers=[experiment_tracker],
        disable_credentials_check=True,
    )
