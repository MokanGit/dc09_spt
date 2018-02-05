# ----------------------------
# Class to implement the SIA DC03 message
# (c 2018 van Ovost Automatisering b.v.
# Author : Jacq. van Ovost
# ----------------------------
import time
from param import *
"""

    Copyright (c) 2018  van Ovost Automatisering b.v.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    you may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
class dc03_codes:
    """
    Some special codes
    """
    @staticmethod
    def dc03_is_user(code):
        """
        Codes that have the user number following the code.
        Note that there is no way to transfer a zone in the message
        """
        codes_with_user = { "BC", "CE", "CF", "CJ", "CK", "CL", "CP", "CQ", "CR", "DA", "DB", "EE",
            "JD", "JH", "JK", "JP", "JS", "JT", "JV", "JX", "JY", "JZ", "OC", "OH", "OJ", "OK", "OL", 
            "OP", "OQ", "OR", "OT", "RX"}
        return code in codes_with_user

    @staticmethod
    def dc03_is_door(code):
        """
        Codes that have the door number following the code.
        Note that there is no way to transfer a zone in the message
        """
        codes_with_door = {"DC", "DD", "DE", "DF", "DG", "DH", "DI", "DJ", "DK", "DL", "DM", "DN", 
            "DO", "DP", "DQ", "DR", "DS", "DV", "DW", "DX", "DY", "DZ"}
        return code in codes_with_door

    @staticmethod
    def dc03_is_area(code):
        """
        Codes that have the area number following the code.
        Note that there is no way to transfer a zone in the message
        """
        codes_with_area = {"BA", "CA", "CD", "CG", "CI", "CT", "CW", "FI", "FK", "JA", "JR", "NF", 
            "NL", "NM", "OA", "OG", "OI"}
        return code in codes_with_area

class dc03_msg:
    """
    construct a SIA DC03 message block
    
    This static function builds a message DC03 block for packing into a SIA-DC09 message.
    The DC09 standard document : SIA DC-09-2007 SIA-IP standaard.pdf,
    Refers to the DC07 standard document : SIA DC-07-2001.04 SIA-CIS.pdf,
    Which refers to the DC03 standard document : SIA DC-03-1990.01 (R2000.11)
    
    All of these documents are available from the shop of https://services.securityindustry.org
    
    The static method, dc03event, builds a DC03 message from a map with the various values.
    """
    @staticmethod
    def dc03event(spt_account,  params={}):   
        """
        Construct a DC03 message
        
        Parameters
            spt_account
                the account of the alarm transceiver.
                in most situations this will be used inthe alarm message too, but for situations like a could based receiver,
                the account in the map will be different.
            params
                a map with key-value pairs.
                at this moment only the more commonly used fields are used.
                the currently handled keys are:
                    account
                        the account number.
                        most receivers expect 4 to 8 numeric digits
                    area
                        the area number in which the event happened (area is a part of an installation that can arm and disarm independantly)
                    areaname
                        the name of the area.
                    zone
                        the alarm zone number.
                        the alarm zone is not always transferred. with some events the user number will be used.
                    user
                        the user number doing the action (if available)
                    username
                        the name of the user
                    code
                        the event code in 2 upper case characters according to the DC03 standard.
                    text
                        an descriptive text explaining the event
                    time
                        an time string in format 'hh:mm:ss' or the word 'now'
            all name and text fields can only use ascii characters in the range space to '~' but except [ ] | ^ and /
        """
        account = param.strpar(params,  'account', spt_account)
        area = param.numpar(params,  'area')
        zone = param.numpar(params,'zone')
        user = param.numpar(params,  'user')
        msg = ''
        if account == None:
            msg += '#' + self.account + '|'
        else:
            msg += '#' + account + '|'
        code = param.strpar(params,  'code', None)
        text = param.strpar(params,  'text', None)
        if (code == None or code == 'A') and text != None:
            msg += 'A' + text
        else:
            msg += 'N'
            if code == None:
                code = 'RP'
            if area != None and not dc03_codes.dc03_is_area(code):
                msg += 'ri' + area
                if 'areaname' in params:
                    msg += '^' + params['areaname'] + '^'
            if user != None and not dc03_codes.dc03_is_area(code):
                msg += 'id' + user
                if 'username' in params:
                    msg += '^' + params['username'] + '^'
            if 'time' in params:
                timep = params['time']
                if timep == 'now':
                    timep = time.strftime('%H:%M:%S')
                msg += 'ti' + timep
            msg += code
            if dc03_codes.dc03_is_user(code) and user != None:
                if user != None:
                    msg += user
            elif dc03_codes.dc03_is_area(code) and area != None:
                if area != None:
                    msg += area
            else:
                if zone != None:
                    msg += zone
            if text != None:
                msg += '^' + text + '^'
        return msg + ']'
