import os
from django.http import JsonResponse
from django.conf import settings
from rest_framework.views import APIView
import requests
import json


class Login(APIView):
    def validate(self, data, required_fields=[]):
        missing_fields = list(filter(lambda field: field not in data, required_fields))
        return missing_fields

    def post(self, request):

        try:
            data = request.data
        except Exception as e:
            error_response = {
                "status": 400,
                "detail": {
                    "message": f"Something happened.",
                    "exception_detail": f"{e}:",
                },
            }
            return JsonResponse(error_response)

        username = data.get("username", None)
        password = data.get("password", None)
        service = data.get("service", None)

        missing = self.validate(
            request.data,
            ["username", "password", "service"],
        )
        if missing:
            error_reponse = {
                400,
                {"detail": {"message": f"missing parameter(s): {', '.join(missing)}"}},
            }
            return JsonResponse(error_reponse)

        session = requests.Session()

        url = f"{settings.MOODLE_SERVER_URL}/login/token.php?username={username}&password={password}&service={service}"

        response = session.get(url)

        response_j = json.loads(response.content.decode("utf-8"))

        return JsonResponse(response_j)


class GetCourses(APIView):
    def validate(self, data, required_fields=[]):
        missing_fields = list(filter(lambda field: field not in data, required_fields))
        return missing_fields

    def post(self, request):

        try:
            data = request.data
        except Exception as e:
            error_response = {
                "status": 400,
                "detail": {
                    "message": f"Something happened.",
                    "exception_detail": f"{e}:",
                },
            }
            return JsonResponse(error_response)

        wstoken = data.get("wstoken", None)

        wsfunction = "core_course_get_courses"
        url = f"{settings.MOODLE_SERVER_URL}/webservice/rest/server.php?wstoken={wstoken}&wsfunction={wsfunction}&moodlewsrestformat=json"

        missing = self.validate(
            request.data,
            ["wstoken"],
        )

        if missing:
            error_reponse = {
                400,
                {"detail": {"message": f"missing parameter(s): {', '.join(missing)}"}},
            }
            return JsonResponse(error_reponse)

        session = requests.Session()

        response = session.get(url)
        response_j = json.loads(response.content.decode("utf-8"))

        return JsonResponse({"status": 200, "courses": response_j})


class UpdateGrade(APIView):
    def validate(self, data, required_fields=[]):
        missing_fields = list(filter(lambda field: field not in data, required_fields))
        return missing_fields

    def post(self, request):

        try:
            data = request.data
        except Exception as e:
            error_response = {
                "status": 400,
                "detail": {
                    "message": f"Something happened.",
                    "exception_detail": f"{e}:",
                },
            }
            return JsonResponse(error_response)

        missing = self.validate(
            request.data,
            ["wstoken", "course_id"],
        )

        if missing:
            error_reponse = {
                400,
                {"detail": {"message": f"missing parameter(s): {', '.join(missing)}"}},
            }
            return JsonResponse(error_reponse)

        wstoken = data.get("wstoken", None)
        course_id = data.get("course_id", None)

        wsfunction = "core_grade_update_grades"
        url = f"{settings.MOODLE_SERVER_URL}/webservice/rest/server.php?wstoken={wstoken}&wsfunction={wsfunction}&moodlewsrestformat=json"

        session = requests.Session()

        payload = {"volume_path": settings.MEDIA_ROOT, "course_id": course_id}

        response = session.post(url, json=payload)
        response_j = json.loads(response.content.decode("utf-8"))

        return JsonResponse(
            {"status": 200, "detail": {"message": response_j["message"]}}
        )


class GetGradesByCourseID(APIView):
    def validate(self, data, required_fields=[]):
        missing_fields = list(filter(lambda field: field not in data, required_fields))
        return missing_fields

    def post(self, request):

        try:
            data = request.data
        except Exception as e:
            error_response = {
                "status": 400,
                "detail": {
                    "message": f"Something happened.",
                    "exception_detail": f"{e}:",
                },
            }
            return JsonResponse(error_response)

        missing = self.validate(
            request.data,
            ["wstoken", "course_id"],
        )

        if missing:
            error_reponse = {
                400,
                {"detail": {"message": f"missing parameter(s): {', '.join(missing)}"}},
            }
            return JsonResponse(error_reponse)

        wstoken = data.get("wstoken", None)
        course_id = data.get("course_id", None)

        wsfunction = "core_grades_get_grades"
        url = f"{settings.MOODLE_SERVER_URL}/webservice/rest/server.php?wstoken={wstoken}&wsfunction={wsfunction}&moodlewsrestformat=json"

        session = requests.Session()

        payload = {"volume_path": settings.MEDIA_ROOT, "course_id": course_id}

        response = session.post(url, json=payload)
        response_j = json.loads(response.content.decode("utf-8"))

        data = dict()
        data["courses"] = response_j["courses"]

        return JsonResponse({"status": 200, "courses": response_j})
