from config.environment_tools import get_db_name, get_db_user, get_db_port, get_db_pw, get_db_host

CONNECTION_URI_TEMPLATE = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'


def get_connection_uri(user, password, host, database, port=3306):
    return CONNECTION_URI_TEMPLATE.format(user=user,
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)


def get_connection_uri_from_env():
    user = get_db_user()
    password = get_db_pw()
    host = get_db_host()
    database = get_db_name()
    port = get_db_port()

    for k, v in locals().items():
        if not v or len(v) == 0:
            raise EnvironmentError('"{}" of database is empty in environment'.format(k))

    return CONNECTION_URI_TEMPLATE.format(user=user,
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)

