"""Offline regressions for DataArts requests and the shared MCP adapter.

No cloud credentials or live Huawei resources are used. Run with:
    python -m pytest tests/test_dataarts_compatibility.py
"""

import asyncio
import base64
import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from jsonschema import Draft202012Validator, validate
from mcp.types import CallToolRequest, CallToolRequestParams, ListToolsRequest
from requests import Response

from assets.utils.hwc_tools import (
    build_http_info,
    create_api_client,
    filter_parameters,
    load_config,
)
from assets.utils.openapi import OpenAPIToToolsConverter
from assets.utils.server import MCPServer

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "0123456789abcdef0123456789abcdef"
WORKSPACE = "test-workspace"


def config_path(service):
    return (
        ROOT
        / f"huaweicloud_services_server/mcp_server_{service}/src/mcp_server_{service}/config/config.yaml"
    )


@pytest.fixture(scope="module")
def catalog():
    result = {}
    for service in ("dataartsstudio", "cdm", "dgc", "dlf", "ecs", "rds"):
        spec = json.loads(config_path(service).with_name(f"{service}.json").read_text())
        tools = OpenAPIToToolsConverter(spec).convert()
        result[service] = (spec, tools)
    return result


def request(catalog, name, arguments, service="dataartsstudio"):
    spec, tools = catalog[service]
    return build_http_info(name, arguments, spec, tools)


def schema(catalog, name, service="dataartsstudio"):
    return next(t.inputSchema for t in catalog[service][1] if t.name == name)


@pytest.mark.parametrize(
    "service,count",
    [
        ("dataartsstudio", 410),
        ("cdm", 28),
        ("dgc", 38),
        ("dlf", 39),
    ],
)
def test_all_operations_discoverable_with_valid_schemas(catalog, service, count):
    spec, tools = catalog[service]
    assert len(tools) == len(spec["paths"]) == count
    assert len({t.name for t in tools}) == count
    assert "{region}" in spec["info"]["x-host"]
    for tool in tools:
        Draft202012Validator.check_schema(tool.inputSchema)
        assert "X-Auth-Token" not in tool.inputSchema["properties"]


def test_workspace_header_and_new_connection_filter(catalog):
    args = {
        "project_id": PROJECT,
        "workspace": WORKSPACE,
        "limit": "20",
        "offset": "0",
        "ip": "10.0.0",
    }
    validate(args, schema(catalog, "ListDataconnections"))
    info = request(catalog, "ListDataconnections", args)
    assert info["method"] == "GET"
    assert info["resource_path"] == "/v1/{project_id}/data-connections"
    assert info["path_params"] == {"project_id": PROJECT}
    assert info["header_params"]["workspace"] == WORKSPACE
    assert dict(info["query_params"]) == {"limit": "20", "offset": "0", "ip": "10.0.0"}
    assert info["body"] == {}
    assert "X-Auth-Token" not in info["header_params"]
    with pytest.raises(Exception, match="workspace"):
        request(catalog, "ListDataconnections", {"project_id": PROJECT})


def test_catalog_search_preserves_empty_arrays_and_false(catalog):
    args = {
        "project_id": PROJECT,
        "workspace": WORKSPACE,
        "query": "",
        "type_names": [],
        "limit": 10,
        "offset": 0,
        "search_all_attributes": False,
    }
    info = request(catalog, "ShowEntities", filter_parameters(args))
    assert info["method"] == "POST"
    assert info["body"] == {
        "query": "",
        "type_names": [],
        "limit": 10,
        "offset": 0,
        "search_all_attributes": False,
    }
    assert "connection_names" not in info["body"]
    assert info["header_params"]["workspace"] == WORKSPACE


def test_array_body_is_not_silently_dropped(catalog):
    tool_schema = schema(catalog, "DeleteApi")
    assert tool_schema["properties"]["request_body"]["type"] == "array"
    args = {
        "project_id": PROJECT,
        "workspace": WORKSPACE,
        "request_body": ["api-1", "api-2"],
    }
    info = request(catalog, "DeleteApi", args)
    assert info["body"] == ["api-1", "api-2"]
    assert info["path_params"]["project_id"] == PROJECT


