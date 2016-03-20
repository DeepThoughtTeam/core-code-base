from django.db import models
from django.conf import settings


# The core file model
class FileBase(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=30, blank=False)  # PARAM, MODEL, TRAIN_IN, TEST_IN, TRAIN_OUT, TEST_OUT
    content = models.FileField(upload_to='files')  # include the path information


class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=30, blank=False)

    train_in = models.OneToOneField(FileBase, related_name='train_in', on_delete=models.CASCADE)
    train_out = models.OneToOneField(FileBase, related_name='train_out', on_delete=models.CASCADE)
    test_in = models.OneToOneField(FileBase, related_name='test_in', on_delete=models.CASCADE)
    test_out = models.OneToOneField(FileBase, related_name='test_out', on_delete=models.CASCADE)
    # The file instance for the model
    model = models.OneToOneField(FileBase, related_name='model', on_delete=models.CASCADE)
    # The file instance for the parameter
    parameter = models.OneToOneField(FileBase, related_name='parameter', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(default='')
    completed_status = models.CharField(max_length=30, default='Incompleted')

    def __unicode__(self):
        return u'%s %s %s' % (self.author, self.name, self.create_time)

    @staticmethod
    def get_tasks(author):
        return Task.objects.filter(author=author).order_by("create_time").reverse()

    # format the task entry into html
    def html(self):
        format_str = "<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td><a>%s</a></td> </tr>"
        name = self.name
        model_name = self.model.name
        para_name = self.parameter.name
        create_time = self.create_time
        finish_time = self.finish_time
        completed_status = self.completed_status
        return format_str % (name, model_name, para_name, create_time, finish_time, completed_status)
