import json
import logging
import os

from django import template
from django.conf import settings
from django.contrib.gis.geos import Point
from utils.datetime import stringdatetime_naar_datetime

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def replace_comma_by_dot(value):
    return str(value).replace(",", ".")


@register.filter
def to_datetime(value):
    if value and isinstance(value, str):
        return stringdatetime_naar_datetime(value)
    return value


@register.filter
def to_timestamp(value):
    try:
        return int(value.timestamp())
    except Exception as e:
        logger.error(f"No datatime instance, value={value}: error={e}")


@register.filter
def json_encode(value):
    if isinstance(value, Point):
        return value.geojson
    return json.dumps(value)


@register.filter
def json_loads(value):
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return None


@register.filter
def replace_n(value):
    return value.replace("\\n", "<br/>").replace("?", "?<br/>")


@register.simple_tag
def vind_in_dict(op_zoek_dict, key):
    if not isinstance(op_zoek_dict, dict):
        return key
    result = op_zoek_dict.get(key, op_zoek_dict.get(str(key), key))
    if isinstance(result, (list, tuple)):
        return result[0]
    return result


@register.filter
def adres_order_nummer(taak, taken_sorted):
    return taken_sorted.get(taak.id, taak.id)


@register.filter(name="python_any")
def python_any(values):
    if values:
        return any(values)
    return values


@register.filter
def file_exists(file_path):
    return os.path.isfile(
        os.path.join(settings.BASE_DIR, "apps/main/templates/", file_path)
    )