def test_body_path_collision_retains_both_values():
    spec = {
        "paths": {
            "/Update": {
                "x-method": "put",
                "x-url": "{endpoint}/items/{id}",
                "put": {
                    "operationId": "Update",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "values": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                    },
                                }
                            }
                        },
                    },
                },
            }
        }
    }
    tools = OpenAPIToToolsConverter(spec).convert()
    args = {"id": "path-id", "request_body": {"id": "body-id", "values": []}}
    validate(args, tools[0].inputSchema)
    info = build_http_info("Update", args, spec, tools)
    assert info["path_params"] == {"id": "path-id"}
    assert info["body"] == {"id": "body-id", "values": []}


def test_subject_types_and_new_request_contract(catalog):
    spec = catalog["dataartsstudio"][0]
    assert (
        spec["components"]["schemas"]["CatalogVO"]["properties"]["parent_id"]["type"]
        == "integer"
    )
    assert (
        schema(catalog, "CreateSubjectNew")["properties"]["parent_id"]["type"]
        == "integer"
    )
    assert "entity" in schema(catalog, "CreateSubject")["properties"]
    assert spec["components"]["schemas"]["DwType"]["type"] == "string"


def test_multipart_upload_uses_bytes_not_server_file_paths(catalog):
    args = {
        "project_id": PROJECT,
        "workspace": WORKSPACE,
        "file": {
            "filename": "apis.xlsx",
            "data": base64.b64encode(b"test workbook").decode(),
        },
    }
    validate(args, schema(catalog, "ImportDataServiceExcel"))
    info = request(catalog, "ImportDataServiceExcel", args)
    assert info["header_params"]["Content-Type"] == "multipart/form-data"
    filename, stream = info["body"]["file"].convert_to_file_tuple()
    assert filename == "apis.xlsx"
    assert stream.read() == b"test workbook"
    args["file"]["data"] = "not valid base64!"
    with pytest.raises(ValueError):
        request(catalog, "ImportDataServiceExcel", args)


@pytest.mark.parametrize("service", ["dgc", "dlf"])
def test_factory_job_updates(catalog, service):
    spec = catalog[service][0]
    model = spec["components"]["schemas"]["Node"]["properties"]
    values = model["type" if service == "dgc" else "nodeType"]["enum"]
    assert "CloudTableManager" in values
    assert "CloudTableManage" not in values
    basic = spec["components"]["schemas"][
        "BasicConfig" if service == "dgc" else "BasicInfo"
    ]
    assert basic["properties"]["taskPriority"]["maximum"] == 2
    if service == "dgc":
        assert {"MRSSparkPython", "HetuEngineSQL", "RDSSQL"} <= set(values)
        info = request(
            catalog,
            "ShowJob",
            {
                "project_id": PROJECT,
                "job_name": "job",
                "workspace": WORKSPACE,
                "getJobSubmitVersion": False,
            },
            service,
        )
        assert dict(info["query_params"])["getJobSubmitVersion"] is False
        assert info["header_params"]["workspace"] == WORKSPACE


def test_cdm_new_stop_operation_and_response_typo(catalog):
    args = {
        "project_id": PROJECT,
        "cluster_id": "cluster",
        "stop": {"stopMode": "IMMEDIATELY"},
    }
    validate(args, schema(catalog, "StopCluster", "cdm"))
    info = request(
        catalog,
        "StopCluster",
        args,
        "cdm",
    )
    assert info["method"] == "POST"
    assert info["resource_path"].endswith("/clusters/{cluster_id}/action")
    assert info["body"] == {"stop": {"stopMode": "IMMEDIATELY"}}
    properties = catalog["cdm"][0]["components"]["schemas"]["Submission"]["properties"]
    assert "last-update-user" in properties
    assert "last-udpate-user" not in properties


