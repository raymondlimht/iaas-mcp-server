# DataArts Studio compatibility audit

Audited **2026-11-20**, targeting **AP-Bangkok (`ap-southeast-2`)**. Scope: Management Center, Factory (DataArts/DGC/DLF), Architecture, Quality, Catalog, DataService, Security and Migration/CDM. Fabric, Insight, deployment and ontology implementation are excluded.

## Baseline and evidence

- Fork: [raymondlimht/iaas-mcp-server](https://github.com/raymondlimht/iaas-mcp-server), preserving upstream history, licensing and attribution.
- Upstream baseline: [`90837ff7658d`](https://github.com/huaweicloud-samples/iaas-mcp-server/commit/90837ff7658dd0fa9977daa4bf5ba5e7a6826a37) (2026-02-11). Repository inactivity is not proof of formal abandonment.
- **D — International API Reference**, Issue 01, 2026-09-17: [official PDF](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf). All **385 API leaf sections** in chapters 4–11 were inventoried; chapter 4.4's 36 migration parameter-reference sections are not separate operations. **359** sections map to bundled tools below; **26** are explicitly unresolved below. Duplicate/alternative routes can map to one tool. PDF SHA-256: `c66b06887c7fbddb829fca3ed4b866bf97c90b1e232a16ac58eff2ff3c8690f0`.
- **E — International API Explorer**, retrieved 2026-11-20: [DataArtsStudio catalogue](https://console-intl.huaweicloud.com/apiexplorer/v3/apis?product_short=DataArtsStudio&limit=100&offset=0) (**409** operations, paginated in batches of 100) and [CDM catalogue](https://console-intl.huaweicloud.com/apiexplorer/v3/apis?product_short=CDM&limit=100&offset=0) (**28**). Each E link below identifies the operation-specific Swagger source used for parameters, bodies and responses. DGC/DLF catalogue queries returned no operations; use S/D there. A SHA-256 of the sorted `product/name.json SHA-256` manifest of all 437 retrieved schemas is `7b98f5dff0ae3c0b5f1b771a3b36f25e7061a37ed403a12d20f29c292ee66aa7` (newline-separated, no trailing newline).
- **S — Official Huawei Python SDK 3.1.223**, released 2026-11-19, commit [`649cc7a63af8`](https://github.com/huaweicloud/huaweicloud-sdk-python-v3/commit/649cc7a63af8904b8ea476cb68f374dd59a4a8e6): [DataArtsStudio](https://github.com/huaweicloud/huaweicloud-sdk-python-v3/blob/649cc7a63af8904b8ea476cb68f374dd59a4a8e6/huaweicloud-sdk-dataartsstudio/huaweicloudsdkdataartsstudio/v1/dataartsstudio_client.py) (413 operations), [CDM](https://github.com/huaweicloud/huaweicloud-sdk-python-v3/blob/649cc7a63af8904b8ea476cb68f374dd59a4a8e6/huaweicloud-sdk-cdm/huaweicloudsdkcdm/v1/cdm_client.py) (28), [DGC](https://github.com/huaweicloud/huaweicloud-sdk-python-v3/blob/649cc7a63af8904b8ea476cb68f374dd59a4a8e6/huaweicloud-sdk-dgc/huaweicloudsdkdgc/v1/dgc_client.py) (31), [DLF](https://github.com/huaweicloud/huaweicloud-sdk-python-v3/blob/649cc7a63af8904b8ea476cb68f374dd59a4a8e6/huaweicloud-sdk-dlf/huaweicloudsdkdlf/v1/dlf_client.py) (39); models in each module's `v1/model/` and [changelog](https://github.com/huaweicloud/huaweicloud-sdk-python-v3/blob/649cc7a63af8904b8ea476cb68f374dd59a4a8e6/CHANGELOG.md). SDK coverage documentation directs Migration to [CDM](https://support.huaweicloud.com/intl/en-us/sdkreference-dataartsstudio/dataartsstudio_06_0002.html).

“Aligned” below means no difference found in the compared published contract, **not a successful cloud call**. E comparisons cover method/URI, parameter locations/types/required flags, request and response schemas and media types, ignoring prose, examples, ordering and vendor documentation extensions. SDK checks cover operation/method/URI, parameter locations, nested request/response field presence and relevant changelog changes; they do not establish every SDK model constraint. The PDF provides the independent operation inventory and spot checks; every PDF parameter table was not independently revalidated against E. Source conflicts remain explicit rather than being guessed away.

## Result and focused changes

| Server | Before | After | Coverage |
|---|---:|---:|---|
| DataArtsStudio | 373 | 410 | All 409 Explorer operations + retained `AuthorizeDataConnection` |
| CDM | 27 | 28 | All 28 Explorer/SDK operations; added `StopCluster` |
| DGC | 38 | 38 | All 31 current SDK operations + 7 legacy connection operations |
| DLF | 39 | 39 | All 39 current SDK operations |

**515 tools retained or supplied; 38 operations added.** Ledger status totals: 317 aligned, 7 deprecated; retained, 1 unresolved; retained, 152 updated, 38 updated (added). A shared-schema change counts each affected operation as updated. All existing tool names remain, including upstream spellings.

- Refreshed only differing DataArts/CDM definitions from E. Examples include connection `ip` filtering, Architecture subject/entity types, Catalog search/lineage models, Factory package/baseline APIs, Security models and Migration APIs. Added definitions are included only as dependencies of current operations. Removed four dangling `#/responses/...` schemas in `ListAllStandards` errors (400/401/403/404); E also supplies no resolvable error schema, so the response shape remains unspecified.
- DGC/DLF changes follow S: job priority, corrected `CloudTableManager`/DGC node-type enums, warning/task statuses, real-time status fields, script versions, submitted-job query selection and export options. CDM corrects `last-update-user` and current cluster models. Seven legacy DGC connection tools are retained and marked deprecated; Huawei [documents their replacement by Management Center](https://support.huaweicloud.com/intl/en-us/ally-visitor-1-api-dataartsstudio/apiOverview_DLF_V1.html).
- Shared adapter now exposes documented `workspace` and other service headers while leaving signing headers to the existing SDK; sends proper SDK query tuples, repeated query values and selected media types; omits absent optional values while retaining `false`, `0` and empty arrays; preserves recursive Catalog/filter schemas; separates body/path name collisions; and supports multipart imports plus non-JSON exports. These changes are needed by DataArts and have ECS/RDS regression coverage.
- Added the missing `mcp-server-dataartsstudio` entry point. Added only `mcp>=1.8.0,<2`: the existing imports use MCP 1.x APIs removed in MCP 2.x. A fresh unconstrained installation reproduced startup failure; the bounded installation starts successfully. No repository-wide dependency upgrades or lockfile changes.
- Added `HUAWEI_REGION` / YAML `region`, retaining `cn-north-4` as the existing default; the pre-existing per-call region override still takes precedence. Pass the request's project ID to SDK credentials so it is not independently inferred from another project. Added DGC's missing `dayu.{region}.myhuaweicloud.com` host.

## Bangkok and unresolved verification

The [official region map](https://github.com/huaweicloud/huaweicloud-sdk-python-v3/blob/649cc7a63af8904b8ea476cb68f374dd59a4a8e6/huaweicloud-sdk-dataartsstudio/huaweicloudsdkdataartsstudio/v1/region/dataartsstudio_region.py) lists `dayu.ap-southeast-2.myhuaweicloud.com`; DGC uses `dayu`, CDM uses `cdm`, and DLF uses `dayu-dlf`, as listed in their SDK region maps. Endpoint listing alone does not establish component entitlement, edition support, workspace availability or operation availability in Bangkok. **Every operation remains region-dependent until tested against the intended Bangkok resources.**

Explorer's explicit `region_id=ap-southeast-2` query for `ListDataconnections` returned HTTP 400 / `APIEXPLORER.1055` (“API information is empty”). Generic Explorer queries succeeded but returned metadata for other regions. Therefore E is a published contract reference, not Bangkok certification. Security's 86 operations are published in E/S but have no chapter in the examined International PDF; regional/product-edition support is unresolved.

No live Huawei API tests were performed: suitable Bangkok credentials, project, DataArts instance/workspace and component resources were not supplied. No cloud resources were changed. Automated signing used fake keys with network dispatch mocked. Live verification must separately establish read/pagination behavior and explicitly chosen write/import/export operations against suitable resources; offline tests cannot certify those effects.

Other source discrepancies:

- `AuthorizeDataConnection` disappeared from E and was removed from S in 3.1.214. Its original tool remains with a caution. SDK removal does not prove service-side retirement.
- `ListDataconnections`: the International [HTML reference](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/ListDataconnections.html) mentions a `service` query filter absent from E/S. It is not added without source reconciliation; current E/S filters are implemented.
- `ListFactoryReleasePackages`, `ShowFactoryPackageDetail`, `ShowFactorySupplementData`: SDK `X-request-id` fields are response headers, not missing JSON fields; no invented body properties were added.
- Four SDK-only operations below have no retrieved E contract or matching API section in D. They are not added pending published regional contract confirmation. This is an unresolved coverage gap, not an assertion that they are unsupported.

| SDK-only operation | Method / URI | Status |
|---|---|---|
| `CreateFactoryEnv` | `PUT /v2/{project_id}/factory/env` | unresolved; not bundled |
| `CreateFactoryJob` | `POST /v2/{project_id}/factory/jobs` | unresolved; not bundled |
| `ListFactoryJobs` | `GET /v2/{project_id}/factory/jobs` | unresolved; not bundled |
| `ShowFactoryEnv` | `GET /v2/{project_id}/factory/env` | unresolved; not bundled |

The following **26 International-reference operations** have no matching bundled, Explorer or SDK route. They are individually accounted for as **unresolved; not bundled**. Their PDF descriptions establish their existence in that reference, but published machine-readable contracts and Bangkok availability could not be reconciled. No speculative tool names or request schemas were introduced.

<details>
<summary>26 documentation-only routes (PDF section and page)</summary>

| Section | Page | Method / URI |
|---|---:|---|
| 7.3.4 Freezing a Workspace | [760](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=760) | `POST /v1/{project_id}/{instance_id}/workspace/{workspace_id}/frozen-workspace` |
| 7.3.5 Unfreezing a Workspace | [762](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=762) | `POST /v1/{project_id}/{instance_id}/workspace/{workspace_id}/unfrozen-workspace` |
| 7.3.6 Editing a Workspace | [764](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=764) | `PUT /v1/{project_id}/{instance_id}/update-workspace/{workspace_id}` |
| 8.8.5 Querying Details of a Topic | [1323](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=1323) | `GET /v2/{project_id}/design/subjects/{id}` |
| 8.26.1 Previewing SQL Statements | [3064](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3064) | `GET /v1/{project_id}/design/table/{tb_id}/ddl` |
| 8.28.8 Querying the Lookup Table Reversing Result | [3209](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3209) | `GET /v1/{project_id}/code-tables/database` |
| 8.28.9 Reversing a Lookup Table | [3214](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3214) | `POST /v1/{project_id}/code-tables/database` |
| 9.3.4 Starting or Stopping a Quality Job | [3278](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3278) | `POST /v2/{project_id}/quality/quality-tasks/action` |
| 9.3.5 Deleting Quality Jobs | [3281](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3281) | `POST /v2/{project_id}/quality/quality-tasks/batch-delete` |
| 9.4.3 Deleting Comparison Jobs | [3297](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3297) | `POST /v2/{project_id}/quality/consistency-tasks/batch-delete` |
| 9.5.3 Data quality O&M management operation processing and recording | [3311](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3311) | `PUT /v2/{project_id}/quality/instances/{instance_id}` |
| 9.6.1 Rerunning a Quality Job or Comparison Job | [3314](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3314) | `POST /v2/{project_id}/quality/instances/restart` |
| 9.7.1 Obtaining a Quality Report Scoring System | [3317](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3317) | `GET /v2/{project_id}/quality/report/scoring` |
| 9.7.2 Obtaining the Quality Report Overview | [3319](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3319) | `GET /v2/{project_id}/quality/report/overview` |
| 9.7.3 Obtaining the Quality Report Trend | [3322](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3322) | `GET /v2/{project_id}/quality/report/trend` |
| 9.7.4 Obtaining the Quality Report Rules | [3326](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3326) | `GET /v2/{project_id}/quality/report/rules` |
| 9.7.5 Obtaining Sub-rule Fields of a Quality Report | [3329](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3329) | `GET /v2/{project_id}/quality/report/sub-rule/results` |
| 9.7.6 Obtaining the Technical Report Data | [3333](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3333) | `GET /v2/{project_id}/quality/report/technology/scores` |
| 9.7.7 Obtaining the Business Report Data | [3337](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3337) | `GET /v2/{project_id}/quality/report/business/scores` |
| 9.8.1 Export Resources | [3341](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3341) | `POST /v2/{project_id}/quality/resource/export` |
| 9.8.2 Obtaining the Status of an Import/Export Task | [3344](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3344) | `GET /v2/{project_id}/quality/resource/status/{resource_id}` |
| 9.8.3 Downloading a Resource File | [3347](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3347) | `GET /v2/{project_id}/quality/resource/download` |
| 9.8.4 Uploading a Resource File | [3349](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3349) | `POST /v2/{project_id}/quality/resource/upload` |
| 9.8.5 Importing Resources | [3352](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3352) | `POST /v2/{project_id}/quality/resource/import` |
| 9.9.1 Stopping Instances | [3355](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=3355) | `POST /v2/{project_id}/quality/instances/batch-stop` |
| 11.10.1 Obtaining the Reviewer List | [4120](https://support.huaweicloud.com/intl/en-us/api-dataartsstudio/api-dataartsstudio-pdf.pdf#page=4120) | `GET /v1/{project_id}/service/authorizeapply/approver` |

</details>

## Input compatibility and local use

Set `HUAWEI_REGION=ap-southeast-2` alongside the existing `HUAWEI_ACCESS_KEY` and `HUAWEI_SECRET_KEY` environment variables, then run `mcp-server-dataartsstudio -t stdio` from an installation of this fork. Supply the Bangkok `project_id` and the documented `workspace` header value in tool arguments. Factory/Migration operations also remain in the existing `mcp-server-dgc`, `mcp-server-dlf` and `mcp-server-cdm` commands. No new credentials mechanism or permissions layer is introduced.

Tool names and existing flat body fields are preserved wherever representable. Intentional input corrections:

- Previously omitted required service headers must now be supplied; missing values fail locally instead of sending incomplete requests.
- Current E/S field types and enum spellings replace incorrect/removed spellings. Existing callers using those invalid values need to follow the newly discovered schema.
- Array/scalar/free-form bodies and bodies whose fields collide with path/query/header names use `request_body`; path/header/query fields remain top-level. This changes the previously unusable/ambiguous input shape for: `CreateSecurityPermissionSetMember`, `UpdateStandard`, `AssociateClassificationToEntity`, `UpdateTemplate`, `UpdateTaskInfo`, `UpdateCodeTable`, `ImportLineage`, `BatchSyncMetadata`, `CreateDesignDerivativeIndex`, `DeleteClassificationFromEntities`, `ExportDataServiceExcel`, `CreateTask`, `DeleteApi`, `ListEntityDetails`. Example: `DeleteApi` accepts the IDs array as `request_body`, while `UpdateStandard` keeps the URL ID separate from its body.
- Multipart file fields accept `{"filename":"import.xlsx","data":"<base64>"}`. Binary responses return a JSON envelope with `content_type`, `encoding: "base64"`, and `data`; text responses are returned as JSON strings. Existing JSON responses retain their shape.

## Automated verification

Validated on Python 3.10.21 with MCP 1.30.0, FastMCP 3.4.11 and Huawei SDK core 3.1.223:

- **25 passing offline tests** in `tests/test_dataarts_compatibility.py`: all 515 DataArts/CDM/DGC/DLF tool schemas and internal references, recursive validation, workspace headers, paths, optional values, bodies, query arrays, offset/limit pagination mapping, multipart encoding, download responses, Factory changes, mocked 403/429 errors, Bangkok signing/project selection, and representative ECS/RDS mappings. This is representative request coverage, not a live call for every operation or pagination traversal.
- Installed command `--help`, real stdio MCP `initialize` and `tools/list`: **410 unique DataArts tools**, no schema-reference errors. Dependency consistency check passes.
- New test-file lint passes. Full-repository lint reports 82 findings; the 56 findings in modified shared files are unchanged from baseline. The inherited lint workflow therefore is not green; unrelated cleanup is excluded. Existing file formatting was preserved except touched code.
- Definition comparison: all 437 E operations match after resolving schemas and normalizing non-contract metadata, except the four explicitly removed invalid `ListAllStandards` error references. All matched S methods/routes and request-parameter locations align; nested SDK model field presence has no unexplained omissions.

Reproduce offline tests from the repository root after installation:

```sh
python -m pip install -e . pytest jsonschema
python -m pytest -q tests/test_dataarts_compatibility.py
mcp-server-dataartsstudio --help
```

## Complete operation ledger

Each bundled operation appears once below. E/S/D refer to the pinned/retrieved sources above; D numbers are PDF sections. **No ledger row is live-verified; all rows carry the Bangkok regional qualification above.** Together with the 30 unresolved routes/operations above, this accounts for every operation found in the compared source snapshots. “Aligned” for DGC/DLF means SDK/route/field checks at the scope stated above, not a full independent PDF constraint audit.

<details>
<summary>DATAARTSSTUDIO: 410 bundled operations</summary>

| Operation | Component | Status | Evidence |
|---|---|---|---|
| `AcceptSecurityApplication` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=AcceptSecurityApplication) + S |
| `AddDesignEntityTags` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=AddDesignEntityTags) + S + D 8.27.1 |
| `AddTagToAsset` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=AddTagToAsset) + S + D 10.10.2 |
| `AddWorkSpaceUsers` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=AddWorkSpaceUsers) + S + D 7.5.4 |
| `ApplySecurityTableAuthority` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ApplySecurityTableAuthority) + S |
| `AssociateClassificationToEntity` | Catalog | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=AssociateClassificationToEntity) + S + D 10.5.2 |
| `AssociateConnectionCluster` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=AssociateConnectionCluster) + S |
| `AssociateSecurityLevelToEntitie` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=AssociateSecurityLevelToEntitie) + S + D 10.6.2 |
| `AuthorizeActionApiToInstance` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=AuthorizeActionApiToInstance) + S + D 11.1.10 |
| `AuthorizeApiToInstance` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=AuthorizeApiToInstance) + S + D 11.1.8 |
| `AuthorizeDataConnection` | Catalog | unresolved; retained | baseline / SDK removal note |
| `BatchApproveApply` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchApproveApply) + S + D 11.2.2 |
| `BatchApproveSecurityApplications` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchApproveSecurityApplications) + S |
| `BatchAssociateClassificationToEntities` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchAssociateClassificationToEntities) + S + D 10.5.1 |
| `BatchAssociateSecurityLevelToEntities` | Catalog | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchAssociateSecurityLevelToEntities) + S + D 10.6.1 |
| `BatchBindMigrationResourceToWorkspace` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchBindMigrationResourceToWorkspace) + S + D 7.8.1 |
| `BatchCreateDesignTableModelsFromLogic` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchCreateDesignTableModelsFromLogic) + S + D 8.21.16 |
| `BatchCreateSecurityPermissionSetMembers` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchCreateSecurityPermissionSetMembers) + S |
| `BatchCreateSecurityPermissionSetPermissions` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchCreateSecurityPermissionSetPermissions) + S |
| `BatchDeleteSecurityDataCategories` | Security | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchDeleteSecurityDataCategories) + S |
| `BatchDeleteSecurityDataClassificationRule` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchDeleteSecurityDataClassificationRule) + S |
| `BatchDeleteSecurityDynamicMaskingPolicies` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchDeleteSecurityDynamicMaskingPolicies) + S |
| `BatchDeleteSecurityPermissionSetMembers` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchDeleteSecurityPermissionSetMembers) + S |
| `BatchDeleteSecurityPermissionSetPermissions` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchDeleteSecurityPermissionSetPermissions) + S |
| `BatchDeleteSecurityResourcePermissionPolicies` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchDeleteSecurityResourcePermissionPolicies) + S |
| `BatchDeleteSecuritySecrecyLevels` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchDeleteSecuritySecrecyLevels) + S |
| `BatchDeleteTemplates` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchDeleteTemplates) + S + D 9.2.5 |
| `BatchDeleteWorkspaces` | Management Center | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchDeleteWorkspaces) + S + D 7.3.8 |
| `BatchOffline` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchOffline) + S + D 8.7.5 |
| `BatchPublish` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchPublish) + S + D 8.7.4 |
| `BatchRejectSecurityApplications` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchRejectSecurityApplications) + S |
| `BatchSyncMetadata` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchSyncMetadata) + S + D 10.9.1 |
| `BatchTag` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchTag) + S + D 10.9.12 |
| `BatchUpdateSecurityDlfDataWareHouses` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=BatchUpdateSecurityDlfDataWareHouses) + S |
| `CancelFactoryPackages` | Factory | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CancelFactoryPackages) + S + D 6.2.12 |
| `ChangeCatalog` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ChangeCatalog) + S + D 8.5.4 |
| `ChangeResource` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ChangeResource) + S + D 7.7.1 |
| `ChangeSubjects` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ChangeSubjects) + S + D 8.9.2 |
| `CheckDimensionStatus` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CheckDimensionStatus) + S + D 8.14.7 |
| `CheckFactLogicTableStatus` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CheckFactLogicTableStatus) + S + D 8.17.4 |
| `CheckSecurityDataClassificationCombineRule` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CheckSecurityDataClassificationCombineRule) + S |
| `CompareDesignVersions` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CompareDesignVersions) + S + D 8.20.2 |
| `ConfirmApprovals` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ConfirmApprovals) + S + D 8.7.3 |
| `ConfirmMessage` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ConfirmMessage) + S + D 11.3.2 |
| `CountAllModels` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CountAllModels) + S + D 8.1.3 |
| `CountOverviews` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CountOverviews) + S + D 8.1.1 |
| `CountStandards` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CountStandards) + S + D 8.1.4 |
| `CountTableModels` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CountTableModels) + S + D 8.1.2 |
| `CreateApi` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateApi) + S + D 11.1.1 |
| `CreateApp` | DataService | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateApp) + S + D 11.7.1 |
| `CreateApprover` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateApprover) + S + D 8.7.6 |
| `CreateBizMetric` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateBizMetric) + S + D 8.19.2 |
| `CreateCatalog` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateCatalog) + S + D 8.5.3 |
| `CreateCluster` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateCluster) + S |
| `CreateCodeTable` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateCodeTable) + S + D 8.28.2 |
| `CreateConnections` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateConnections) + S + D 7.1.3 |
| `CreateDatasourceConnection` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateDatasourceConnection) + S |
| `CreateDatasourceConnectionRoutes` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateDatasourceConnectionRoutes) + S |
| `CreateDesignAggregationLogicTable` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateDesignAggregationLogicTable) + S + D 8.18.2 |
| `CreateDesignAtomicIndex` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateDesignAtomicIndex) + S + D 8.11.2 |
| `CreateDesignCompoundMetric` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateDesignCompoundMetric) + S + D 8.13.2 |
| `CreateDesignDerivativeIndex` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateDesignDerivativeIndex) + S + D 8.12.2 |
| `CreateDesignDimension` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateDesignDimension) + S + D 8.14.2 |
| `CreateDirectory` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateDirectory) + S + D 8.10.2 |
| `CreateFactoryBaseline` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateFactoryBaseline) + S |
| `CreateFactoryPendingItemsPackage` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateFactoryPendingItemsPackage) + S + D 6.2.6 |
| `CreateFactorySupplementDataInstance` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateFactorySupplementDataInstance) + S + D 6.2.1 |
| `CreateLineageInfo` | Catalog | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateLineageInfo) + S + D 10.7.1 |
| `CreateManagerWorkSpace` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateManagerWorkSpace) + S + D 7.3.2 |
| `CreateOrUpdateAsset` | Management Center | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateOrUpdateAsset) + S + D 10.4.3 |
| `CreateOrUpdateEntities` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateOrUpdateEntities) + S + D 10.9.5 |
| `CreateSecurityAssignedQueue` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityAssignedQueue) + S |
| `CreateSecurityDataCategory` | Security | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityDataCategory) + S |
| `CreateSecurityDataClassificationCombineRule` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityDataClassificationCombineRule) + S |
| `CreateSecurityDataClassificationRule` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityDataClassificationRule) + S |
| `CreateSecurityDataClassificationRuleGroup` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityDataClassificationRuleGroup) + S |
| `CreateSecurityDynamicMaskingPolicy` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityDynamicMaskingPolicy) + S |
| `CreateSecurityPermissionSet` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityPermissionSet) + S |
| `CreateSecurityPermissionSetMember` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityPermissionSetMember) + S |
| `CreateSecurityPermissionSetPermission` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityPermissionSetPermission) + S |
| `CreateSecurityResourcePermissionPolicy` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecurityResourcePermissionPolicy) + S |
| `CreateSecuritySecrecyLevel` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSecuritySecrecyLevel) + S |
| `CreateServiceCatalog` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateServiceCatalog) + S + D 11.5.6 |
| `CreateStandard` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateStandard) + S + D 8.3.2 |
| `CreateStandardTemplate` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateStandardTemplate) + S + D 8.6.2 |
| `CreateSubject` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSubject) + S + D 8.8.3 |
| `CreateSubjectNew` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateSubjectNew) + S + D 8.8.9 |
| `CreateTableModel` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateTableModel) + S + D 8.21.2 |
| `CreateTask` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateTask) + S + D 10.8.2 |
| `CreateTemplate` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateTemplate) + S + D 9.2.2 |
| `CreateWorkspace` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=CreateWorkspace) + S + D 8.21.10 |
| `DebugApi` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DebugApi) + S + D 11.1.9 |
| `DebugDataconnection` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DebugDataconnection) + S + D 7.1.4 |
| `DebugSecurityDlfDataWareHouses` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DebugSecurityDlfDataWareHouses) + S |
| `DeclineSecurityApplication` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeclineSecurityApplication) + S |
| `DeleteApi` | DataService | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteApi) + S + D 11.1.5 |
| `DeleteApp` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteApp) + S + D 11.7.4 |
| `DeleteApprover` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteApprover) + S + D 8.7.8 |
| `DeleteAsset` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteAsset) + S + D 10.4.4 |
| `DeleteBizMetric` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteBizMetric) + S + D 8.19.4 |
| `DeleteCatalog` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteCatalog) + S + D 8.5.5 |
| `DeleteClassificationFromEntities` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteClassificationFromEntities) + S + D 10.5.3 |
| `DeleteCodeTable` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteCodeTable) + S + D 8.28.3 |
| `DeleteDataconnection` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDataconnection) + S + D 7.1.1 |
| `DeleteDatasourceConnection` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDatasourceConnection) + S |
| `DeleteDatasourceConnectionRoutes` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDatasourceConnectionRoutes) + S |
| `DeleteDesignAggregationLogicTable` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDesignAggregationLogicTable) + S + D 8.18.4 |
| `DeleteDesignAtomicIndex` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDesignAtomicIndex) + S + D 8.11.4 |
| `DeleteDesignCompoundMetric` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDesignCompoundMetric) + S + D 8.13.4 |
| `DeleteDesignDerivativeIndex` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDesignDerivativeIndex) + S + D 8.12.4 |
| `DeleteDesignDimension` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDesignDimension) + S + D 8.14.4 |
| `DeleteDesignDimensionLogicTable` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDesignDimensionLogicTable) + S + D 8.16.2 |
| `DeleteDesignFactLogicTable` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDesignFactLogicTable) + S + D 8.17.2 |
| `DeleteDesignLatestApproval` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDesignLatestApproval) + S + D 8.7.9 |
| `DeleteDirectory` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteDirectory) + S + D 8.10.4 |
| `DeleteEntity` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteEntity) + S + D 10.9.7 |
| `DeleteSecurityAssignedQueue` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteSecurityAssignedQueue) + S |
| `DeleteSecurityDataClassificationRule` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteSecurityDataClassificationRule) + S |
| `DeleteSecurityDataClassificationRuleGroup` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteSecurityDataClassificationRuleGroup) + S |
| `DeleteSecurityLevelFromEntity` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteSecurityLevelFromEntity) + S + D 10.6.3 |
| `DeleteSecurityPermissionSet` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteSecurityPermissionSet) + S |
| `DeleteSecuritySecrecyLevel` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteSecuritySecrecyLevel) + S |
| `DeleteServiceCatalog` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteServiceCatalog) + S + D 11.5.7 |
| `DeleteStandard` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteStandard) + S + D 8.3.3 |
| `DeleteStandardTemplate` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteStandardTemplate) + S + D 8.6.4 |
| `DeleteSubject` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteSubject) + S + D 8.8.2 |
| `DeleteSubjectNew` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteSubjectNew) + S + D 8.8.8 |
| `DeleteTableModel` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteTableModel) + S + D 8.21.4 |
| `DeleteTaskInfo` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteTaskInfo) + S + D 10.8.5 |
| `DeleteWorkspaces` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteWorkspaces) + S + D 8.21.12 |
| `DeleteWorkspaceusers` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeleteWorkspaceusers) + S + D 7.5.5 |
| `DeployFactoryPackages` | Factory | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DeployFactoryPackages) + S + D 6.2.11 |
| `DownloadTaskLog` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=DownloadTaskLog) + S |
| `ExecuteApiToInstance` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ExecuteApiToInstance) + S + D 11.1.7 |
| `ExecuteSecurityDiagnose` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ExecuteSecurityDiagnose) + S |
| `ExecuteTaskAction` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ExecuteTaskAction) + S + D 10.8.6 |
| `ExportDataServiceExcel` | DataService | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ExportDataServiceExcel) + S + D 11.1.15 |
| `ExportDataServiceExcelTemplate` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ExportDataServiceExcelTemplate) + S + D 11.1.17 |
| `ExportDataServiceZip` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ExportDataServiceZip) + S + D 11.1.16 |
| `ExportDesignModelTableDdl` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ExportDesignModelTableDdl) + S + D 8.21.15 |
| `ExportDesignModels` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ExportDesignModels) + S + D 8.22.4 |
| `ExportDesignResult` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ExportDesignResult) + S + D 8.22.5 |
| `ImportCatalogs` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ImportCatalogs) + S + D 8.22.2 |
| `ImportDataMapLineage` | Catalog | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ImportDataMapLineage) + S + D 10.11.4 |
| `ImportDataServiceExcel` | DataService | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ImportDataServiceExcel) + S + D 11.1.14 |
| `ImportLineage` | Catalog | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ImportLineage) + S + D 10.13.3 |
| `ImportModels` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ImportModels) + S + D 8.22.1 |
| `ImportResult` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ImportResult) + S + D 8.22.3 |
| `ImportSecurityBuiltinCategoryGroups` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ImportSecurityBuiltinCategoryGroups) + S |
| `InitializeStandardTemplate` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=InitializeStandardTemplate) + S + D 8.6.5 |
| `ListAggregationLogicTables` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListAggregationLogicTables) + S + D 8.18.1 |
| `ListAllCatalogList` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListAllCatalogList) + S + D 11.5.1 |
| `ListAllStandards` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListAllStandards) + S + D 8.3.1 |
| `ListAllTables` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListAllTables) + S + D 8.2.1 |
| `ListApiCatalogList` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListApiCatalogList) + S + D 11.5.2 |
| `ListApiTopN` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListApiTopN) + S + D 11.8.10 |
| `ListApicGroups` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListApicGroups) + S + D 11.6.2 |
| `ListApicInstances` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListApicInstances) + S + D 11.6.1 |
| `ListApis` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListApis) + S + D 11.1.2 |
| `ListApisTop` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListApisTop) + S + D 11.8.3 |
| `ListApply` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListApply) + S + D 11.2.1 |
| `ListApprovers` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListApprovers) + S + D 8.7.7 |
| `ListApps` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListApps) + S + D 11.7.2 |
| `ListAppsTop` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListAppsTop) + S + D 11.8.4 |
| `ListBizMetricDimensions` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListBizMetricDimensions) + S + D 8.19.6 |
| `ListBizMetricOwners` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListBizMetricOwners) + S + D 8.19.7 |
| `ListBizMetrics` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListBizMetrics) + S + D 8.19.1 |
| `ListBusiness` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListBusiness) + S + D 8.8.6 |
| `ListCatalogList` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListCatalogList) + S + D 11.5.3 |
| `ListCatalogTree` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListCatalogTree) + S + D 8.5.1 |
| `ListCategoriesTree` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListCategoriesTree) + S + D 10.11.2 |
| `ListCategory` | Quality | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListCategory) + S + D 9.1.1 |
| `ListColumns` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListColumns) + S + D 7.6.4 |
| `ListCompoundMetrics` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListCompoundMetrics) + S + D 8.13.1 |
| `ListCondition` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListCondition) + S + D 8.15.1 |
| `ListConsistencyTask` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListConsistencyTask) + S + D 9.4.1 |
| `ListDataArtsStudioInstances` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDataArtsStudioInstances) + S + D 7.4.1 |
| `ListDataServiceInstanceAccesslogs` | DataService | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDataServiceInstanceAccesslogs) + S + D 11.9.4 |
| `ListDataServiceInstancesDetail` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDataServiceInstancesDetail) + S + D 11.9.2 |
| `ListDataServiceInstancesOverview` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDataServiceInstancesOverview) + S + D 11.9.1 |
| `ListDataServiceMarketApis` | DataService | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDataServiceMarketApis) + S + D 11.5.13 |
| `ListDataTables` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDataTables) + S + D 7.6.3 |
| `ListDatabases` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDatabases) + S + D 7.6.1 |
| `ListDataconnections` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDataconnections) + S + D 7.1.2 |
| `ListDatasourceConnections` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDatasourceConnections) + S |
| `ListDerivativeIndexes` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDerivativeIndexes) + S + D 8.12.1 |
| `ListDesignDataLayers` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDesignDataLayers) + S + D 8.25.1 |
| `ListDimensionGroups` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDimensionGroups) + S + D 8.14.6 |
| `ListDimensionLogicTables` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDimensionLogicTables) + S + D 8.16.1 |
| `ListDimensions` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDimensions) + S + D 8.14.1 |
| `ListDirectories` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListDirectories) + S + D 8.10.1 |
| `ListEntityDetails` | Catalog | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListEntityDetails) + S + D 10.11.1 |
| `ListFactLogicTables` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactLogicTables) + S + D 8.17.1 |
| `ListFactoryAlarmInfo` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactoryAlarmInfo) + S + D 6.2.10 |
| `ListFactoryAlarmRules` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactoryAlarmRules) + S + D 6.3.1 |
| `ListFactoryJobInstancesByName` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactoryJobInstancesByName) + S + D 6.2.15 |
| `ListFactoryPendingItems` | Factory | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactoryPendingItems) + S + D 6.2.5 |
| `ListFactoryReleasePackages` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactoryReleasePackages) + S + D 6.2.7 |
| `ListFactoryScripts` | Factory | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactoryScripts) + S + D 6.1.1 |
| `ListFactorySearchBaselineInstances` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactorySearchBaselineInstances) + S |
| `ListFactoryTaskCompletion` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactoryTaskCompletion) + S + D 6.2.14 |
| `ListFactoryTaskOverview` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactoryTaskOverview) + S + D 6.2.13 |
| `ListFactoryWorkspacesApproval` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListFactoryWorkspacesApproval) + S + D 6.4.1 |
| `ListInstanceList` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListInstanceList) + S + D 11.1.12 |
| `ListInstances` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListInstances) + S + D 9.5.1 |
| `ListLogicEntities` | Catalog | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListLogicEntities) + S + D 10.11.3 |
| `ListManagerWorkSpaces` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListManagerWorkSpaces) + S + D 7.3.1 |
| `ListMessage` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListMessage) + S + D 11.3.1 |
| `ListMetricRelations` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListMetricRelations) + S + D 8.19.8 |
| `ListQualityTask` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListQualityTask) + S + D 9.3.2 |
| `ListQualityTaskLists` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListQualityTaskLists) + S + D 9.3.1 |
| `ListQualityTemplates` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListQualityTemplates) + S + D 9.2.1 |
| `ListRelations` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListRelations) + S + D 8.21.5 |
| `ListSchemas` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSchemas) + S + D 7.6.2 |
| `ListSearchFactoryBaselines` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSearchFactoryBaselines) + S |
| `ListSearchFactoryEvents` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSearchFactoryEvents) + S |
| `ListSecurityApprovals` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityApprovals) + S |
| `ListSecurityAssignedQueues` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityAssignedQueues) + S |
| `ListSecurityDataCategories` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityDataCategories) + S |
| `ListSecurityDataClassificationRuleGroups` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityDataClassificationRuleGroups) + S |
| `ListSecurityDataClassificationRules` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityDataClassificationRules) + S |
| `ListSecurityDatasourceActions` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityDatasourceActions) + S |
| `ListSecurityDatasourceConfigurations` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityDatasourceConfigurations) + S |
| `ListSecurityDatasourceUrls` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityDatasourceUrls) + S |
| `ListSecurityDlfDataWareHouses` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityDlfDataWareHouses) + S |
| `ListSecurityDynamicMaskingPolicies` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityDynamicMaskingPolicies) + S |
| `ListSecurityMemberPermission` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityMemberPermission) + S |
| `ListSecurityMemberPermissionsByUserId` | Security | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityMemberPermissionsByUserId) + S |
| `ListSecurityMemberSyncTasks` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityMemberSyncTasks) + S |
| `ListSecurityMemberTablePermission` | Security | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityMemberTablePermission) + S |
| `ListSecurityPermissionSetMembers` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityPermissionSetMembers) + S |
| `ListSecurityPermissionSetPermissions` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityPermissionSetPermissions) + S |
| `ListSecurityPermissionSets` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityPermissionSets) + S |
| `ListSecurityResourcePermissions` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityResourcePermissions) + S |
| `ListSecurityRoleActions` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityRoleActions) + S |
| `ListSecuritySecrecyLevels` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecuritySecrecyLevels) + S |
| `ListSecuritySensitiveDataDetails` | Security | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecuritySensitiveDataDetails) + S |
| `ListSecuritySensitiveDataOverviews` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecuritySensitiveDataOverviews) + S |
| `ListSecurityTableApprovers` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityTableApprovers) + S |
| `ListSecurityUnreasonablePermissions` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityUnreasonablePermissions) + S |
| `ListSecurityUserTablePermission` | Security | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSecurityUserTablePermission) + S |
| `ListSubjectLevels` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListSubjectLevels) + S + D 8.9.1 |
| `ListTableModelRelations` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListTableModelRelations) + S + D 8.21.7 |
| `ListTableModels` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListTableModels) + S + D 8.21.1 |
| `ListTaskLogs` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListTaskLogs) + S |
| `ListTaskTableReferenceDetail` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListTaskTableReferenceDetail) + S |
| `ListWorkspaceRoles` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListWorkspaceRoles) + S + D 7.5.1 |
| `ListWorkspaces` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListWorkspaces) + S + D 8.21.9 |
| `ListWorkspacesForUser` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListWorkspacesForUser) + S + D 7.3.7 |
| `ListWorkspaceusers` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ListWorkspaceusers) + S + D 7.5.3 |
| `MigrateApi` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=MigrateApi) + S + D 11.5.9 |
| `MigrateCatalog` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=MigrateCatalog) + S + D 11.5.8 |
| `ModifyCustomizedFields` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ModifyCustomizedFields) + S + D 8.23.2 |
| `ModifySecurityAdmin` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ModifySecurityAdmin) + S |
| `ParseUserBehavior` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ParseUserBehavior) + S + D 10.9.3 |
| `PayForDgcOneKey` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=PayForDgcOneKey) + S + D 7.2.1 |
| `PublishApiToInstance` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=PublishApiToInstance) + S + D 11.1.6 |
| `RemoveDesignEntityTags` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=RemoveDesignEntityTags) + S + D 8.27.2 |
| `RemoveDesignQualityInfos` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=RemoveDesignQualityInfos) + S + D 8.24.2 |
| `RenewDataProfile` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=RenewDataProfile) + S + D 10.15.2 |
| `ResetLinkAttributeAndStandard` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ResetLinkAttributeAndStandard) + S + D 8.3.6 |
| `RetryFactoryJobInstance` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=RetryFactoryJobInstance) + S + D 6.2.16 |
| `RollbackApproval` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=RollbackApproval) + S + D 8.7.2 |
| `SearchApprovals` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchApprovals) + S + D 8.7.1 |
| `SearchAtomicIndexes` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchAtomicIndexes) + S + D 8.11.1 |
| `SearchAuthorizeApp` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchAuthorizeApp) + S + D 11.4.1 |
| `SearchBindApi` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchBindApi) + S + D 11.4.2 |
| `SearchCatalogs` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchCatalogs) + S + D 8.5.2 |
| `SearchCodeTableValues` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchCodeTableValues) + S + D 8.28.6 |
| `SearchCodeTables` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchCodeTables) + S + D 8.28.1 |
| `SearchCustomizedFields` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchCustomizedFields) + S + D 8.23.1 |
| `SearchDebugInfo` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchDebugInfo) + S + D 11.1.13 |
| `SearchDesignLatestApprovalDiff` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchDesignLatestApprovalDiff) + S + D 8.7.10 |
| `SearchDwByType` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchDwByType) + S + D 8.4.1 |
| `SearchFactoryJobBaselineInfo` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchFactoryJobBaselineInfo) + S |
| `SearchFieldsForRelation` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchFieldsForRelation) + S + D 8.21.14 |
| `SearchIdByPath` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchIdByPath) + S + D 11.5.10 |
| `SearchPublishInfo` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchPublishInfo) + S + D 11.1.11 |
| `SearchSgcComputeDimensions` | Management Center | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchSgcComputeDimensions) + S |
| `SearchSubject` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchSubject) + S + D 8.8.1 |
| `SearchSubjectNew` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchSubjectNew) + S + D 8.8.7 |
| `SearchVersions` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SearchVersions) + S + D 8.20.1 |
| `SetFactoryJobTags` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=SetFactoryJobTags) + S + D 6.2.9 |
| `ShowAggregationLogicTableById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowAggregationLogicTableById) + S + D 8.18.5 |
| `ShowApi` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowApi) + S + D 11.1.4 |
| `ShowApiDashboard` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowApiDashboard) + S + D 11.8.8 |
| `ShowApisDashboard` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowApisDashboard) + S + D 11.8.7 |
| `ShowApisDetail` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowApisDetail) + S + D 11.8.5 |
| `ShowApisOverview` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowApisOverview) + S + D 11.8.1 |
| `ShowAppInfo` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowAppInfo) + S + D 11.7.5 |
| `ShowApplyDetail` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowApplyDetail) + S + D 11.2.3 |
| `ShowAppsDashboard` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowAppsDashboard) + S + D 11.8.9 |
| `ShowAppsDetail` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowAppsDetail) + S + D 11.8.6 |
| `ShowAppsOverview` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowAppsOverview) + S + D 11.8.2 |
| `ShowAtomicIndexById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowAtomicIndexById) + S + D 8.11.5 |
| `ShowBizCatalogDetail` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowBizCatalogDetail) + S + D 8.5.6 |
| `ShowBizMetricById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowBizMetricById) + S + D 8.19.5 |
| `ShowBusinessAssets` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowBusinessAssets) + S + D 10.1.1 |
| `ShowBusinessAssetsStatistic` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowBusinessAssetsStatistic) + S + D 10.3.2 |
| `ShowBusinessAssetsTree` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowBusinessAssetsTree) + S + D 10.1.2 |
| `ShowCatalogDetail` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowCatalogDetail) + S + D 11.5.5 |
| `ShowCodeTableById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowCodeTableById) + S + D 8.28.5 |
| `ShowCompoundMetricById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowCompoundMetricById) + S + D 8.13.5 |
| `ShowConditionById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowConditionById) + S + D 8.15.2 |
| `ShowConsistencyTaskDetail` | Quality | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowConsistencyTaskDetail) + S + D 9.4.2 |
| `ShowDataDetail` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDataDetail) + S + D 10.9.6 |
| `ShowDataPreview` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDataPreview) + S + D 10.14.1 |
| `ShowDataProfile` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDataProfile) + S + D 10.15.1 |
| `ShowDataServiceInstance` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDataServiceInstance) + S + D 11.9.3 |
| `ShowDataSets` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDataSets) + S + D 10.9.4 |
| `ShowDataconnection` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDataconnection) + S + D 7.1.5 |
| `ShowDatamapLineage` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDatamapLineage) + S + D 10.9.8 |
| `ShowDatasourceConnection` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDatasourceConnection) + S |
| `ShowDerivativeIndexById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDerivativeIndexById) + S + D 8.12.5 |
| `ShowDesignOperationResult` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDesignOperationResult) + S + D 8.21.17 |
| `ShowDimensionById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDimensionById) + S + D 8.14.5 |
| `ShowDimensionLogicTableById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowDimensionLogicTableById) + S + D 8.16.3 |
| `ShowEntities` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowEntities) + S + D 10.4.1 |
| `ShowEntityInfoByGuid` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowEntityInfoByGuid) + S + D 10.4.2 |
| `ShowFactLogicTableById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowFactLogicTableById) + S + D 8.17.3 |
| `ShowFactoryDependInstances` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowFactoryDependInstances) + S |
| `ShowFactoryFullText` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowFactoryFullText) + S + D 6.2.17 |
| `ShowFactoryJobDependInstances` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowFactoryJobDependInstances) + S |
| `ShowFactoryPackageDetail` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowFactoryPackageDetail) + S + D 6.2.8 |
| `ShowFactorySupplementData` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowFactorySupplementData) + S + D 6.2.2 |
| `ShowGlossaryList` | Management Center | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowGlossaryList) + S + D 10.10.1 |
| `ShowInstanceInfos` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowInstanceInfos) + S + D 10.9.11 |
| `ShowInstanceLog` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowInstanceLog) + S + D 10.8.7 |
| `ShowInstanceResult` | Quality | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowInstanceResult) + S + D 9.5.2 |
| `ShowJobMonitorInfo` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowJobMonitorInfo) + S |
| `ShowLineage` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowLineage) + S + D 10.13.2 |
| `ShowLineageBulk` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowLineageBulk) + S + D 10.9.9 |
| `ShowMessageDetail` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowMessageDetail) + S + D 11.3.3 |
| `ShowMetricAssets` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowMetricAssets) + S + D 10.2.2 |
| `ShowMetricTree` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowMetricTree) + S + D 10.2.1 |
| `ShowNodes` | Catalog | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowNodes) + S + D 10.9.10 |
| `ShowPathById` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowPathById) + S + D 11.5.11 |
| `ShowPathObjectById` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowPathObjectById) + S + D 11.5.12 |
| `ShowQualityTaskDetail` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowQualityTaskDetail) + S + D 9.3.3 |
| `ShowQueues` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowQueues) + S + D 10.9.13 |
| `ShowRealTimeJobDetails` | Factory | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowRealTimeJobDetails) + S |
| `ShowRelationById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowRelationById) + S + D 8.21.6 |
| `ShowSecurityAdmin` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityAdmin) + S |
| `ShowSecurityDataClassificationRule` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityDataClassificationRule) + S |
| `ShowSecurityDataClassificationRuleGroup` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityDataClassificationRuleGroup) + S |
| `ShowSecurityDatasourceProtectionDiagnoseResult` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityDatasourceProtectionDiagnoseResult) + S |
| `ShowSecurityDynamicMaskingPolicy` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityDynamicMaskingPolicy) + S |
| `ShowSecurityMemberSyncTask` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityMemberSyncTask) + S |
| `ShowSecurityNoMaskingTableResult` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityNoMaskingTableResult) + S |
| `ShowSecurityPermissionManagementDiagnoseResult` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityPermissionManagementDiagnoseResult) + S |
| `ShowSecurityPermissionSet` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityPermissionSet) + S |
| `ShowSecurityResourcePermissionPolicy` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecurityResourcePermissionPolicy) + S |
| `ShowSecuritySecrecyLevel` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecuritySecrecyLevel) + S |
| `ShowSecuritySensitiveDataDiagnoseResult` | Security | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowSecuritySensitiveDataDiagnoseResult) + S |
| `ShowStandardById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowStandardById) + S + D 8.3.5 |
| `ShowStandardTemplate` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowStandardTemplate) + S + D 8.6.1 |
| `ShowTableData` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowTableData) + S + D 10.9.14 |
| `ShowTableModelById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowTableModelById) + S + D 8.21.8 |
| `ShowTags` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowTags) + S + D 10.9.2 |
| `ShowTaskInfo` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowTaskInfo) + S + D 10.8.3 |
| `ShowTaskList` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowTaskList) + S + D 10.8.1 |
| `ShowTechnicalAssetsStatistic` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowTechnicalAssetsStatistic) + S + D 10.3.1 |
| `ShowTemplatesDetail` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowTemplatesDetail) + S + D 9.2.3 |
| `ShowUnrelatedTable` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowUnrelatedTable) + S + D 10.13.1 |
| `ShowWorkSpace` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowWorkSpace) + S + D 7.3.3 |
| `ShowWorkspaceDetailById` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=ShowWorkspaceDetailById) + S + D 8.21.13 |
| `StopFactorySupplementDataInstance` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=StopFactorySupplementDataInstance) + S + D 6.2.3 |
| `UnpublishSecurityApplication` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UnpublishSecurityApplication) + S |
| `UpdateApi` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateApi) + S + D 11.1.3 |
| `UpdateApp` | DataService | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateApp) + S + D 11.7.3 |
| `UpdateBizMetric` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateBizMetric) + S + D 8.19.3 |
| `UpdateCatalog` | DataService | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateCatalog) + S + D 11.5.4 |
| `UpdateCodeTable` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateCodeTable) + S + D 8.28.4 |
| `UpdateCodeTableValues` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateCodeTableValues) + S + D 8.28.7 |
| `UpdateDataServiceInstanceLtsLog` | DataService | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDataServiceInstanceLtsLog) + S + D 11.9.6 |
| `UpdateDataServiceInstanceObsLog` | DataService | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDataServiceInstanceObsLog) + S + D 11.9.5 |
| `UpdateDataconnection` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDataconnection) + S + D 7.1.6 |
| `UpdateDatasourceConnectionHostMessage` | Migration | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDatasourceConnectionHostMessage) + S |
| `UpdateDesignAggregationLogicTable` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDesignAggregationLogicTable) + S + D 8.18.3 |
| `UpdateDesignAtomicIndex` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDesignAtomicIndex) + S + D 8.11.3 |
| `UpdateDesignCompoundMetric` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDesignCompoundMetric) + S + D 8.13.3 |
| `UpdateDesignDataLayers` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDesignDataLayers) + S + D 8.25.2 |
| `UpdateDesignDerivativeIndex` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDesignDerivativeIndex) + S + D 8.12.3 |
| `UpdateDesignDimension` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDesignDimension) + S + D 8.14.3 |
| `UpdateDesignTableQuality` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDesignTableQuality) + S + D 8.24.1 |
| `UpdateDirectory` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateDirectory) + S + D 8.10.3 |
| `UpdateEntityAttribute` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateEntityAttribute) + S + D 10.12.1 |
| `UpdateFactoryJobName` | Factory | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateFactoryJobName) + S + D 6.2.4 |
| `UpdateSecurityAssignedQueue` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityAssignedQueue) + S |
| `UpdateSecurityDataCategories` | Security | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityDataCategories) + S |
| `UpdateSecurityDataClassificationCombineRule` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityDataClassificationCombineRule) + S |
| `UpdateSecurityDataClassificationRule` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityDataClassificationRule) + S |
| `UpdateSecurityDataClassificationRuleGroup` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityDataClassificationRuleGroup) + S |
| `UpdateSecurityDynamicMaskingPolicy` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityDynamicMaskingPolicy) + S |
| `UpdateSecurityMemberPermissionExpireTime` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityMemberPermissionExpireTime) + S |
| `UpdateSecurityPermissionSet` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityPermissionSet) + S |
| `UpdateSecurityPermissionSetPermission` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityPermissionSetPermission) + S |
| `UpdateSecurityResourcePermissionPolicy` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityResourcePermissionPolicy) + S |
| `UpdateSecurityRuleEnableStatus` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecurityRuleEnableStatus) + S |
| `UpdateSecuritySecrecyLevel` | Security | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSecuritySecrecyLevel) + S |
| `UpdateStandard` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateStandard) + S + D 8.3.4 |
| `UpdateStandardTemplate` | Architecture | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateStandardTemplate) + S + D 8.6.3 |
| `UpdateSubject` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSubject) + S + D 8.8.4 |
| `UpdateSubjectNew` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateSubjectNew) + S + D 8.8.10 |
| `UpdateTableModel` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateTableModel) + S + D 8.21.3 |
| `UpdateTaskInfo` | Catalog | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateTaskInfo) + S + D 10.8.4 |
| `UpdateTemplate` | Quality | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateTemplate) + S + D 9.2.4 |
| `UpdateWorkSpaceOld` | Management Center | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateWorkSpaceOld) + S |
| `UpdateWorkSpaceUserOrGroup` | Management Center | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateWorkSpaceUserOrGroup) + S + D 7.5.2 |
| `UpdateWorkspace` | Architecture | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=DataArtsStudio&name=UpdateWorkspace) + S + D 8.21.11 |

</details>

<details>
<summary>CDM: 28 bundled operations</summary>

| Operation | Component | Status | Evidence |
|---|---|---|---|
| `CreateAndStartRandomClusterJob` | Migration (CDM) | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=CreateAndStartRandomClusterJob) + S + D 4.2.4 |
| `CreateCluster` | Migration (CDM) | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=CreateCluster) + S + D 4.1.14 |
| `CreateJob` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=CreateJob) + S + D 4.2.6 |
| `CreateLink` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=CreateLink) + S + D 4.3.1 |
| `DeleteCluster` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=DeleteCluster) + S + D 4.1.2 |
| `DeleteJob` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=DeleteJob) + S + D 4.2.2 |
| `DeleteLink` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=DeleteLink) + S + D 4.3.3 |
| `ListClusters` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ListClusters) + S + D 4.1.15 |
| `ModifyCluster` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ModifyCluster) + S + D 4.1.10 |
| `RestartCluster` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=RestartCluster) + S + D 4.1.11, 4.1.12, 4.1.13 |
| `ShowAvailabilityZones` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowAvailabilityZones) + S + D 4.1.3 |
| `ShowClusterDetail` | Migration (CDM) | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowClusterDetail) + S + D 4.1.1 |
| `ShowClusterEnterpriseProjects` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowClusterEnterpriseProjects) + S + D 4.1.8 |
| `ShowDatastores` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowDatastores) + S + D 4.1.4 |
| `ShowEnterpriseProjects` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowEnterpriseProjects) + S + D 4.1.7 |
| `ShowFlavorDetail` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowFlavorDetail) + S + D 4.1.6 |
| `ShowFlavors` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowFlavors) + S + D 4.1.5 |
| `ShowInstanceDetail` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowInstanceDetail) + S + D 4.1.9 |
| `ShowJobStatus` | Migration (CDM) | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowJobStatus) + S + D 4.2.8 |
| `ShowJobs` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowJobs) + S + D 4.2.1 |
| `ShowLink` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowLink) + S + D 4.3.2 |
| `ShowSubmissions` | Migration (CDM) | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=ShowSubmissions) + S + D 4.2.9 |
| `StartCluster` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=StartCluster) + S + D 4.1.11, 4.1.12, 4.1.13 |
| `StartJob` | Migration (CDM) | updated | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=StartJob) + S + D 4.2.7 |
| `StopCluster` | Migration (CDM) | updated (added) | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=StopCluster) + S + D 4.1.11, 4.1.12, 4.1.13 |
| `StopJob` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=StopJob) + S + D 4.2.5 |
| `UpdateJob` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=UpdateJob) + S + D 4.2.3 |
| `UpdateLink` | Migration (CDM) | aligned | [E](https://console-intl.huaweicloud.com/apiexplorer/v4/apis/detail?product_short=CDM&name=UpdateLink) + S + D 4.3.4 |

</details>

<details>
<summary>DGC: 38 bundled operations</summary>

| Operation | Component | Status | Evidence |
|---|---|---|---|
| `CancelScript` | Factory (DGC) | aligned | S + D 5.1.8 |
| `CreateConnection` | Factory (DGC) | deprecated; retained | baseline / SDK removal note |
| `CreateJob` | Factory (DGC) | updated | S + D 5.3.1 |
| `CreateResource` | Factory (DGC) | aligned | S + D 5.2.1 |
| `CreateScript` | Factory (DGC) | updated | S + D 5.1.1 |
| `DeleteConnction` | Factory (DGC) | deprecated; retained | baseline / SDK removal note |
| `DeleteJob` | Factory (DGC) | aligned | S + D 5.3.12 |
| `DeleteResource` | Factory (DGC) | aligned | S + D 5.2.4 |
| `DeleteScript` | Factory (DGC) | aligned | S + D 5.1.6 |
| `ExecuteScript` | Factory (DGC) | aligned | S + D 5.1.7 |
| `ExportConnections` | Factory (DGC) | deprecated; retained | baseline / SDK removal note |
| `ExportJob` | Factory (DGC) | aligned | S + D 5.3.6 |
| `ExportJobList` | Factory (DGC) | updated | S + D 5.3.7 |
| `ImportConnections` | Factory (DGC) | deprecated; retained | baseline / SDK removal note |
| `ImportJob` | Factory (DGC) | aligned | S + D 5.3.8 |
| `ListConnections` | Factory (DGC) | deprecated; retained | baseline / SDK removal note |
| `ListJobInstances` | Factory (DGC) | updated | S + D 5.3.16 |
| `ListJobs` | Factory (DGC) | aligned | S + D 5.3.3 |
| `ListResources` | Factory (DGC) | aligned | S + D 5.2.5 |
| `ListScriptResults` | Factory (DGC) | aligned | S + D 5.1.5 |
| `ListScripts` | Factory (DGC) | updated | S + D 5.1.4 |
| `ListSystemTasks` | Factory (DGC) | updated | S + D 5.3.18 |
| `RestoreJobInstance` | Factory (DGC) | aligned | S + D 5.3.14 |
| `RunOnce` | Factory (DGC) | aligned | S + D 5.3.9 |
| `ShowConnection` | Factory (DGC) | deprecated; retained | baseline / SDK removal note |
| `ShowFileInfo` | Factory (DGC) | aligned | S + D 5.3.5 |
| `ShowJob` | Factory (DGC) | updated | S + D 5.3.4 |
| `ShowJobInstance` | Factory (DGC) | aligned | S + D 5.3.17 |
| `ShowJobStatus` | Factory (DGC) | updated | S + D 5.3.15 |
| `ShowResource` | Factory (DGC) | aligned | S + D 5.2.3 |
| `ShowScript` | Factory (DGC) | updated | S + D 5.1.3 |
| `StartJob` | Factory (DGC) | aligned | S + D 5.3.10 |
| `StopJob` | Factory (DGC) | aligned | S + D 5.3.11 |
| `StopJobInstance` | Factory (DGC) | aligned | S + D 5.3.13 |
| `UpdateConnection` | Factory (DGC) | deprecated; retained | baseline / SDK removal note |
| `UpdateJob` | Factory (DGC) | updated | S + D 5.3.2 |
| `UpdateResource` | Factory (DGC) | aligned | S + D 5.2.2 |
| `UpdateScript` | Factory (DGC) | updated | S + D 5.1.2 |

</details>

<details>
<summary>DLF: 39 bundled operations</summary>

| Operation | Component | Status | Evidence |
|---|---|---|---|
| `CancelScript` | Factory (DLF) | aligned | S + D 5.1.8 |
| `CreateConnection` | Factory (DLF) | aligned | S |
| `CreateJob` | Factory (DLF) | updated | S + D 5.3.1 |
| `CreateResource` | Factory (DLF) | aligned | S + D 5.2.1 |
| `CreateScript` | Factory (DLF) | aligned | S + D 5.1.1 |
| `DeleteConnction` | Factory (DLF) | aligned | S |
| `DeleteJob` | Factory (DLF) | aligned | S + D 5.3.12 |
| `DeleteResource` | Factory (DLF) | aligned | S + D 5.2.4 |
| `DeleteScript` | Factory (DLF) | aligned | S + D 5.1.6 |
| `ExecuteScript` | Factory (DLF) | aligned | S + D 5.1.7 |
| `ExportConnections` | Factory (DLF) | aligned | S |
| `ExportJob` | Factory (DLF) | aligned | S + D 5.3.6 |
| `ExportJobList` | Factory (DLF) | aligned | S + D 5.3.7 |
| `ImportConnections` | Factory (DLF) | aligned | S |
| `ImportJob` | Factory (DLF) | aligned | S + D 5.3.8 |
| `ListConnections` | Factory (DLF) | aligned | S |
| `ListJobInstances` | Factory (DLF) | aligned | S + D 5.3.16 |
| `ListJobs` | Factory (DLF) | updated | S + D 5.3.3 |
| `ListResources` | Factory (DLF) | aligned | S + D 5.2.5 |
| `ListScriptResults` | Factory (DLF) | aligned | S + D 5.1.5 |
| `ListScripts` | Factory (DLF) | aligned | S + D 5.1.4 |
| `ListSystemTasks` | Factory (DLF) | updated | S + D 5.3.18 |
| `RestoreJobInstance` | Factory (DLF) | aligned | S + D 5.3.14 |
| `RunOnce` | Factory (DLF) | aligned | S + D 5.3.9 |
| `ShowConnection` | Factory (DLF) | aligned | S |
| `ShowDirectoryTree` | Factory (DLF) | aligned | S |
| `ShowFileInfo` | Factory (DLF) | aligned | S + D 5.3.5 |
| `ShowJob` | Factory (DLF) | updated | S + D 5.3.4 |
| `ShowJobInstance` | Factory (DLF) | aligned | S + D 5.3.17 |
| `ShowJobStatus` | Factory (DLF) | updated | S + D 5.3.15 |
| `ShowResource` | Factory (DLF) | aligned | S + D 5.2.3 |
| `ShowScript` | Factory (DLF) | aligned | S + D 5.1.3 |
| `StartJob` | Factory (DLF) | aligned | S + D 5.3.10 |
| `StopJob` | Factory (DLF) | aligned | S + D 5.3.11 |
| `StopJobInstance` | Factory (DLF) | aligned | S + D 5.3.13 |
| `UpdateConnection` | Factory (DLF) | aligned | S |
| `UpdateJob` | Factory (DLF) | updated | S + D 5.3.2 |
| `UpdateResource` | Factory (DLF) | aligned | S + D 5.2.2 |
| `UpdateScript` | Factory (DLF) | aligned | S + D 5.1.2 |

</details>
