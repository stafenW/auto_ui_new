from django.db import models


class Case(models.Model):
    process_id = models.IntegerField()
    title = models.CharField(max_length=200, null=True, blank=True)
    code = models.TextField()
    operations = models.TextField()
    has_norm = models.IntegerField(default=0)
    is_running = models.IntegerField(default=0)
    is_waiting = models.IntegerField(default=0)
    last_succ = models.IntegerField(default=0)
    run_log = models.TextField(max_length=2000, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=200, null=True, blank=True)
    last_run_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_comp_count = models.IntegerField(default=0, null=True, blank=True)
    last_error_count = models.IntegerField(default=0, null=True, blank=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "processId": self.process_id,
            "hasNorm": self.has_norm,
            "isWaiting": self.is_waiting,
            "isRunning": self.is_running,
            "lastSucc": self.last_succ,
            "runLog": self.run_log,
            "createTime": self.create_time,
            "tags": str(self.tags).split(','),
            "lastRunTime": self.last_run_time,
        }

    class Meta:
        db_table = "case"


# Create your models here.
class Process(models.Model):
    title = models.CharField(max_length=100)
    describe = models.CharField(max_length=500, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "describe": self.describe,
            "operations": [],
            "createTime": self.create_time
        }

    class Meta:
        db_table = "process"


class Operation(models.Model):
    process_id = models.ForeignKey(to=Process, to_field='id', on_delete=models.CASCADE)
    process_index = models.IntegerField()
    type = models.IntegerField(default=0)
    ope_type = models.CharField(max_length=30)
    ope_name = models.CharField(max_length=200, null=True, blank=True)
    open_url = models.CharField(max_length=1000, null=True, blank=True)
    find_type = models.CharField(max_length=20, null=True, blank=True)
    find_val = models.CharField(max_length=200, null=True, blank=True)
    input_val = models.CharField(max_length=255, null=True, blank=True)
    is_enter = models.IntegerField(default=0, null=True, blank=True)
    time_limit = models.IntegerField(null=True, blank=True)
    var_ope = models.CharField(max_length=30, null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    other_process = models.IntegerField(null=True, blank=True)
    button = models.CharField(max_length=20, null=True, blank=True)

    def get_finder(self):
        return {
            "findType": self.find_type,
            "findVal": self.find_val
        }

    def get_var_ope(self):
        return {
            "option": self.var_ope
        }

    def to_dict(self):
        value = {}
        if self.ope_type == "open-page":
            value = {
                "url": self.open_url
            }
        elif self.ope_type == "jump":
            value = {
                "url": self.open_url
            }
        elif self.ope_type == "click":
            value = {
                "elFinder": self.get_finder()
            }
        elif self.ope_type == "try-to-click":
            value = {
                "elFinder": self.get_finder()
            }
        elif self.ope_type == "input":
            value = {
                "elFinder": self.get_finder(),
                "inputVal": self.input_val,
                "isEnter": 1 if self.is_enter else 0
            }
        elif self.ope_type == "wait":
            value = {
                "timeLimit": self.time_limit
            }
        elif self.ope_type == "wait-el":
            value = {
                "elFinder": self.get_finder(),
                "timeLimit": self.time_limit
            }
        elif self.ope_type == "snapshot":
            value = {
                "varOpe": self.get_var_ope()
            }
        elif self.ope_type == "snapshot-el":
            value = {
                "elFinder": self.get_finder(),
                "varOpe": self.get_var_ope()
            }
        elif self.ope_type == "get-text":
            value = {
                "elFinder": self.get_finder(),
                "varOpe": self.get_var_ope()
            }
        elif self.ope_type == "other-process":
            value = {
                "otherProcessId": self.other_process
            }
        elif self.ope_type == "keyword-opt":
            value = {
                "keywordOpt": self.button
            }
        return {
            "id": self.id,
            "processId": self.process_id.id if isinstance(self.process_id, Process) else self.process_id,
            "processIndex": self.process_index,
            "type": self.type,
            "opeType": self.ope_type,
            "opeName": self.ope_name,
            "value": value,
        }

    def set_open_url(self, url):
        self.open_url = url

    def set_finder(self, finder):
        self.find_type = finder.get("findType")
        self.find_val = finder.get("findVal")

    def set_time_limit(self, time_limit):
        self.time_limit = time_limit

    def set_input_val(self, input_val, is_enter=0):
        self.input_val = input_val
        if not is_enter:
            is_enter = 0
        self.is_enter = is_enter

    def set_var_ope(self, val):
        self.var_ope = val.get("option")

    def set_other_process(self, process_id):
        self.other_process = process_id

    def set_keyword_opt(self, button):
        self.button = button

    class Meta:
        db_table = "operation"
