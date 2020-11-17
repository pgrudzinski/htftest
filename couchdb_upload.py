import cloudant

from openhtf.util import data, format_string
from openhtf.core import test_record

from openhtf.util import conf

conf.declare('db_url', default_value='http://db:5984',
             description='URL of the database to upload test records.')
conf.declare('db_user')
conf.declare('db_pass', )
conf.declare('db_name', default_value='test_records',
             description='Name of the database to upload test records to.')

class CouchDBUploader():
    """Return an output callback that writes test records to CouchDB or Cloudant.

    Example test_id might be:
    '{dut_id}_{metadata[test_name]}_{start_time_millis}'

    Args:
        id_pattern: A format string specifying database ID will be formated with
            TestRecord as a dictionary. 
        upload_attachements: Whether attachements should be uploaded to a database 
            together with TestRecord.
        db_url: URL of the database to upload test records.
        db_name: Name of the database to upload test records to.
        db_user: Username used to connect to the database.
        db_pass: Password used to connect to the database.
    """
    @conf.inject_positional_arguments
    def __init__(db_user, db_pass, db_url, db_name, id_pattern=None):
        self.db_client_context = cloudant.couchdb(db_user, db_pass, url=db_url)
        self.id_pattern = id_pattern
        self.db_name = db_name

    def __call__(self, test_record):
        record_dict = data.convert_to_base_types(
            test_record, json_safe=(not self.allow_nan)
        )
        if id_pattern is not None:
            record_dict['_id'] = format_string(self.id_pattern, record_dict)
        with self.db_client_context as client:
            db = client.get_database(self.db_name)
            db.create_document(test_record)


