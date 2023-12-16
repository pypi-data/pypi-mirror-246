#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Assessment """
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from pydantic import BaseModel
from requests import JSONDecodeError

from regscale.core.app.api import Api
from regscale.core.app.application import Application


class Assessment(BaseModel):
    leadAssessorId: Optional[str] = None  # Required field
    title: Optional[str] = None  # Required field
    assessmentType: Optional[str] = None  # Required field
    plannedStart: Optional[str] = None  # Required field
    plannedFinish: Optional[str] = None  # Required field
    status: Optional[str] = "Scheduled"  # Required field
    id: Optional[int] = None
    facilityId: Optional[int] = None
    orgId: Optional[int] = None
    assessmentResult: Optional[str] = None
    actualFinish: Optional[str] = None
    assessmentReport: Optional[str] = None
    masterId: Optional[int] = None
    complianceScore: Optional[float] = None
    targets: Optional[str] = None
    automationInfo: Optional[str] = None
    automationId: Optional[str] = None
    metadata: Optional[str] = None
    assessmentPlan: Optional[str] = None
    methodology: Optional[str] = None
    rulesOfEngagement: Optional[str] = None
    disclosures: Optional[str] = None
    scopeIncludes: Optional[str] = None
    scopeExcludes: Optional[str] = None
    limitationsOfLiability: Optional[str] = None
    documentsReviewed: Optional[str] = None
    activitiesObserved: Optional[str] = None
    fixedDuringAssessment: Optional[str] = None
    summaryOfResults: Optional[str] = None
    oscalsspId: Optional[int] = None
    oscalComponentId: Optional[int] = None
    controlId: Optional[int] = None
    requirementId: Optional[int] = None
    securityPlanId: Optional[int] = None
    projectId: Optional[int] = None
    supplyChainId: Optional[int] = None
    policyId: Optional[int] = None
    componentId: Optional[int] = None
    incidentId: Optional[int] = None
    parentId: Optional[int] = None
    parentModule: Optional[str] = None
    createdById: Optional[str] = None
    dateCreated: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    isPublic: bool = True

    def __getitem__(self, key: any) -> any:
        """
        Get attribute from Pipeline
        :param any key:
        :return: value of provided key
        :rtype: any
        """
        return getattr(self, key)

    def __setitem__(self, key: any, value: any) -> None:
        """
        Set attribute in Pipeline with provided key
        :param any key: Key to change to provided value
        :param any value: New value for provided Key
        :return: None
        """
        return setattr(self, key, value)

    def insert_assessment(self, app: Application) -> Optional["Assessment"]:
        """
        Function to create a new assessment in RegScale and returns the new assessment's ID
        :param Application app: Application object
        :return: New Assessment object created in RegScale
        :rtype: Optional[Assessment]
        """
        api = Api(app)
        url = f"{app.config['domain']}/api/assessments"
        response = api.post(url=url, json=self.dict())
        if not response.ok:
            app.logger.debug(response.status_code)
            app.logger.error(f"Failed to insert Assessment.\n{response.text}")
        return Assessment(**response.json()) if response.ok else None

    @staticmethod
    def bulk_insert(
        app: Application,
        assessments: list["Assessment"],
        max_workers: Optional[int] = 30,
    ) -> list["Assessment"]:
        """Bulk insert assets using the RegScale API and ThreadPoolExecutor

        :param Application app: Application Instance
        :param list["Assessment"] assessments: Assessment List
        :param Optional[int] max_workers: Max Workers, defaults to 30
        :return: List of Assessments created in RegScale
        :rtype: list["Assessment"]
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            workers = [
                executor.submit(
                    assessment.insert_assessment,
                    app,
                )
                for assessment in assessments
            ]
        return [worker.result() for worker in workers] or []

    @staticmethod
    def fetch_all_assessments(app: Application) -> list["Assessment"]:
        """
        Function to retrieve all assessments from RegScale
        :param Application app: Application Object
        :return: List of assessments from RegScale
        :rtype: list[Assessment]
        """
        query = """
            query {
              assessments (take: 50, skip: 0) {
                items {
                  id
                  status
                   actualFinish
                   assessmentReport
                   facilityId
                   orgId
                   masterId
                   complianceScore
                   isPublic
                   targets
                   automationInfo
                   automationId
                   metadata
                   assessmentPlan
                   methodology
                   rulesOfEngagement
                   disclosures
                   scopeIncludes
                   scopeExcludes
                   uuid
                   limitationsOfLiability
                   documentsReviewed
                   activitiesObserved
                   fixedDuringAssessment
                   oscalsspId
                   oscalComponentId
                   controlId
                   requirementId
                   securityPlanId
                   policyId
                   supplyChainId
                   leadAssessorId
                   componentId
                   incidentId
                   projectId
                   parentModule
                   parentId
                   createdById
                   dateCreated
                   title
                   lastUpdatedById
                   dateLastUpdated
                   assessmentType
                   assessmentResult
                   plannedStart
                   plannedFinish
                }
                pageInfo {
                  hasNextPage
                }
                totalCount
              }
            }
        """
        api = Api(app)
        try:
            app.logger.info("Retrieving all assessments in RegScale...")
            existing_assessments = api.graph(query=query)["assessments"]["items"]
            app.logger.info(
                "%i assessment(s) retrieved from RegScale.", len(existing_assessments)
            )
        except JSONDecodeError:
            existing_assessments = []
        return [Assessment(**assessment) for assessment in existing_assessments]

    @staticmethod
    def fetch_all_assessments_by_parent(
        app: Application,
        parent_id: int,
        parent_module: str,
        org_and_facil: Optional[bool] = False,
    ) -> dict:
        """
        Function to retrieve all assessments from RegScale by parent

        :param Application app: RegScale Application object
        :param int parent_id: RegScale ID of parent
        :param str parent_module: Module of parent
        :param bool org_and_facil: If True, return org and facility names
        :return: GraphQL response from RegScale
        :rtype: dict
        """
        api = Api(app)
        # The indentation is important here
        org_and_facil_query = """
                  facility {
                    name
                  }
                  org {
                    name
                  }
        """
        body = f"""
            query {{
              assessments (skip: 0, take: 50, where: {{parentId: {{eq: {parent_id}}} parentModule: {{eq: "{parent_module}"}}}}) {{
                items {{
                  id
                  title
                  leadAssessor {{
                    firstName
                    lastName
                    userName
                  }}
                  {org_and_facil_query if org_and_facil else ""}
                  assessmentType
                  plannedStart
                  plannedFinish
                  status
                  actualFinish
                  assessmentResult
                  parentId
                  parentModule
                }}
                totalCount
                pageInfo {{
                  hasNextPage
                }}
              }}
            }}
        """
        assessments = api.graph(query=body)
        if parent_module not in [
            "securityplans",
            "incidents",
            "policies",
            "components",
            "requirements",
            "supplychain",
        ]:
            return assessments

        replacements = {
            "securityplans": "securityPlanId",
            "incidents": "incidentId",
            "policies": "policyId",
            "components": "componentId",
            "requirements": "requirementId",
            "supplychain": "supplyChainId",
        }
        if replacement_key := replacements.get(parent_module):
            body = body.replace(
                f'parentId: {{eq: {parent_id}}} parentModule: {{eq: "{parent_module}"}}',
                f"{replacement_key}: {{eq: {parent_id}}}",
            )
        return {**assessments, **api.graph(query=body)}