def test_region_configuration_and_explicit_project(monkeypatch, catalog):
    monkeypatch.setenv("HUAWEI_REGION", "ap-southeast-2")
    cfg = load_config(config_path("dataartsstudio"))
    assert cfg.region == "ap-southeast-2"
    with patch("assets.utils.hwc_tools.ClientBuilder") as builder:
        create_api_client(
            "fake-ak",
            "fake-sk",
            catalog["dataartsstudio"][0]["info"]["x-host"],
            cfg.region,
            PROJECT,
        )
        credentials = builder.return_value.with_credentials.call_args.args[0]
        assert credentials.project_id == PROJECT
        region = builder.return_value.with_credentials.return_value.with_region.call_args.args[
            0
        ]
        assert region.id == "ap-southeast-2"
        assert region.endpoints == ["https://dayu.ap-southeast-2.myhuaweicloud.com"]
    monkeypatch.delenv("HUAWEI_REGION")
    assert load_config(config_path("ecs")).region == "cn-north-4"


@pytest.mark.parametrize(
    "service,name,args",
    [
        (
            "ecs",
            "ListServersDetails",
            {"project_id": PROJECT, "limit": 10, "offset": 0},
        ),
        ("rds", "ListInstances", {"project_id": PROJECT, "limit": 10, "offset": 0}),
    ],
)
def test_shared_adapter_other_service_regression(catalog, service, name, args):
    info = request(catalog, name, args, service)
    assert info["method"] == "GET"
    assert info["path_params"] == {"project_id": PROJECT}
    assert dict(info["query_params"]) == {"limit": 10, "offset": 0}
    assert info["body"] == {}


def test_mcp_handlers_discovery_call_and_file_response(monkeypatch):
    monkeypatch.setenv("HUAWEI_ACCESS_KEY", "fake-ak")
    monkeypatch.setenv("HUAWEI_SECRET_KEY", "fake-sk")
    monkeypatch.setenv("HUAWEI_REGION", "ap-southeast-2")
    server = MCPServer(config_path("dataartsstudio"))

    async def run():
        listed = await server.server.request_handlers[ListToolsRequest](
            ListToolsRequest(method="tools/list")
        )
        assert len(listed.root.tools) == 410
        args = {"project_id": PROJECT, "workspace": WORKSPACE}
        response = Response()
        response.status_code = 200
        response._content = b'{"data_connection_lists":[]}'
        response.headers["Content-Type"] = "application/json"
        client = Mock()
        client.do_http_request.return_value = response
        with patch(
            "assets.utils.server.create_api_client", return_value=client
        ) as factory:
            result = await server.server.request_handlers[CallToolRequest](
                CallToolRequest(
                    method="tools/call",
                    params=CallToolRequestParams(
                        name="ListDataconnections", arguments=args
                    ),
                )
            )
            assert not result.root.isError
            assert json.loads(result.root.content[0].text) == {
                "data_connection_lists": []
            }
            assert factory.call_args.args[3] == "ap-southeast-2"
            assert factory.call_args.kwargs["project_id"] == PROJECT
            response._content = b"\x00\xfftest"
            response.headers["Content-Type"] = "application/octet-stream"
            args.update(task_id="task", path="jobmanager")
            result = await server.server.request_handlers[CallToolRequest](
                CallToolRequest(
                    method="tools/call",
                    params=CallToolRequestParams(
                        name="DownloadTaskLog", arguments=args
                    ),
                )
            )
            payload = json.loads(result.root.content[0].text)
            assert base64.b64decode(payload["data"]) == b"\x00\xfftest"
            assert payload["encoding"] == "base64"

    asyncio.run(run())


def test_signed_bangkok_request_does_not_lookup_another_project(catalog):
    info = request(
        catalog,
        "ListDataconnections",
        {"project_id": PROJECT, "workspace": WORKSPACE, "offset": "0", "limit": "10"},
    )
    client = create_api_client(
        "fake-ak",
        "fake-sk",
        "dayu.{region}.myhuaweicloud.com",
        "ap-southeast-2",
        PROJECT,
    )
    with patch.object(client, "_do_http_request_sync", return_value=Mock()) as send:
        client.do_http_request(**info)
    signed = send.call_args.args[0]
    assert signed.host == "dayu.ap-southeast-2.myhuaweicloud.com"
    assert signed.resource_path == f"/v1/{PROJECT}/data-connections"
    assert signed.header_params["workspace"] == WORKSPACE
    assert "Authorization" in signed.header_params
    assert dict(signed.query_params) == {"offset": "0", "limit": "10"}


