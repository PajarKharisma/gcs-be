def success(data):
    return {
        'code' : 200,
        'data_length' : len(data),
        'data' : data
    }

def error(msg):
    return {
        'code' : 500,
        'messages' : msg
    }
