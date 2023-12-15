"""
Main interface for neptune-graph service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_neptune_graph import (
        Client,
        ListGraphSnapshotsPaginator,
        ListGraphsPaginator,
        ListImportTasksPaginator,
        ListPrivateGraphEndpointsPaginator,
        NeptuneGraphClient,
    )

    session = Session()
    client: NeptuneGraphClient = session.client("neptune-graph")

    list_graph_snapshots_paginator: ListGraphSnapshotsPaginator = client.get_paginator("list_graph_snapshots")
    list_graphs_paginator: ListGraphsPaginator = client.get_paginator("list_graphs")
    list_import_tasks_paginator: ListImportTasksPaginator = client.get_paginator("list_import_tasks")
    list_private_graph_endpoints_paginator: ListPrivateGraphEndpointsPaginator = client.get_paginator("list_private_graph_endpoints")
    ```
"""

from .client import NeptuneGraphClient
from .paginator import (
    ListGraphSnapshotsPaginator,
    ListGraphsPaginator,
    ListImportTasksPaginator,
    ListPrivateGraphEndpointsPaginator,
)

Client = NeptuneGraphClient


__all__ = (
    "Client",
    "ListGraphSnapshotsPaginator",
    "ListGraphsPaginator",
    "ListImportTasksPaginator",
    "ListPrivateGraphEndpointsPaginator",
    "NeptuneGraphClient",
)
