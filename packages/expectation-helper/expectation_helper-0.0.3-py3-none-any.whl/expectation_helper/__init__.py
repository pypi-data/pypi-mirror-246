import bg_helper as bh
import fs_helper as fh
import settings_helper as sh
from os.path import isdir


SETTINGS = sh.get_all_settings(__name__).get(sh.APP_ENV, {})

_gx_local_repo_path = fh.abspath(SETTINGS.get('gx_local_repo_path'))
assert _gx_local_repo_path, 'The GX_LOCAL_REPO_PATH is not set'
if not isdir(_gx_local_repo_path):
    print(f'Cloning great_expectations to {_gx_local_repo_path}')
    bh.tools.git_clone(
        'https://github.com/great-expectations/great_expectations',
        _gx_local_repo_path,
        show=True
    )
