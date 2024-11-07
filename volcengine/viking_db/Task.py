class Task(object):
    def __init__(self, collection_name, create_time, process_info, task_id, task_params, task_status, task_type, update_person, update_time):
        self.collection_name = collection_name
        self.create_time = create_time
        self.process_info = process_info
        self.task_id = task_id
        self.task_params = task_params
        self.task_status = task_status
        self.task_type = task_type
        self.update_person = update_person
        self.update_time = update_time

