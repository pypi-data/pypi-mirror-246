#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Security Control Implementation """

# standard python imports
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import requests
from lxml.etree import Element
from pydantic import BaseModel

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.models.regscale_models.control import Control


class ControlImplementationStatus(Enum):
    """Control Implementation Status"""

    FullyImplemented = "Fully Implemented"
    NotImplemented = "Not Implemented"
    PartiallyImplemented = "Partially Implemented"
    InRemediation = "In Remediation"
    Inherited = "Inherited"
    NA = "Not Applicable"
    Planned = "Planned"
    Archived = "Archived"
    RiskAccepted = "Risk Accepted"


class ControlImplementation(BaseModel):
    """Control Implementation"""

    parentId: Optional[int]
    parentModule: Optional[str]
    controlOwnerId: str  # Required
    status: str  # Required
    controlID: int  # Required
    control: Optional[Control] = None
    id: Optional[int] = None
    createdById: Optional[str] = None
    uuid: Optional[str] = None
    policy: Optional[str] = None
    implementation: Optional[str] = None
    dateLastAssessed: Optional[str] = None
    lastAssessmentResult: Optional[str] = None
    practiceLevel: Optional[str] = None
    processLevel: Optional[str] = None
    cyberFunction: Optional[str] = None
    implementationType: Optional[str] = None
    implementationMethod: Optional[str] = None
    qdWellDesigned: Optional[str] = None
    qdProcedures: Optional[str] = None
    qdSegregation: Optional[str] = None
    qdFlowdown: Optional[str] = None
    qdAutomated: Optional[str] = None
    qdOverall: Optional[str] = None
    qiResources: Optional[str] = None
    qiMaturity: Optional[str] = None
    qiReporting: Optional[str] = None
    qiVendorCompliance: Optional[str] = None
    qiIssues: Optional[str] = None
    qiOverall: Optional[str] = None
    responsibility: Optional[str] = None
    inheritedControlId: Optional[int] = None
    inheritedRequirementId: Optional[int] = None
    inheritedSecurityPlanId: Optional[int] = None
    inheritedPolicyId: Optional[int] = None
    dateCreated: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    weight: Optional[int] = None
    isPublic: bool = True
    inheritable: bool = False
    systemRoleId: Optional[int] = None
    plannedImplementationDate: Optional[str] = None
    stepsToImplement: Optional[str] = None

    @staticmethod
    def post_implementation(app: Application, implementation: "ControlImplementation"):
        res = None
        api = Api(app)
        headers = {
            "accept": "*/*",
            "Authorization": app.config["token"],
            "Content-Type": "application/json-patch+json",
        }

        res = api.post(
            app.config["domain"] + "/api/controlimplementation",
            headers=headers,
            data=implementation.dict(),
        )
        if not res.raise_for_status() and res.status_code == 200:
            return res.json()
        else:
            return res

    @staticmethod
    def update(
        app: Application, implementation: "ControlImplementation"
    ) -> Union[requests.Response, Dict]:
        """
        Update Method for ControlImplementation

        :param app: Application instance
        :param implementation: ControlImplementation instance
        :return: A control implementation dict or a response object
        :rtype: Union[requests.Response, Dict]
        """
        api = Api(app)

        res = api.put(
            app.config["domain"] + f"/api/controlimplementation/{implementation.id}",
            json=implementation.dict(),
        )
        if not res.raise_for_status() and res.status_code == 200:
            return res.json()
        else:
            return res

    @staticmethod
    def fetch_existing_implementations(
        app: Application, regscale_parent_id: int, regscale_module: str
    ):
        """_summary_

        :param app: Application instance
        :param regscale_parent_id: RegScale Parent ID
        :param regscale_module: RegScale Parent Module
        :return: _description_
        """
        api = Api(app)
        existing_implementations = []
        existing_implementations_response = api.get(
            url=app.config["domain"]
            + "/api/controlimplementation"
            + f"/getAllByParent/{regscale_parent_id}/{regscale_module}"
        )
        if existing_implementations_response.ok:
            existing_implementations = existing_implementations_response.json()
        return existing_implementations

    @staticmethod
    def from_oscal_element(
        app: Application, obj: Element, control: dict
    ) -> "ControlImplementation":
        """
        Create RegScale ControlImplementation from XMl element

        :param Application app: RegScale CLI Application object
        :param Element obj: dictionary
        :param dict control: Control dictionary
        :return: ControlImplementation class
        :rtype: ControlImplementation
        """

        logger = create_logger()
        user = app.config["userId"]
        imp = ControlImplementation(
            controlOwnerId=user, status="notimplemented", controlID=control["id"]
        )

        for element in obj.iter():
            if element.text is not None:
                text = element.text.strip()  # remove unnecessary whitespace
                if text:
                    logger.debug("Text: %s", text)
            logger.debug("Element: %s", element.tag)
            imp.control = control["controlId"]
            for name, value in element.attrib.items():
                logger.debug(f"Property: {name}, Value: {value}")
                if (
                    "name" in element.attrib.keys()
                    and element.attrib["name"] == "implementation-status"
                ):
                    imp.status = (
                        "Fully Implemented"
                        if value == "implemented"
                        else "Not Implemented"
                    )
        return imp

    @staticmethod
    def from_dict(obj: Any) -> "ControlImplementation":
        """
        Create ControlImplementation from dictionary
        :param obj: dictionary
        :return: ControlImplementation class
        :rtype: ControlImplementation
        """
        if "id" in obj:
            del obj["id"]
        return ControlImplementation(**obj)

    def __hash__(self):
        return hash(
            (
                self.controlID,
                self.controlOwnerId,
                self.status,
            )
        )

    @staticmethod
    def stringify_children(node):
        from itertools import chain

        from lxml.etree import tostring

        parts = (
            [node.text]
            + list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren())))
            + [node.tail]
        )
        # filter removes possible Nones in texts and tails
        return "".join(filter(None, parts))

    @staticmethod
    def post_batch_implementation(
        app: Application, implementations: List[Dict]
    ) -> Optional[Union[requests.Response, Dict]]:
        """
        Post a batch of control implementations to the RegScale API

        :param Application app: RegScale CLI Application object
        :param List[Dict] implementations: list of control implementations to post to RegScale
        :return: Response from RegScale API or the response content if the response is not ok
        :rtype: Optional[Union[requests.Response, Dict]]
        """
        if len(implementations) > 0:
            api = Api(app)
            headers = {
                "accept": "*/*",
                "Authorization": app.config["token"],
                "Content-Type": "application/json-patch+json",
            }
            res = api.post(
                url=urljoin(
                    app.config["domain"], "/api/controlImplementation/batchCreate"
                ),
                json=implementations,
                headers=headers,
            )
            if not res.raise_for_status() and res.status_code == 200:
                app.logger.info(
                    f"Created {len(implementations)} Control Implementations, Successfully!"
                )
                return res.json()
            else:
                return res

    @staticmethod
    def put_batch_implementation(
        app: Application, implementations: List[Dict]
    ) -> Optional[Union[requests.Response, Dict]]:
        """
        Put a batch of control implementations to the RegScale API

        :param Application app: RegScale CLI Application object
        :param List[Dict] implementations: list of control implementations to post to RegScale
        :return: Response from RegScale API or the response content if the response is not ok
        :rtype: Optional[Union[requests.Response, Dict]]
        """
        if len(implementations) > 0:
            api = Api(app)
            headers = {
                "accept": "*/*",
                "Authorization": app.config["token"],
                "Content-Type": "application/json-patch+json",
            }
            res = api.post(
                url=urljoin(
                    app.config["domain"], "/api/controlImplementation/batchUpdate"
                ),
                json=implementations,
                headers=headers,
            )
            if not res.raise_for_status() and res.status_code == 200:
                app.logger.info(
                    f"Updated {len(implementations)} Control Implementations, Successfully!"
                )
                return res.json()
            else:
                return res

    @staticmethod
    def get_existing_control_implementations(parent_id: int) -> Dict:
        """
        Fetch existing control implementations as dict with control id as the key used for
        automating control implementation creation

        :param int parent_id: parent control id
        :return: Dictionary of existing control implementations
        :rtype: dict
        """
        app = Application()
        api = Api(app)
        logger = create_logger()
        domain = app.config.get("domain")
        existing_implementation_dict = {}
        get_url = urljoin(
            domain, f"/api/controlImplementation/getAllByPlan/{parent_id}"
        )
        response = api.get(get_url)
        if response.ok:
            existing_control_implementations_json = response.json()
            for cim in existing_control_implementations_json:
                existing_implementation_dict[cim.get("controlName")] = cim
            logger.info(
                f"Found {len(existing_implementation_dict)} existing control implementations"
            )
        elif response.status_code == 404:
            logger.info(f"No existing control implementations found for {parent_id}")
        else:
            logger.warning(
                f"Unable to get existing control implementations. {response.content}"
            )
        return existing_implementation_dict
