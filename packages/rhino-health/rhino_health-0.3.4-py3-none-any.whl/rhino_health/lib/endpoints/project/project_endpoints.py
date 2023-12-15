from typing import Callable, List, Optional
from warnings import warn

import arrow
from funcy import compact, flatten

from rhino_health.lib.endpoints.aimodel.aimodel_dataclass import AIModel
from rhino_health.lib.endpoints.cohort.cohort_dataclass import Cohort, FutureCohort
from rhino_health.lib.endpoints.data_schema.data_schema_dataclass import (
    Dataschema,
    FutureDataschema,
)
from rhino_health.lib.endpoints.endpoint import Endpoint, NameFilterMode, VersionMode
from rhino_health.lib.endpoints.project.project_dataclass import (
    FutureProject,
    Project,
    ProjectCreateInput,
    SystemResources,
)
from rhino_health.lib.endpoints.workgroup.workgroup_dataclass import FutureWorkgroup, Workgroup
from rhino_health.lib.metrics.aggregate_metrics.aggregation_service import (
    get_cloud_aggregated_metric_data,
)
from rhino_health.lib.metrics.base_metric import (
    AggregatableMetric,
    BaseMetric,
    JoinableMetric,
    MetricResponse,
)
from rhino_health.lib.utils import alias, rhino_error_wrapper


class ProjectEndpoints(Endpoint):
    """
    @autoapi False

    Rhino SDK LTS supported endpoints

    Endpoints listed here will not change
    """

    @property
    def project_dataclass(self):
        """
        @autoapi False
        """
        return Project

    @property
    def workgroup_dataclass(self):
        """
        @autoapi False
        """
        return Workgroup

    @property
    def cohort_dataclass(self):
        """
        @autoapi False
        """
        return Cohort

    @property
    def data_schema_dataclass(self):
        """
        @autoapi False
        """
        return Dataschema

    @property
    def aimodel_dataclass(self):
        """
        @autoapi False
        """
        return AIModel

    @property
    def resource_management(self):
        """
        @autoapi False
        """
        return SystemResources

    @rhino_error_wrapper
    def get_projects(self, project_uids: Optional[List[str]] = None) -> List[Project]:
        """
        Returns projects the SESSION has access to. If uids are provided, returns only the
        project_uids that are specified.

        :param project_uids: Optional List of strings of project uids to get
        """
        if not project_uids:
            return self.session.get("/projects/").to_dataclasses(self.project_dataclass)
        else:
            return [
                self.session.get(f"/projects/{project_uid}/").to_dataclass(self.project_dataclass)
                for project_uid in project_uids
            ]

    def get_system_resources_for_workgroup(self, project_uid, workgroup_uid) -> SystemResources:
        """
        Returns agent system resources(Memory, GPU, storage) for a collaborating workgroup.

        .. warning:: This feature is under development and the return response may change

        Parameters
        ----------
        project_uid: str
            UID of the project
        workgroup_uid: str
            UID of the workgroup

        Returns
        -------
        system resources: SystemResources
            SystemResources dataclass that match the name
        """

        return self.session.get(
            f"projects/{project_uid}/get_collaborator_resources/{workgroup_uid}/"
        ).to_dataclass(self.resource_management, handle_resource_management_response)


def handle_resource_management_response(response):
    if response["status"] == "success":
        data = response["data"]
        errors = response["errors"]
        # errors are handled per attribute
        data.update(errors)
        return {
            "filesystem_storage": {
                "total": data["filesystem_total_bytes"],
                "free": data["filesystem_free_bytes"],
                "used": data["filesystem_used_bytes"],
            },
            "cpu_percent_used": data["cpu_percent_used"],
            "memory": {
                "total": data["mem_total_bytes"],
                "free": data["mem_free_bytes"],
                "used": data["mem_used_bytes"],
            },
            "gpu": {
                "gpu_percent_used": data["gpu_percent_used"],
                "gpu_mem_percent_used": data["gpu_mem_percent_used"],
            },
        }
    else:
        return response


