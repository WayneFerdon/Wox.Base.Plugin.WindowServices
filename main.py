# ----------------------------------------------------------------
# Author: WayneFerdon wayneferdon@hotmail.com
# Date: 2023-04-02 11:57:59
# LastEditors: WayneFerdon wayneferdon@hotmail.com
# LastEditTime: 2023-04-02 13:44:54
# FilePath: \Flow.Launcher.Plugin.WindowServices\main.py
# ----------------------------------------------------------------
# Copyright (c) 2023 by Wayne Ferdon Studio. All rights reserved.
# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the MIT license.
# See the LICENSE file in the project root for more information.
# ----------------------------------------------------------------

import os
import subprocess
from Query import *
from services import *

ICON_DIR = './Images'
SERVICE_RUNNING = os.path.join(ICON_DIR, 'running.png')
SERVICE_STOPPED = os.path.join(ICON_DIR, 'stopped.png')
SERVICE_START = os.path.join(ICON_DIR, 'start.png')
SERVICE_STOP = os.path.join(ICON_DIR, 'stop.png')
BAT_FILE = 'toggle_service.bat'
STATUS_ICON = {
    Service.Status.RUNNING:SERVICE_RUNNING,
    Service.Status.STOPPED:SERVICE_STOPPED
}

class WindowServices(Query):
    def query(self, query:str):
        results = list()
        services = get_services()
        for service in services:
            if query.lower() in service.name.lower() or query.lower() in service.display_name.lower():
                subtitle = f"{service.status.name} - Press ENTER to toggle service"
                results.append(QueryResult(
                    str(service),
                    subtitle,
                    STATUS_ICON[service.status],
                    service.name,
                    'toggle_service',
                    True,
                    service.name, service.status.name
                ).toDict())
        return results

    def context_menu(self, serviceName:str): 
        results = list()
        results.append(QueryResult(
            'Start Service',
            f'Start {serviceName} service',
            SERVICE_START,
            serviceName,
            'control_service',
            False,
            serviceName, 'start'
        ).toDict())
        results.append(QueryResult(
            'Stop Service',
            f'Stop {serviceName} service',
            SERVICE_STOP,
            serviceName,
            'control_service',
            False,
            serviceName, 'stop'
        ).toDict())
        return results

    def control_service(self, service_name:str, comand:str):
        bat_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), BAT_FILE)
        popen = subprocess.Popen(f'Powershell -Command "Start-Process sc -ArgumentList \\\"{comand} \\\"\\\"{service_name}\\\"\\\"\\\" -Verb RunAs -WindowStyle Hidden"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    def toggle_service(self, service_name:str, service_state:str):
        if service_state == Service.Status.RUNNING.name:
            self.control_service(service_name, 'stop')
        elif service_state == Service.Status.STOPPED.name:
            self.control_service(service_name, 'start')


if __name__ == '__main__':
    WindowServices()