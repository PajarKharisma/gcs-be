from config import context

def setContext(payload, type='INPUT'):
    if type == 'INPUT':
        for key, value in payload.items():
            context.INPUT_VALUES[key] = value
    else:
        for key, value in payload.items():
            context.OUTPUT_VALUES[key] = value

def getContext(type='INPUT'):
    if type == 'INPUT':
        return context.INPUT_VALUES
    else:
        return context.OUTPUT_VALUES
