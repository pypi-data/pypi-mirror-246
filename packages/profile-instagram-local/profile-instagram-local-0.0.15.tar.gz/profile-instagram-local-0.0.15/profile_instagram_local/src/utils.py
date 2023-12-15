from datetime import datetime, timedelta
from dotenv import load_dotenv
from .constants_instagram_graphql import ConstantsInstagramAPI                  # noqa: E402
load_dotenv()

from logger_local.Logger import Logger  # noqa: E402

logger = Logger.create_logger(object=ConstantsInstagramAPI.OBJECT_TO_INSERT_CODE)

INVALID_PROFILE_ID = -1


class Utils:

    @staticmethod
    def get_expiry() -> str:
        logger.start()
        # Get the current date
        current_date = datetime.now()

        # Calculate the date 59 days ahead (the actual expiry date is 60 days ahead)
        future_date = current_date + timedelta(days=59)

        # Convert the future date to a string in the desired format
        expiry = future_date.strftime("%Y-%m-%d")
        logger.end(object={'expiry': expiry})
        return expiry
