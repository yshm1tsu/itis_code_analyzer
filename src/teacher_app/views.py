from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from teacher_app.models import Student, Configuration
from teacher_app.models.configuration import ConfigurationStatistics
from teacher_app.utils import (
    create_folder_for_student,
    add_configuration,
    get_results_file,
)


@csrf_exempt
def add_student_view(request):
    if request.method == "POST":
        data = request.POST
        first_name = data["first_name"]
        last_name = data["last_name"]
        patronymic = data["patronymic"]
        configuration_uuid = data["configuration_uuid"]
        configuration = Configuration.objects.filter(uuid=configuration_uuid).first()
        configuration_file_name = configuration.filename
        group = data["group"]
        student = Student.objects.filter(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            group=group,
        ).first()
        if not student:
            Student.objects.create(
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic,
                group=group,
            )
            create_folder_for_student(group, first_name, last_name)
        student_directory_name = f"{group}_{first_name}_{last_name}"
        add_configuration(
            student_directory_name,
            teacher_directory="",
            filename=configuration_file_name,
        )
        return JsonResponse(
            data={
                "message": "Вы успешно вошли в систему",
                "directory_name": student_directory_name,
                "student": student.pk,
                "configuration_file_name": configuration_file_name,
            }
        )


@csrf_exempt
def manage_configuration_statistics(request):
    if request.method == "POST":
        data = request.POST
        if data["type"] == "start":
            student = data["student"]
            configuration = Configuration.objects.filter(
                uuid=data["configuration_uuid"]
            ).first()
            configuration_statistics = ConfigurationStatistics.objects.create(
                student_id=student, configuration=configuration
            )
            return JsonResponse(
                data={
                    "configuration_statistics_id": configuration_statistics.pk,
                    "student": student,
                }
            )
        if data["type"] == "end":
            student = data["student"]
            configuration_statistics_id = data["configuration_statistics"]
            student_data = Student.objects.filter(pk=student).first()
            if not student:
                raise ValueError("No such student")
            student_directory_name = f"{student_data.group}_{student_data.first_name}_{student_data.last_name}"
            results_file = get_results_file(student_directory_name)
            configuration_statistics = ConfigurationStatistics.objects.filter(
                pk=configuration_statistics_id
            ).first()
            configuration_statistics.file.save("results.json", results_file)
            configuration_statistics.time_ended = timezone.now()
            configuration_statistics.save()
        return HttpResponse(status=200)
