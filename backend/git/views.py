from django.http import JsonResponse
from rest_framework.views import APIView
from . import scripts
import os


class InitializeRepository(APIView):
    def post(self, request, *args, **kwargs):
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile

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

        path = f"{settings.MEDIA_ROOT}"
        file = "file_0.py"
        default_storage.save(f"{file.name}", ContentFile(eval(data.decode("UTF-8"))))

        repo = scripts.initialize(path)

        response = {"detail": {"message": "Repo successfully created!"}, "repo": repo}
        return JsonResponse(response)


class CommitChanges(APIView):
    def post(self, request, *args, **kwargs):
        from django.conf import settings
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile

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

        repo_path = f"{settings.MEDIA_ROOT}" + "/.git"
        repository = scripts.getRepository(repo_path)
        if repository == None:
            repository = scripts.initialize(repo_path)

        file = "file_0.py"
        with open(os.path.join(f"{settings.MEDIA_ROOT}", file), "w") as stream:
            stream.write(data)

        scripts.commit(repo_path, "Adil", "adil.ahmadli@proton.me")

        response = {"detail": {"message": "Changes saved!"}}
        return JsonResponse(response)


class GetSourceCode(APIView):
    def get(self, request, *args, **kwargs):
        pass
