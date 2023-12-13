# -*- coding: utf-8 -*-
"""
This module is used to store excel column definition information.
"""
import pathlib
import warnings

from json import loads
from sys import version_info

from typing import Any, Dict, List, Optional, TypedDict

from jira import JIRA, JIRAError
from urllib3 import disable_warnings

from .story import Story

if version_info < (3, 11):
    from typing_extensions import NotRequired, Self
else:
    from typing import NotRequired, Self


# Currently, the openpyxl package will report an obsolete warning.
warnings.simplefilter(action="ignore", category=UserWarning)
# Disable the HTTPS certificate verification warning.
disable_warnings()

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE / "assets"


class JiraFieldTypeDefinition(TypedDict):
    type: NotRequired[str]
    name: NotRequired[str]
    properties: NotRequired[List[Self]]
    isBasic: NotRequired[bool]
    arrayItemType: NotRequired[str]


_jira_field_types = []
if not _jira_field_types:
    for i in loads((ASSETS / "jira_field_type.json").read_text(encoding="utf-8")):
        _jira_field_types.append(i)


def get_jira_field(field_type: Optional[str]) -> Optional[JiraFieldTypeDefinition]:
    if field_type is None or len(field_type.strip()) == 0:
        return None
    for jira_field_type in _jira_field_types:
        if jira_field_type.get("type", "").lower() == field_type.lower():
            return jira_field_type
    return None


class JiraFieldPropertyPathDefinition(TypedDict):
    path: str
    isArray: bool


def get_field_paths_of_jira_field(
    field_type: str, field_property_name: str
) -> Optional[List[JiraFieldPropertyPathDefinition]]:
    jira_field = get_jira_field(field_type)
    if jira_field is None:
        return None
    if jira_field.get("isBasic", False) is True:
        return [{"path": field_property_name, "isArray": False}]
    result = []
    is_array_item = "arrayItemType" in jira_field
    _internal_get_field_paths_of_jira_field(
        jira_field,
        is_array_item,
        [
            {
                "path": field_property_name,
                "isArray": is_array_item,
            }
        ],
        result,
    )
    return result


def _internal_get_field_paths_of_jira_field(
    jira_field: Optional[JiraFieldTypeDefinition],
    is_array_item: bool,
    temp: List[JiraFieldPropertyPathDefinition],
    final: List[JiraFieldPropertyPathDefinition],
):
    if jira_field is None:
        return None
    if jira_field.get("isBasic", False) is True:
        for item in temp:
            final.append(
                {
                    "path": item["path"],
                    "isArray": is_array_item,
                }
            )
    if "arrayItemType" in jira_field:
        _internal_get_field_paths_of_jira_field(
            get_jira_field(jira_field["arrayItemType"]), True, temp, final
        )
    if "properties" in jira_field:
        field_properties = jira_field.get("properties", [])
        for field_property in field_properties:
            if field_property.get("arrayItemType", None) is not None:
                for item in temp:
                    item["path"] = connect_jira_field_path(
                        item["path"], field_property.get("name", "")
                    )
                _internal_get_field_paths_of_jira_field(
                    get_jira_field(field_property.get("arrayItemType")),
                    True,
                    temp,
                    final,
                )
            if field_property.get("type", None) is None:
                continue
            child_field = get_jira_field(field_property.get("type"))
            if child_field is None:
                continue
            child_field_is_basic = child_field.get("isBasic", False)
            if child_field_is_basic:
                for item in temp:
                    final.append(
                        {
                            "path": connect_jira_field_path(
                                item["path"], field_property.get("name", "")
                            ),
                            "isArray": is_array_item,
                        }
                    )
                continue
            for item in temp:
                item["path"] = connect_jira_field_path(
                    item["path"], field_property.get("name", "")
                )
            _internal_get_field_paths_of_jira_field(
                child_field, is_array_item, temp, final
            )
    return None


