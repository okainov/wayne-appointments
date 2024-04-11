import datetime
import json
import re

import requests


class Wayne:
    # CPL permits in Wayne County, MI, USA
    def get_token(self, response):
        text = response.text
        tokens = re.findall("__RequestVerificationToken.*?value=\"(.*?)\"", text)
        return tokens[0]

    def get_appointments(self):
        s = requests.Session()
        first_url = "https://go.nemoqappointment.com/Booking/Booking/Index/v86fs3t6j"
        next_url = "https://go.nemoqappointment.com/Booking/Booking/Next/v86fs3t6j"
        response = s.get(first_url)
        token = self.get_token(response)

        termin_data = {
            "__RequestVerificationToken": token,
            'ServiceGroupId': 451,  # CPL
            'FormId': 1,
            'StartNextButton': "Make an appointment",
        }
        response = s.post(next_url, termin_data)
        token = self.get_token(response)

        # Accept conditions
        termin_data = {
            "__RequestVerificationToken": token,
            'NumberOfPeople': 1,
            'AcceptInformationStorage': True,
            "Next": "Next",
            "AgreementText": "qqq",
        }
        response = s.post(next_url, termin_data)
        token = self.get_token(response)

        today = datetime.datetime.now().strftime("%m/%d/%Y")
        termin_data = {
            "__RequestVerificationToken": token,
            "TimeSearchFirstAvailableButton": "First available time",
            "ServiceTypeId": 2403,  # CPL
            "SectionId": 290,  # Office
            "FormId": 1,
            "FromDateString": today,
            "RegionId": 0,  # All
        }
        response = s.post(next_url, termin_data)
        text = response.text
        result = {"status": "ok",
                  "appointments": []}
        if "No available times could be found" in text:
            result["status"] = "Nothing"
        appointments = re.findall("<div.*?timeTableCell(.*?)<.div>", text, flags=re.S)
        for appt in appointments:
            appt_time = re.findall("data-fromdatetime=\"(.*?)\"", appt)[0]
            appt_status = re.findall("aria-label=\"(.*?)\"", appt)[0]
            result["appointments"].append({"datetime": appt_time, "status": appt_status})

        return result
