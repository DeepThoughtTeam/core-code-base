from django.db import models
from django.conf import settings
from django.utils.html import escape


# The core file model
class FileBase(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100, blank=False)
    type = models.CharField(max_length=30, blank=False)  # PARAM, MODEL, TRAIN_IN, TEST_IN, TRAIN_OUT, TEST_OUT
    content = models.FileField(upload_to='files')  # include the path information


class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=30, blank=False)

    learning_rate = models.FloatField(blank=False)
    num_iter = models.IntegerField(blank=False)
    out_dim = models.IntegerField(blank=False)

    train_in = models.OneToOneField(FileBase, related_name='train_in', on_delete=models.CASCADE)
    train_out = models.OneToOneField(FileBase, related_name='train_out', on_delete=models.CASCADE, null=True)
    test_in = models.OneToOneField(FileBase, related_name='test_in', on_delete=models.CASCADE)
    test_out = models.OneToOneField(FileBase, related_name='test_out', on_delete=models.CASCADE, null=True)
    # The file instance for the model
    model = models.OneToOneField(FileBase, related_name='model', on_delete=models.CASCADE, null=True)
    # The file instance for the parameter
    parameter = models.OneToOneField(FileBase, related_name='parameter', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_now_add=True)
    completed_status = models.CharField(max_length=30, default='Incompleted')

    def __unicode__(self):
        return u'%s %s %s' % (self.author, self.name, self.create_time)

    def __str__(self):
        return self.__unicode__()

    @staticmethod
    def get_tasks(author):
        return Task.objects.filter(author=author).order_by("create_time").reverse()

    # format the task entry into html
    @property
    def html(self):
        format_str = "<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td></td> </tr>"
        name = escape(self.name)
        create_time = escape(self.create_time)
        finish_time = escape(self.finish_time)
        completed_status = escape(self.completed_status)

        completed_str = ""
        if completed_status == "Completed":
            # <a href="/nngarage/get-task-detailed-info/taks3">Completed</a>
            completed_str = '<a href=\'/nngarage/get-task-detailed-info/' + name + '\'>Completed</a>'
        else:
            completed_str = completed_status
        
        return format_str % (name, create_time, finish_time, completed_str)
