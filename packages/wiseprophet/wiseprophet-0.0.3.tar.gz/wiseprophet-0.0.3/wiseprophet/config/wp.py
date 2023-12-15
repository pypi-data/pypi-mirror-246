

o_config = {

    "NODE": {
        "host": "localhost",
        "port": "8800"
    },
    "PY": {
        "host": "54.180.83.158",
        "port": "1338"
    },
    "META_DB": {
        "host": "15.164.216.49",
        "port": "3306",
        "id": "root",
        "passwd": "wise1012",
        "db": "WISE_PROPHET_V1",
        "type": "mysql"
    },
    "LDAP": {
        "host": "54.180.83.158",
        "port": "389"
    },
    "HIVE_DB": {
        "host": "54.180.83.158",
        "port": "3306",
        "id": "hive",
        "passwd": "wise1012",
        "db": "metastore",
        "type": "mysql"
    },
    "WEB_HDFS": {
        "host": "54.180.83.158",
        "port": "8443",
        "monitoring_port":"4040",
        "hadoop-id":"root",
        "ldap-port": "389"
    },
    "WP_API": {
        "host": "54.180.83.158",
        "port": "1338"
    },
    "KAFKA": {
        "host": "13.124.41.117",
        "connectors-port":"8083",
        "topics-port":"8082"
    },
    "JUPYTER": {
        "host": "localhost",
        "port": "8888",
        "token": "wise1012",
        "env-name": "python3"
    },
    "STORAGE_TYPE":"HDFS",
    "API_TYPE": "SPARK",
    "PREPROCESSING_AVAILABLE" : "true",
    "LOAD_BALANCER": "false",
    "LANG": "ko",
    "BACKGROUND": "false",
    "PLATFORM_ID": 1,
    "ADVANCE": "true",
    "CLOUD": "false",
    "CRON": "true",
    "CRYPTO_TYPE":"",
    "DEFAULT_DATA_PATH": "/user/",
    "LIB_PATH": "C://00.Project/01.WB/Source/backup2/wp-platform.v1/projects/wp-server2/lib/instantclient_21_3",
    "LICENSE":"U2FsdGVkX19ha3g0LCXiXkUTgZt14vJUP64Nb4SpF/+QcjNU1TkPqvdgrKhpmki2uuxNeA8qDVubguy05f/mYXszFD2imZusk7pvNNhyOcs=",
    "ML_PATH": "/root/wp-platform.v1/projects/wp-ml"
}


def getConfig(p_type,p_key):
    # print(o_config)
    if p_type != '':
        s_value = o_config[p_type][p_key]
        
        if s_value in ['true', 'false']:
            s_value = o_config[p_type].getboolean(p_key)
    else:
        s_value = o_config[p_key]
    return s_value