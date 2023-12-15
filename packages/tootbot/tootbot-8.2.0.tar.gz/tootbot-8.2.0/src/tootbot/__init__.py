"""Package 'tootbot' level definitions."""
import sys
from typing import Final
from typing import List
from typing import Tuple

from asyncpraw.models import Submission
from typing_extensions import TypeAlias

__version__: Final[str] = "8.2.0"
__display_name__: Final[str] = "Tootbot"
__package_name__: Final[str] = __display_name__.lower()

# Package level Static Variables
POST_RECORDER_SQLITE_DB: Final[str] = "history.db"
POST_RECORDER_HISTORY_RETENTION_DAYS: Final[int] = 31
USER_AGENT: Final[str] = __display_name__
CLIENT_WEBSITE: Final[str] = "https://pypi.org/project/tootbot/"
PROGRESS_BAR_FORMAT: Final[str] = "{desc}: {percentage:3.0f}%|{bar}| Eta: {remaining} - Elapsed: {elapsed}"
FATAL_TOOTBOT_ERROR: Final[str] = "Tootbot cannot continue, now shutting down"
VERSION_DEBUG: Final[str] = f"{__display_name__}_{__version__}_Python_{sys.version.split()[0]}"

SubmissionId: TypeAlias = str
Tags: TypeAlias = str
RedditPostsList: TypeAlias = List[Tuple[SubmissionId, Tags, Submission]]
