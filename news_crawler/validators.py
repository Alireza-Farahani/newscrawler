from schematics import Model
from schematics.types import URLType, StringType, DateTimeType


class REGEX:
    NO_COMMA = "^[^,]*$"


class LiveScienceValidatorItem(Model):
    url = URLType(required=True)
    title = StringType(required=True)
    content = StringType(required=True)
    date = DateTimeType(required=True)
    subtitle = StringType()
    author = StringType(required=True, regex=REGEX.NO_COMMA)  # No comma in the name


class ScienceAlertValidatorItem(Model):
    url = URLType(required=True)
    title = StringType(required=True)
    content = StringType(required=True)
    date = DateTimeType(required=True)
    author = StringType(required=True, regex=REGEX.NO_COMMA)
    source = URLType()              # TODO: coverage 25%


class ScienceDailyValidatorItem(Model):
    url = URLType(required=True)
    title = StringType(required=True)
    content = StringType(required=True)
    date = DateTimeType(required=True)
    source = StringType(required=True)
    subtitle = StringType(required=True)
    source_article_url = URLType()  # TODO: coverage 25%


class ScienceNewsValidatorItem(Model):
    url = URLType(required=True)
    title = StringType(required=True)
    content = StringType(required=True)
    date = DateTimeType(required=True)
    subtitle = StringType(required=True)
    author = StringType(required=True, regex=REGEX.NO_COMMA)


class ScientificAmericanValidatorItem(Model):
    url = URLType(required=True)
    title = StringType(required=True)
    content = StringType(required=True)
    date = DateTimeType(required=True)
    subtitle = StringType(required=True)
    author = StringType(required=True, regex=REGEX.NO_COMMA)
