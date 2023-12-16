#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Dataclass for a RegScale Link """

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

from pydantic import BaseModel
from requests import JSONDecodeError, Response

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger


class Link(BaseModel):
    """Link Model"""

    title: str = ""  # Required
    url: str = ""  # Required
    id: Optional[int] = None
    parentID: Optional[int] = None
    parentModule: Optional[str] = None
    # createdBy: Optional[str] = None
    createdById: Optional[str] = None
    # lastUpdatedBy: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    dateLastUpdated: Optional[str] = None
    externalId: Optional[str] = None
    otherAttributes: Optional[str] = None
    isPublic: bool = True

    def __hash__(self):
        """
        Enable object to be hashable
        :return: Hashed Link
        """
        return hash(
            (
                self.title,
                self.parentID,
                self.parentModule,
                self.url,
            )
        )

    def __eq__(self, other) -> bool:
        """
        Enable object to be equal
        :param other: Object to compare to
        :return: True if equal
        """
        return (
            self.title == other.title
            and self.parentID == other.parentID
            and self.parentModule == other.parentModule
            and self.url == other.url
        )

    @staticmethod
    def update_link(app: Application, link: "Link") -> "Link":
        """
        Update a Link
        :param app: Application
        :param link: Link to update
        :return: Updated Link
        """
        api = Api(app)
        link_id = link.id

        response = api.put(
            app.config["domain"] + f"/api/links/{link_id}", json=link.dict()
        )
        if response.status_code == 200:
            try:
                link = Link(**response.json())
            except JSONDecodeError:
                link = None
        return link

    @staticmethod
    def bulk_insert(
        api: Api, links: List["Link"], thread_count: Optional[int] = 10
    ) -> List[Response]:
        """
        Bulk insert Links to the RegScale API

        :param Api api: RegScale API
        :param List["Link"] links: List of links to insert
        :param Optional[int] thread_count: Number of threads to use, defaults to 10
        :return: List of Responses from RegScale API
        :rtype: List[Response]
        """
        app = api.app
        results = []

        # use threadpoolexecutor to speed up inserts
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [
                executor.submit(
                    Link.insert_link,
                    app,
                    link,
                )
                for link in links
            ]
            for future in as_completed(futures):
                results.append(future.result())
        return results

    @staticmethod
    def insert_link(app: Application, link: "Link") -> "Link":
        """
        Insert a Link into RegScale
        :param app: Application
        :param link: Link to insert
        :return: Inserted Link
        """
        api = Api(app)
        logger = create_logger()
        response = api.post(app.config["domain"] + "/api/links", json=link.dict())
        if response.status_code == 200:
            try:
                link = Link(**response.json())
            except JSONDecodeError as jex:
                logger.error("Unable to read link:\n%s", jex)
                link = None
        else:
            logger.warning("Unable to insert link: %s", link.title)
        return link

    @staticmethod
    def fetch_links_by_parent(
        app: Application,
        regscale_id: int,
        regscale_module: str,
    ) -> List["Link"]:
        """
        Fetch Links by Parent ID and Module
        :param app: Application
        :param regscale_id: RegScale ID
        :param regscale_module: RegScale Module
        :return: List of Links
        """
        api = Api(app)
        body = """
                query {
                    links(take: 50, skip: 0, where: { parentModule: {eq: "parent_module"} parentID: {
                      eq: parent_id
                    }}) {
                    items {
                        id
                        title
                        url
                        parentID
                        parentModule
                        dateCreated
                        createdById
                        lastUpdatedById
                        dateLastUpdated
                        isPublic
                    },
                    pageInfo {
                        hasNextPage
                    }
                    ,totalCount}
                }
                    """.replace(
            "parent_module", regscale_module
        ).replace(
            "parent_id", str(regscale_id)
        )
        existing_regscale_links = api.graph(query=body)["links"]["items"]
        return [Link(**link) for link in existing_regscale_links]
