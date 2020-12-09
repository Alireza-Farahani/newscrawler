from schematics import Model
from schematics.types import URLType, StringType, DateTimeType


class LiveScienceValidatorItem(Model):
    url = URLType(required=True)
    title = StringType(required=True)
    subtitle = StringType()
    content = StringType(required=True)
    author = StringType(required=True, regex="^[^,]*$")  # No comma in the name
    date = DateTimeType(required=True)
