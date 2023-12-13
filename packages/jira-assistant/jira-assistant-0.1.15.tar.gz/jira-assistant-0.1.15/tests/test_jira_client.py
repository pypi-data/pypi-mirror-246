from __future__ import annotations

import os

from requests_mock import Mocker

from jira_assistant.jira_client import (
    JiraClient,
    get_jira_field,
    get_field_paths_of_jira_field,
)
from tests.mock_server import (
    mock_jira_requests,
    mock_jira_requests_with_failed_status_code,
    mock_jira_stories,
)


def test_get_stories_detail():
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        client = JiraClient(os.environ["JIRA_URL"], os.environ["JIRA_ACCESS_TOKEN"])

        stories = client.get_stories_detail(
            ["A-1", "A-2", "B-1"],
            [
                {
                    "name": "domain",
                    "jira_name": "customfield_15601",
                    "jira_path": "customfield_15601.value",
                },
                {
                    "name": "status",
                    "jira_name": "status",
                    "jira_path": "status.name",
                },
            ],
        )
        assert len(stories) == 3


def test_get_stories_detail_with_large_amount_of_stories():
    with Mocker(real_http=False, case_sensitive=False, adapter=mock_jira_requests()):
        client = JiraClient(os.environ["JIRA_URL"], os.environ["JIRA_ACCESS_TOKEN"])

        stories = client.get_stories_detail(
            list(mock_jira_stories.keys()),
            [
                {
                    "name": "domain",
                    "jira_name": "customfield_15601",
                    "jira_path": "customfield_15601.value",
                },
                {
                    "name": "status",
                    "jira_name": "status",
                    "jira_path": "status.name",
                },
            ],
        )
        assert len(stories) == 246


def test_health_check():
    with Mocker(real_http=False, adapter=mock_jira_requests()):
        client = JiraClient(os.environ["JIRA_URL"], os.environ["JIRA_ACCESS_TOKEN"])

        assert client.health_check() is True


def test_health_check_failed():
    with Mocker(real_http=False, adapter=mock_jira_requests_with_failed_status_code()):
        client = JiraClient(os.environ["JIRA_URL"], os.environ["JIRA_ACCESS_TOKEN"])

        assert client.health_check() is False


def test_get_stories_detail_failed():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests_with_failed_status_code(),
    ):
        client = JiraClient(os.environ["JIRA_URL"], os.environ["JIRA_ACCESS_TOKEN"])

        stories = client.get_stories_detail(
            ["A-1", "A-2", "B-1"],
            [
                {
                    "name": "domain",
                    "jira_name": "customfield_15601",
                    "jira_path": "customfield_15601.value",
                },
                {
                    "name": "status",
                    "jira_name": "status",
                    "jira_path": "status.name",
                },
            ],
        )
        assert len(stories) == 0


def test_get_stories_detail_with_large_amount_of_stories_failed():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests_with_failed_status_code(),
    ):
        client = JiraClient(os.environ["JIRA_URL"], os.environ["JIRA_ACCESS_TOKEN"])

        stories = client.get_stories_detail(
            list(mock_jira_stories.keys()),
            [
                {
                    "name": "domain",
                    "jira_name": "customfield_15601",
                    "jira_path": "customfield_15601.value",
                },
                {
                    "name": "status",
                    "jira_name": "status",
                    "jira_path": "status.name",
                },
            ],
        )
        assert len(stories) == 0


def test_get_all_fields():
    with Mocker(
        real_http=False,
        case_sensitive=False,
        adapter=mock_jira_requests(),
    ):
        client = JiraClient(os.environ["JIRA_URL"], os.environ["JIRA_ACCESS_TOKEN"])

        result = client.get_all_fields()

        assert len(result) == 5


def test_get_jira_field_use_basic_type():
    assert get_jira_field(None) is None
    assert get_jira_field("abc") is None
    actual_field = get_jira_field("any")
    assert actual_field is not None
    assert "isBasic" in actual_field
    assert actual_field.get("isBasic", False) is True


def test_get_jira_field_use_complex_type():
    actual_field = get_jira_field("status")
    assert actual_field is not None
    assert "isBasic" in actual_field
    assert actual_field.get("isBasic", True) is False
    assert actual_field.get("type") == "status"
    properties = actual_field.get("properties")
    assert properties is not None
    assert "name" in [p.get("name", "") for p in properties]
    assert "statusCategory" in [p.get("name", "") for p in properties]


def test_get_field_paths_of_jira_field_use_basic_type():
    actual_field_paths = get_field_paths_of_jira_field("string", "customfield_17001")
    assert actual_field_paths is not None
    assert "customfield_17001" == actual_field_paths[0]["path"]
    assert not actual_field_paths[0]["isArray"]


def test_get_field_paths_of_jira_field_use_complex_type_no_hierarchy():
    # Author
    actual_field_paths = get_field_paths_of_jira_field("author", "abc")
    assert actual_field_paths is not None
    assert len(actual_field_paths) == 2
    assert "abc.name" in [item["path"] for item in actual_field_paths]
    assert "abc.emailAddress" in [item["path"] for item in actual_field_paths]


def test_get_field_paths_of_jira_field_use_complex_type_multiple_hierarchy():
    # Project
    actual_field_paths = get_field_paths_of_jira_field("project", "abc")
    assert actual_field_paths is not None
    assert len(actual_field_paths) == 5
    assert "abc.name" in [item["path"] for item in actual_field_paths]
    assert "abc.key" in [item["path"] for item in actual_field_paths]
    assert "abc.projectTypeKey" in [item["path"] for item in actual_field_paths]
    assert "abc.projectCategory.description" in [
        item["path"] for item in actual_field_paths
    ]
    assert "abc.projectCategory.name" in [item["path"] for item in actual_field_paths]


def test_get_field_paths_of_jira_field_use_array_type_no_hierarchy():
    # comments-page
    actual_field_paths = get_field_paths_of_jira_field("comments-page", "abc")
    assert actual_field_paths is not None
    assert len(actual_field_paths) == 5
    assert "abc.comments.author.name" in [item["path"] for item in actual_field_paths]
    assert "abc.comments.author.emailAddress" in [
        item["path"] for item in actual_field_paths
    ]
    assert "abc.comments.author.id" in [item["path"] for item in actual_field_paths]
    assert "abc.comments.author.body" in [item["path"] for item in actual_field_paths]
    assert "abc.comments.author.created" in [
        item["path"] for item in actual_field_paths
    ]
