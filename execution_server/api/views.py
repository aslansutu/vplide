import os
from django.http import JsonResponse
from rest_framework.views import APIView
from api.utils import execute_files

from api.script import evaluate_python_file
from . import serializers


class Evaluate(APIView):
    serializer_class = serializers.FileEvaluateSerializer

    def post(self, request, *args, **kwargs):
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        from django.conf import settings

        try:
            data = request.data
            pl_language = data["pl_language"]
            del data["pl_language"]
        except Exception as e:
            error_response = {
                "status": 400,
                "detail": {
                    "message": f"Something happened.",
                    "exception_detail": f"{e}:",
                },
            }
            return JsonResponse(error_response)

        file_name_list = []
        for file in data.values():
            file_name_list.append(file.name)

            path = f"{settings.MEDIA_ROOT}/{file.name}"
            if os.path.exists(path):
                os.remove(path)

            path = default_storage.save(
                f"{file.name}", ContentFile(eval(file.read().decode("UTF-8")))
            )
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        volume_path = settings.MEDIA_ROOT
        output_path = f"{volume_path}/output.txt"

        if os.path.exists(output_path):
            os.remove(output_path)

        response_j = execute_files(
            pl_language, volume_path, file_name_list, output_path
        )
        # for fname in file_name_list:
        #     path = f"{volume_path}/{fname}"
        #     if os.path.exists(path):
        #         os.remove(path)

        if response_j["status"] == 200:
            with open(settings.MEDIA_ROOT + "/output.txt", "r") as f:
                file_data = f.read()
            response = {
                "detail": {"message": "File successfully run!"},
                "content": file_data,
            }
            return JsonResponse(response)
        else:
            error_response = {
                "status": 400,
                "detail": {
                    "message": f"An error occurred while running the file.",
                },
            }
            return JsonResponse(error_response)


class EvaluateScripts(APIView):
    serializer_class = serializers.FileEvaluateSerializer

    def post(self, request, *args, **kwargs):
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        from django.conf import settings

        try:
            data = request.data
            pl_language = data["pl_language"]
            del data["pl_language"]
        except Exception as e:
            error_response = {
                "status": 400,
                "detail": {
                    "message": f"Something happened.",
                    "exception_detail": f"{e}:",
                },
            }
            return JsonResponse(error_response)

        file_name_list = []
        for file in data.values():
            file_name_list.append(file.name)

            path = f"{settings.MEDIA_ROOT}/{file.name}"
            if os.path.exists(path):
                os.remove(path)

            path = default_storage.save(
                f"{file.name}", ContentFile(eval(file.read().decode("UTF-8")))
            )
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

        volume_path = settings.MEDIA_ROOT
        output_path = f"{volume_path}/output.txt"

        if os.path.exists(output_path):
            os.remove(output_path)

        python_file = f'{settings.MEDIA_ROOT}/main.py'
        evaluation_script = f'{settings.MEDIA_ROOT}/evaluation_script.txt'
        response_j = evaluate_python_file(python_file, evaluation_script)
        print(response_j)

        if response_j["status"] == 200:
            response = {
                "detail": {"message": "File successfully run!"},
                "content": response_j["result"],
            }
            return JsonResponse(response)
        else:
            error_response = {
                "detail": {"message": "An error occurred while running the file."},
                "content": response_j["points"],
            }
            return JsonResponse(error_response)
