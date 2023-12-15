import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

from environment_backups import CONFIGURATION_MANAGER
from environment_backups.compression import zip_folder_with_pwd
from environment_backups.config.configuration import get_configuration_by_name
from environment_backups.exceptions import ConfigurationError

logger = logging.getLogger()


def list_all_projects(project_folder: Path) -> List[str]:
    folders = [x.path for x in os.scandir(project_folder) if x.is_dir()]
    return folders


def get_projects_envs(project_folder: Path, environment_folders: List[str]) -> Dict[str, Any]:
    folders = list_all_projects(project_folder)
    folder_dict = dict()
    for folder in folders:
        path = Path(folder)
        for environment_folder in environment_folders:
            envs = path / environment_folder
            if envs.exists():
                folder_dict[path.name] = {'envs': envs}
    return folder_dict


# TODO Add * to force use of names.
def backup_envs(
    projects_folder: Path,
    backup_folder: Path,
    environment_folders: List[str],
    password: str = None,
    date_format='%Y%m%d_%H',
) -> Tuple[List[Path], Path]:

    project_envs_dict = get_projects_envs(projects_folder, environment_folders)
    # TODO add computer name to the folder?? or the file??
    timestamp = datetime.now().strftime(date_format)
    b_folder = backup_folder / timestamp
    b_folder.mkdir(exist_ok=True)
    zip_list = []
    for project, v in project_envs_dict.items():
        zip_file = b_folder / f'{project}.zip'
        zip_folder_with_pwd(zip_file, v['envs'], password=password)
        zip_list.append(zip_file)
    return zip_list, b_folder


def backup_environment(environment_name: str) -> Tuple[List[Path], Path]:
    app_configuration = CONFIGURATION_MANAGER.get_current()
    cfg, _ = get_configuration_by_name(environment_name, app_configuration)
    if cfg is None:
        error_message = f'No environment configuration found for "{environment_name}"'
        raise ConfigurationError(error_message)
    pwd = app_configuration.get('password')
    environment_folders = app_configuration['application'].get('environment_folder_pattern')
    date_format = app_configuration['application'].get('date_format')
    project_folder = Path(cfg['project_folder'])
    backup_folder = Path(cfg['backup_folder'])
    zip_list, b_folder = backup_envs(
        projects_folder=project_folder,
        backup_folder=backup_folder,
        environment_folders=environment_folders,
        password=pwd,
        date_format=date_format,
    )
    return zip_list, b_folder
