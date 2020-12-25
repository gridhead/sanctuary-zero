"""
##########################################################################
*
*   Copyright © 2019-2020 Akashdeep Dhar <t0xic0der@fedoraproject.org>
*
*   This program is free software: you can redistribute it and/or modify
*   it under the terms of the GNU General Public License as published by
*   the Free Software Foundation, either version 3 of the License, or
*   (at your option) any later version.
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
##########################################################################
"""

from http.client import HTTPSConnection


def obtain_reachable_ip_address(iprtvers):
    urlh = "api64.ipify.org"
    if iprtvers == 4:
        urlh = "api.ipify.org"
    elif iprtvers == 6:
        urlh = "api6.ipify.org"
    try:
        connobjc = HTTPSConnection(urlh)
        connobjc.request("GET", "/")
        response = connobjc.getresponse()
        return response.read().decode("UTF-8")
    except:
        return "Error getting IP address."
