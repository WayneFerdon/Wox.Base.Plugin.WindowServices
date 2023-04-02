# ----------------------------------------------------------------
# Author: WayneFerdon wayneferdon@hotmail.com
# Date: 2023-04-02 11:57:59
# LastEditors: WayneFerdon wayneferdon@hotmail.com
# LastEditTime: 2023-04-02 13:41:06
# FilePath: \Flow.Launcher.Plugin.WindowServices\services.py
# ----------------------------------------------------------------
# Copyright (c) 2023 by Wayne Ferdon Studio. All rights reserved.
# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.
# See the LICENSE file in the project root for more information.
# ----------------------------------------------------------------

import subprocess as sp
from enum import Enum

class Service(object):
    class Status(Enum):
        STOPPED=0
        RUNNING=1,


    def __init__(self, service):
        self._raw = service
        self._name = None
        self._display_name = None
        self._status = None

    def __str__(self):
        return f"{self.name} ({self.display_name})"
    
    @property
    def name(self) -> str:
        if self._name is None:
            self._name = self._raw.split("\n")[0].split(":")[1].strip()
        return self._name

    @property
    def display_name(self) -> str:
        if self._display_name is None:
            self._display_name = self._raw.split("\n")[1].split(":")[1].strip()
        return self._display_name

    @property
    def status(self) -> Status:
        if self._status is None:
            self._status = Service.Status[self._raw.split("\n")[3].split("  ")[-1].strip().upper()]
        return self._status

def get_services() -> list[Service]:
    services_list = list[Service]()
    code_page = sp.check_output("chcp", shell=True, text=True).split(":")[1].strip()
    output = sp.check_output("sc query type= service state= all", shell=True)
    try:
        services = output.decode(f"cp{code_page}")
    except (UnicodeDecodeError, LookupError):
        services = output.decode("utf-8", errors="replace")
    for service in services.split("\r\n\r\n"):
        if "SERVICE_NAME" in service.split("\n")[0]:
            services_list.append(Service(service))
    return services_list