from airflow.utils.db import provide_session
from airflow.models import XCom

@provide_session
def _delete_xcoms(session=None):
    '''
    Delete all Xcoms data.
    '''
    num_rows_deleted = 0

    try:
        num_rows_deleted = session.query(XCom).delete()
        session.commit()
    except:
        session.rollback()