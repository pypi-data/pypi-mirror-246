import logging
import os
import warnings

# disable warnings

warnings.filterwarnings("ignore")

# disable tensorflow warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# disable bnb warnings and others

logging.getLogger().setLevel(logging.WARNING)


class CustomFilter(logging.Filter):
    def filter(self, record):
        msg = "Created a temporary directory at"
        return msg not in record.getMessage()


logger = logging.getLogger()
f = CustomFilter()
logger.addFilter(f)

from zeta.nn import *
from zeta.models import *
from zeta.utils import *
from zeta.training import *
from zeta.tokenizers import *
from zeta.rl import *
from zeta.optim import *
from zeta.ops import *
from zeta.quant import *
