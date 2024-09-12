class Function:
    @staticmethod
    def get_meta_func():
        return {'Name': 'GetMeta'}

    @staticmethod
    def get_snapshot_func(snapshot_time):
        return {'Name': 'Snapshot', 'Input': {'SnapshotTime': snapshot_time}}

    @staticmethod
    def get_add_option_info_func(title, tags, description, classification_id, is_hls_index_only=False):
        return {'Name': 'AddOptionInfo',
                'Input': {'Title': title, 'Tags': tags, 'Description': description,
                          'ClassificationId': classification_id, "IsHlsIndexOnly": is_hls_index_only}}

    @staticmethod
    def get_add_material_option_info_func(title, tags, description, category, record_type, format_input):
        return {'Name': 'AddOptionInfo',
                'Input': {'Title': title, 'Tags': tags, 'Description': description, 'Category': category,
                          'RecordType': record_type, 'Format': format_input}}

    @staticmethod
    def get_start_workflow_func(template_id, templates=None):
        return {'Name': 'StartWorkflow', 'Input': {'TemplateId': template_id, 'Templates': templates}}

    @staticmethod
    def get_start_workflow_template_func(templates):
        return {'Name': 'StartWorkflow', 'Input': {'Templates': templates}}

    @staticmethod
    def get_caption_func(title, format, vid, fid, language, source, tag, action_type, store_uri, auto_publish=False):
        return {'Name': 'CaptionUpload',
                'Input': {'Title': title, 'Format': format, 'Vid': vid, 'Fid': fid, 'Language': language,
                          'Source': source, 'Tag': tag, 'ActionType': action_type, 'StoreUri': store_uri,
                          'AutoPublish': auto_publish}}

    @staticmethod
    def get_encryption_func(conf, policy):
        return {'Name': 'Encryption', 'Input': {'Config': conf, 'PolicyParams': policy}}