def connect_jira_field_path(path_a: str, path_b: str) -> str:
    return path_a + "." + path_b


class JiraClient:
    def __init__(self, url: str, access_token: str) -> None:
        self.jira = JIRA(
            server=url,
            token_auth=access_token,
            timeout=20,
            options={"verify": False},
        )
        self._field_cache: Dict[
            str, Dict[str, Optional[List[JiraFieldPropertyPathDefinition]]]
        ] = {}

    def health_check(self) -> bool:
        try:
            if self.jira.myself() is not None:
                return True
            return False
        except JIRAError:
            return False

    def create_storys(self, storys: List[Story]) -> "List[Story]":
        # self.jira.create_issues(, prefetch=true)
        return storys

    def get_all_fields(
        self,
    ) -> "Dict[str, Dict[str, Optional[List[JiraFieldPropertyPathDefinition]]]]":
        if not self._field_cache:
            for field in self.jira.fields():
                if "schema" not in field.keys():
                    continue

                temp: Dict[str, Optional[List[JiraFieldPropertyPathDefinition]]] = {
                    "id": field["id"],
                }

                class FieldSchema(TypedDict):
                    type: str
                    items: NotRequired[str]
                    custom: NotRequired[str]
                    customId: NotRequired[int]
                    system: NotRequired[str]

                schema: FieldSchema = field["schema"]
                property_name = field["id"]
                is_array = "items" in schema
                if is_array:
                    field_type = schema.get("items", None)
                else:
                    field_type = schema.get("type", None)

                if field_type is not None:
                    temp["properties"] = get_field_paths_of_jira_field(
                        field_type, property_name
                    )

                    self._field_cache[field["name"]] = temp
        return self._field_cache

    def get_stories_detail(
        self, story_ids: List[str], jira_fields: List[Dict[str, str]]
    ) -> "Dict[str, Dict[str, str]]":
        final_result = {}
        batch_size = 200

        try:
            if len(story_ids) > batch_size:
                start_index = 0
                end_index = batch_size
                while end_index <= len(story_ids) and start_index < len(story_ids):
                    # print(f"Start: {start_index}, End: {end_index}")
                    final_result.update(
                        self._internal_get_stories_detail(
                            story_ids[start_index:end_index], jira_fields
                        )
                    )
                    start_index = end_index
                    if start_index + batch_size < len(story_ids):
                        end_index = start_index + batch_size
                    else:
                        end_index = start_index + (len(story_ids) - end_index)
                return final_result

            return self._internal_get_stories_detail(story_ids, jira_fields)
        except JIRAError as e:
            print(
                f"Calling JIRA API failed. HttpStatusCode: {e.status_code}. Response: {e.response.json()}"
            )

            return {}

    def _internal_get_stories_detail(
        self, story_ids: List[str], jira_fields: List[Dict[str, str]]
    ) -> "Dict[str, Dict[str, str]]":
        id_query = ",".join([f"'{str(story_id)}'" for story_id in story_ids])

        try:
            search_result: Dict[str, Any] = self.jira.search_issues(
                jql_str=f"id in ({id_query})",
                maxResults=len(story_ids),
                fields=[field["jira_name"] for field in jira_fields],
                json_result=True,
            )  # type: ignore

            final_result = {}
            for issue in search_result["issues"]:
                fields_result = {}
                for field in jira_fields:
                    # First element in the tuple is jira field name like "customfield_13210 or status..."
                    field_name = field["jira_name"]
                    # Remain elements represent the property path.
                    field_value: Any = issue["fields"]
                    for field_path in field["jira_path"].split("."):
                        if field_value is None:
                            field_value = ""
                            break
                        field_value = field_value.get(field_path, None)
                    fields_result[field_name] = field_value
                final_result[issue["key"].lower()] = fields_result

            return final_result
        except JIRAError as e:
            print(
                f"Calling JIRA API failed. HttpStatusCode: {e.status_code}. Response: {e.response.json()}"
            )

            return {}
