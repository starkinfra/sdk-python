version = "1.0.0"

user = None
language = "en-US"
timeout = 15

from .user.__organization import Organization
from .user.__project import Project

from . import pixrequest
from .pixrequest.__pixrequest import PixRequest

from . import error
from . import key