@pytest.mark.parametrize("status", [403, 429])
def test_cloud_errors_are_reported_not_returned_as_success(monkeypatch, status):
    from huaweicloudsdkcore.exceptions.exceptions import (
        ClientRequestException,
        SdkError,
    )

    monkeypatch.setenv("HUAWEI_ACCESS_KEY", "fake-ak")
    monkeypatch.setenv("HUAWEI_SECRET_KEY", "fake-sk")
    server = MCPServer(config_path("dataartsstudio"))
    client = Mock()
    client.do_http_request.side_effect = ClientRequestException(
        status_code=status,
        sdk_error=SdkError(
            request_id="test-request",
            error_code="TEST",
            error_msg=f"test HTTP {status}",
        ),
    )

    async def run():
        with patch("assets.utils.server.create_api_client", return_value=client):
            result = await server.server.request_handlers[CallToolRequest](
                CallToolRequest(
                    method="tools/call",
                    params=CallToolRequestParams(
                        name="ListDataconnections",
                        arguments={"project_id": PROJECT, "workspace": WORKSPACE},
                    ),
                )
            )
            assert result.root.isError
            assert str(status) in result.root.content[0].text

    asyncio.run(run())


def test_new_factory_fields_and_legacy_tools_retained(catalog):
    for name in ("CreateScript", "UpdateScript"):
        assert (
            schema(catalog, name, "dgc")["properties"]["version"]["type"] == "integer"
        )
    fields = schema(catalog, "ExportJobList", "dgc")["properties"]
    assert {"obsPath", "exportStatus"} <= fields.keys()
    assert "AuthorizeDataConnection" in {t.name for t in catalog["dataartsstudio"][1]}
    assert "DeleteConnction" in {t.name for t in catalog["dgc"][1]}


def test_recursive_schema_keeps_nested_validation():
    spec = {
        "paths": {
            "/Search": {
                "post": {
                    "operationId": "Search",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Filter"}
                            }
                        },
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "Filter": {
                    "type": "object",
                    "properties": {
                        "value": {"type": "integer"},
                        "children": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Filter"},
                        },
                    },
                    "required": ["value"],
                }
            }
        },
    }
    tool = OpenAPIToToolsConverter(spec).convert()[0]
    validate(
        {"value": 1, "children": [{"value": 2, "children": [{"value": 3}]}]},
        tool.inputSchema,
    )
    with pytest.raises(Exception, match="integer"):
        validate(
            {
                "value": 1,
                "children": [{"value": 2, "children": [{"value": "invalid"}]}],
            },
            tool.inputSchema,
        )


def test_all_local_spec_and_tool_references_resolve(catalog):
    def check(node, root):
        if isinstance(node, list):
            for value in node:
                check(value, root)
        elif isinstance(node, dict):
            assert "$ref_resolve_error" not in node
            assert "$ref_cycle_detected" not in node
            if "$ref" in node:
                assert node["$ref"].startswith("#/")
                target = root
                for key in node["$ref"][2:].split("/"):
                    target = target[key.replace("~1", "/").replace("~0", "~")]
            for value in node.values():
                check(value, root)

    for service in ("dataartsstudio", "cdm", "dgc", "dlf"):
        spec, tools = catalog[service]
        check(spec, spec)
        for tool in tools:
            check(tool.inputSchema, tool.inputSchema)


@pytest.mark.parametrize(
    "style,expected",
    [("multi", [("ids", "a"), ("ids", "b")]), ("csv", [("ids", "a,b")])],
)
def test_query_array_encoding(style, expected):
    spec = {
        "paths": {
            "/List": {
                "x-method": "GET",
                "x-url": "/items",
                "get": {
                    "operationId": "List",
                    "parameters": [
                        {
                            "name": "ids",
                            "in": "query",
                            "collectionFormat": style,
                            "schema": {"type": "array", "items": {"type": "string"}},
                        }
                    ],
                },
            }
        }
    }
    tools = OpenAPIToToolsConverter(spec).convert()
    assert (
        build_http_info("List", {"ids": ["a", "b"]}, spec, tools)["query_params"]
        == expected
    )