class ProjectFutureEndpoints(ProjectEndpoints):
    """
    @autoapi True
    @objname ProjectEndpoints

    Endpoints available to interact with Projects on the Rhino Platform

    Notes
    -----
    You should access these endpoints from the RhinoSession object
    """

    @property
    def project_dataclass(self):
        return FutureProject

    @property
    def workgroup_dataclass(self):
        return FutureWorkgroup

    @property
    def cohort_dataclass(self):
        return FutureCohort

    @property
    def data_schema_dataclass(self):
        return FutureDataschema

    def get_project_by_name(self, name: str):
        """
        Returns Project dataclass

        Parameters
        ----------
        name: str
            Full name for the Project

        Returns
        -------
        project: Project
            Project dataclass that match the name

        Examples
        --------
        >>> session.project.get_project_by_name(my_project_name)
        Project()
        """
        results = self.search_for_projects_by_name(name, NameFilterMode.EXACT)
        return max(results, key=lambda x: arrow.get(x.created_at)) if results else None

    def search_for_projects_by_name(
        self, name: str, name_filter_mode: Optional[NameFilterMode] = NameFilterMode.CONTAINS
    ):
        """
        Returns Project dataclasses

        Parameters
        ----------
        name: str
            Full or partial name for the Project
        name_filter_mode: Optional[NameFilterMode]
            Only return results with the specified matching mode

        Returns
        -------
        projects: List[Project]
            Project dataclasses that match the name

        Examples
        --------
        >>> session.project.search_for_projects_by_name(my_project_name)
        [Project()]

        See Also
        --------
        rhino_health.lib.endpoints.endpoint.FilterMode : Different modes to filter by
        """
        query_params = self._get_filter_query_params(
            {"name": name}, name_filter_mode=name_filter_mode
        )
        results = self.session.get("/projects", params=query_params)
        return results.to_dataclasses(self.project_dataclass)

    @rhino_error_wrapper
    def add_project(self, project: ProjectCreateInput) -> Project:
        """
        Adds a new project owned by the currently logged in user.

        .. warning:: This feature is under development and the interface may change
        """
        return self.session.post("/projects", data=project.dict(by_alias=True)).to_dataclass(
            self.project_dataclass
        )

    @rhino_error_wrapper
    def get_cohorts(self, project_uid: str) -> List[Cohort]:
        """
        Returns Cohorts associated with the project_uid
        """
        if not project_uid:
            raise ValueError("Must provide a project id")
        query_params = self._get_filter_query_params({"project_uid": project_uid})
        return self.session.get("cohorts", params=query_params).to_dataclasses(
            self.cohort_dataclass
        )

    @rhino_error_wrapper
    def get_cohort_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None
    ) -> Optional[Cohort]:
        """
        Returns Cohort dataclass

        See Also
        --------
        rhino_health.lib.endpoints.cohort.cohort_endpoints.get_cohort_by_name
        """
        return self.session.cohort.get_cohort_by_name(name, version, project_uid)

    @rhino_error_wrapper
    def search_for_cohorts_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None, name_filter_mode=None
    ) -> List[Cohort]:
        """
        Returns Cohort dataclasses

        See Also
        --------
        rhino_health.lib.endpoints.cohort.cohort_endpoints.search_for_cohorts_by_name
        """
        return self.session.cohort.search_for_cohorts_by_name(
            name, version, project_uid, name_filter_mode=name_filter_mode
        )

    @rhino_error_wrapper
    def get_data_schemas(self, project_uid: str) -> List[FutureDataschema]:
        """
        Returns Datashemas associated with the project_uid
        """
        if not project_uid:
            raise ValueError("Must provide a project id")
        return self.session.get(f"/projects/{project_uid}/dataschemas").to_dataclasses(
            self.data_schema_dataclass
        )

    get_dataschemas = alias(get_data_schemas, "get_data_schemas", base_object="session.project")
    """ @autoapi False """

    @rhino_error_wrapper
    def get_data_schema_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None
    ) -> Dataschema:
        """
        Returns DataSchema dataclass

        See Also
        --------
        rhino_health.lib.endpoints.dataschema.dataschema_endpoints.get_dataschema_by_name
        """
        return self.session.data_schema.get_data_schema_by_name(name, version, project_uid)

    get_dataschema_by_name = alias(
        get_data_schema_by_name, "get_dataschema_by_name", base_object="session.project"
    )
    """ @autoapi False """

    @rhino_error_wrapper
    def search_for_data_schemas_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None, name_filter_mode=None
    ) -> List[Dataschema]:
        """
        Returns DataSchema dataclasses

        See Also
        --------
        rhino_health.lib.endpoints.dataschema.dataschema_endpoints.search_for_data_schemas_by_name
        """
        return self.session.data_schema.search_for_data_schemas_by_name(
            name, version, project_uid, name_filter_mode=name_filter_mode
        )

    search_for_dataschemas_by_name = alias(
        search_for_data_schemas_by_name,
        "search_for_dataschemas_by_name",
        base_object="session.project",
    )
    """ @autoapi False """

    @rhino_error_wrapper
    def get_models(self, project_uid: str) -> List[AIModel]:
        """
        @autoapi False
        Returns AIModels associated with the project_uid

        .. warning:: This function is deprecated and will be removed in the future, please call get_aimodels
        """
        warn(
            "Project.get_models is deprecated and will be removed in the future, please use get_aimodels()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get_aimodels(project_uid)

    @rhino_error_wrapper
    def get_aimodels(self, project_uid: str) -> List[AIModel]:
        """
        Returns AI Models associated with the project
        """
        if not project_uid:
            raise ValueError("Must provide a project id")
        return self.session.get(f"/projects/{project_uid}/models").to_dataclasses(
            self.aimodel_dataclass
        )

    @rhino_error_wrapper
    def get_aimodel_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None
    ) -> Optional[AIModel]:
        """
        Returns AIModel dataclass

        See Also
        --------
        rhino_health.lib.endpoints.aimodel.aimodel_endpoints.get_aimodel_by_name
        """
        return self.session.aimodel.get_aimodel_by_name(name, version, project_uid)

    @rhino_error_wrapper
    def search_for_aimodels_by_name(
        self, name, version=VersionMode.LATEST, project_uid=None, name_filter_mode=None
    ) -> List[AIModel]:
        """
        Returns AIModel dataclasses

        See Also
        --------
        rhino_health.lib.endpoints.aimodel.aimodel_endpoints.search_for_aimodels_by_name
        """
        return self.session.aimodel.search_for_aimodels_by_name(
            name, version, project_uid, name_filter_mode=name_filter_mode
        )

    @rhino_error_wrapper
    def get_collaborating_workgroups(self, project_uid: str):
        return self.session.get(f"/projects/{project_uid}/collaborators").to_dataclasses(
            self.workgroup_dataclass
        )

    @rhino_error_wrapper
    def add_collaborator(self, project_uid: str, collaborating_workgroup_uid: str):
        """
        Adds COLLABORATING_WORKGROUP_UID as a collaborator to PROJECT_UID

        .. warning:: This feature is under development and the interface may change
        """
        # TODO: Backend needs to return something sensible
        # TODO: Automatically generated swagger docs don't match with internal code
        self.session.post(
            f"/projects/{project_uid}/add_collaborator/{collaborating_workgroup_uid}", {}
        )
        return self.session.project.get_projects([project_uid])[0]

    @rhino_error_wrapper
    def remove_collaborator(self, project_uid: str, collaborating_workgroup_uid: str):
        """
        Removes COLLABORATING_WORKGROUP_UID as a collaborator from PROJECT_UID

        .. warning:: This feature is under development and the interface may change
        """
        # TODO: What should this return internally
        # TODO: Backend needs to return something sensible
        # TODO: Automatically generated swagger docs don't match with internal code
        self.session.post(
            f"/projects/{project_uid}/remove_collaborator/{collaborating_workgroup_uid}", {}
        )

    @rhino_error_wrapper
    def aggregate_cohort_metric(
        self,
        cohort_uids: List[str],
        metric_configuration: BaseMetric,
        aggregation_method_override: Optional[Callable] = None,
    ) -> MetricResponse:
        """
        Returns the aggregate metric based on the METRIC_CONFIGURATION for a list of cohorts.

        Parameters
        ----------
        cohort_uids: List[str]
            UIDS for the cohort to query metrics against
        metric_configuration: BaseMetric
            Configuration for the metric to be run
        aggregation_method_override: Optional[Callable]
            A custom function to use to aggregate the results. The method signature should be: method(metric_name: str, metric_results: List[Dict[str, Any]], **kwargs),
            where the metric_results are each of the cohorts results for the metric,
            and the method should return a dict with the structure of: {metric_name: <aggregated_value>}.

        Returns
        -------
        metric_response: MetricResponse
            A response object containing the result of the query

        See Also
        --------
        rhino_health.lib.metrics : Dataclasses specifying possible metric configurations to send
        rhino_health.lib.metrics.base_metric.MetricResponse : Response object
        rhino_health.lib.metrics.aggregate_metrics.aggregation_methods : Sample aggregation methods
        """
        if not isinstance(metric_configuration, AggregatableMetric):
            raise ValueError(
                f"The chosen metric is not aggregatable. For using this metric, please use the cohort.get_metric endpoint instead, for a specific cohort."
            )

        if aggregation_method_override and not metric_configuration.supports_custom_aggregation:
            raise ValueError(
                f"aggregation_method_override is not supported with metric {metric_configuration.metric_name()}"
                " which uses cloud-based aggregation"
            )
        return get_cloud_aggregated_metric_data(
            self.session, cohort_uids, metric_configuration, aggregation_method_override
        )

    @rhino_error_wrapper
    def joined_cohort_metric(
        self,
        configuration: JoinableMetric,
        data_cohorts: List[str],
        filter_cohorts: Optional[List[str]] = None,
    ) -> MetricResponse:
        """
        Perform a Federated Join Cohort Metric

        Intersection Joins allow filtering against columns in that are present in the filter cohort
        and then getting metrics from a separate data cohort which do not contain those columns.

        Union Joins handles deduplication of results between multiple cohorts.

        Parameters
        ----------
        metric_configuration: JoinableMetric
            Configuration for the metric to be run
        data_cohorts: List[str]
            UIDS for the cohort(s) to get the data values from.
            For INTERSECTION mode supports one cohort.
            For UNION mode supports any number of cohorts.
        filter_cohorts: Optional[List[str]] = None
            UIDS for the cohort(s) to perform the join query against.
            For INTERSECTION mode supports one cohort.
            For UNION mode this is ignored

        Returns
        -------
        metric_response: MetricResponse
            A response object containing the result of the query
        """
        configuration.filter_cohorts = filter_cohorts
        configuration.data_cohorts = data_cohorts
        all_cohort_uids = list(flatten(compact([filter_cohorts, data_cohorts])))
        return self.session.project.aggregate_cohort_metric(all_cohort_uids, configuration)
