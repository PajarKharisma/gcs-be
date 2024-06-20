from config import context

def setContext(payload):
    for key, value in payload.items():
        context.VALUES[key] = value

def getContext():
    return context.VALUES
