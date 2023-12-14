# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

import httpx
import logging, verboselogs

from ....options import DeepgramClientOptions
from ...abstract_sync_client import AbstractSyncRestClient

from .response import (
    Project,
    ProjectsResponse,
    Message,
    KeysResponse,
    KeyResponse,
    Key,
    MembersResponse,
    ScopesResponse,
    InvitesResponse,
    UsageRequestsResponse,
    UsageRequest,
    UsageSummaryResponse,
    UsageFieldsResponse,
    BalancesResponse,
    Balance,
)
from .options import (
    ProjectOptions,
    KeyOptions,
    ScopeOptions,
    InviteOptions,
    UsageRequestOptions,
    UsageSummaryOptions,
    UsageFieldsOptions,
)


class ManageClient(AbstractSyncRestClient):
    """
    A client for managing Deepgram projects and associated resources via the Deepgram API.

    This class provides methods for performing various operations on Deepgram projects, including:
    - Retrieving project details
    - Updating project settings
    - Managing project members and scopes
    - Handling project invitations
    - Monitoring project usage and balances

    Args:
        config (DeepgramClientOptions): all the options for the client.

    Attributes:
        url (str): The base URL of the Deepgram API.
        headers (dict): Optional HTTP headers to include in requests.
        endpoint (str): The API endpoint for managing projects.

    Raises:
        DeepgramApiError: Raised for known API errors.
        DeepgramUnknownApiError: Raised for unknown API errors.
        Exception: For any other unexpected exceptions.
    """

    def __init__(self, config: DeepgramClientOptions):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(config.verbose)

        self.config = config
        self.endpoint = "v1/projects"
        super().__init__(config)

    # projects
    def list_projects(self, timeout: httpx.Timeout = None):
        return self.get_projects()

    def get_projects(self, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_projects ENTER")
        url = f"{self.config.url}/{self.endpoint}"
        self.logger.info("url: %s", url)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = ProjectsResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_projects succeeded")
        self.logger.debug("ManageClient.get_projects LEAVE")
        return res

    def get_project(self, project_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_project ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Project.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_project succeeded")
        self.logger.debug("ManageClient.get_project LEAVE")
        return res

    def update_project_option(self, project_id: str, options: ProjectOptions, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.update_project_option ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        json = self.patch(url, json=options, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Message.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("update_project_option succeeded")
        self.logger.debug("ManageClient.update_project_option LEAVE")
        return res

    def update_project(self, project_id: str, name="", timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.update_project ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        options: ProjectOptions = {
            "name": name,
        }
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        json = self.patch(url, json=options, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Message.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("update_project succeeded")
        self.logger.debug("ManageClient.update_project LEAVE")
        return res

    def delete_project(self, project_id: str, timeout: httpx.Timeout = None) -> None:
        self.logger.debug("ManageClient.delete_project ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}"
        json = self.delete(url)
        self.logger.info("json: %s", json, timeout=timeout)
        res = Message.from_json(self.delete(url))
        self.logger.verbose("result: %s", res)
        self.logger.notice("delete_project succeeded")
        self.logger.debug("ManageClient.delete_project LEAVE")
        return res

    # keys
    def list_keys(self, project_id: str, timeout: httpx.Timeout = None):
        return self.get_keys(project_id)

    def get_keys(self, project_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_keys ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = KeysResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_keys succeeded")
        self.logger.debug("ManageClient.get_keys LEAVE")
        return res

    def get_key(self, project_id: str, key_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_key ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys/{key_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("key_id: %s", key_id)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = KeyResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_key succeeded")
        self.logger.debug("ManageClient.get_key LEAVE")
        return res

    def create_key(self, project_id: str, options: KeyOptions, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.create_key ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        json = self.post(url, json=options, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Key.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("create_key succeeded")
        self.logger.debug("ManageClient.create_key LEAVE")
        return res

    def delete_key(self, project_id: str, key_id: str, timeout: httpx.Timeout = None) -> None:
        self.logger.debug("ManageClient.delete_key ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/keys/{key_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("key_id: %s", key_id)
        json = self.delete(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Message.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("delete_key succeeded")
        self.logger.debug("ManageClient.delete_key LEAVE")
        return res

    # members
    def list_members(self, project_id: str, timeout: httpx.Timeout = None):
        return self.get_members(project_id)

    def get_members(self, project_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_members ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/members"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = MembersResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_members succeeded")
        self.logger.debug("ManageClient.get_members LEAVE")
        return res

    def remove_member(self, project_id: str, member_id: str, timeout: httpx.Timeout = None) -> None:
        self.logger.debug("ManageClient.remove_member ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/members/{member_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("member_id: %s", member_id)
        json = self.delete(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Message.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("remove_member succeeded")
        self.logger.debug("ManageClient.remove_member LEAVE")
        return res

    # scopes
    def get_member_scopes(self, project_id: str, member_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_member_scopes ENTER")
        url = (
            f"{self.config.url}/{self.endpoint}/{project_id}/members/{member_id}/scopes"
        )
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("member_id: %s", member_id)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = ScopesResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_member_scopes succeeded")
        self.logger.debug("ManageClient.get_member_scopes LEAVE")
        return res

    def update_member_scope(
        self, project_id: str, member_id: str, options: ScopeOptions, timeout: httpx.Timeout = None
    ):
        self.logger.debug("ManageClient.update_member_scope ENTER")
        url = (
            f"{self.config.url}/{self.endpoint}/{project_id}/members/{member_id}/scopes"
        )
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        json = self.put(url, json=options, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Message.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("update_member_scope succeeded")
        self.logger.debug("ManageClient.update_member_scope LEAVE")
        return res

    # invites
    def list_invites(self, project_id: str, timeout: httpx.Timeout = None):
        return self.get_invites(project_id)

    def get_invites(self, project_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_invites ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = InvitesResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_invites succeeded")
        self.logger.debug("ManageClient.get_invites LEAVE")
        return res

    def send_invite_options(self, project_id: str, options: InviteOptions, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.send_invite_options ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        json = self.post(url, json=options, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Message.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("send_invite_options succeeded")
        self.logger.debug("ManageClient.send_invite_options LEAVE")
        return res

    def send_invite(self, project_id: str, email: str, scope="member", timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.send_invite ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites"
        options: InviteOptions = {
            "email": email,
            "scope": scope,
        }
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        json = self.post(url, json=options, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Message.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("send_invite succeeded")
        self.logger.debug("ManageClient.send_invite LEAVE")
        return res

    def delete_invite(self, project_id: str, email: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.delete_invite ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/invites/{email}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("email: %s", email)
        json = self.delete(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Message.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("delete_invite succeeded")
        self.logger.debug("ManageClient.delete_invite LEAVE")
        return res

    def leave_project(self, project_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.leave_project ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/leave"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        json = self.delete(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Message.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("leave_project succeeded")
        self.logger.debug("ManageClient.leave_project LEAVE")
        return res

    # usage
    def get_usage_requests(self, project_id: str, options: UsageRequestOptions, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_usage_requests ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/requests"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        json = self.get(url, options, timeout=timeout)
        self.logger.info("json: %s", json)
        res = UsageRequestsResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_usage_requests succeeded")
        self.logger.debug("ManageClient.get_usage_requests LEAVE")
        return res

    def get_usage_request(self, project_id: str, request_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_usage_request ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/requests/{request_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("request_id: %s", request_id)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = UsageRequest.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_usage_request succeeded")
        self.logger.debug("ManageClient.get_usage_request LEAVE")
        return res

    def get_usage_summary(self, project_id: str, options: UsageSummaryOptions, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_usage_summary ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/usage"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        json = self.get(url, options, timeout=timeout)
        self.logger.info("json: %s", json)
        res = UsageSummaryResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_usage_summary succeeded")
        self.logger.debug("ManageClient.get_usage_summary LEAVE")
        return res

    def get_usage_fields(self, project_id: str, options: UsageFieldsOptions, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_usage_fields ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/usage/fields"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("options: %s", options)
        json = self.get(url, options, timeout=timeout)
        self.logger.info("json: %s", json)
        res = UsageFieldsResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_usage_fields succeeded")
        self.logger.debug("ManageClient.get_usage_fields LEAVE")
        return res

    # balances
    def list_balances(self, project_id: str, timeout: httpx.Timeout = None):
        return self.get_balances(project_id)

    def get_balances(self, project_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_balances ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/balances"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = BalancesResponse.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_balances succeeded")
        self.logger.debug("ManageClient.get_balances LEAVE")
        return res

    def get_balance(self, project_id: str, balance_id: str, timeout: httpx.Timeout = None):
        self.logger.debug("ManageClient.get_balance ENTER")
        url = f"{self.config.url}/{self.endpoint}/{project_id}/balances/{balance_id}"
        self.logger.info("url: %s", url)
        self.logger.info("project_id: %s", project_id)
        self.logger.info("balance_id: %s", balance_id)
        json = self.get(url, timeout=timeout)
        self.logger.info("json: %s", json)
        res = Balance.from_json(json)
        self.logger.verbose("result: %s", res)
        self.logger.notice("get_balance succeeded")
        self.logger.debug("ManageClient.get_balance LEAVE")
        return res
