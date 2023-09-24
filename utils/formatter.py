def formatData(rawData):
    try:
        cleanData = rawData.replace("\n", "")
        cleanData = cleanData.replace("\r", "")
        if len(cleanData) > 0:
            data = cleanData.split(':')
            return {
                'roll': float(data[1].strip().split(" ")[0]),
                'pitch': float(data[2].strip().split(" ")[0]),
                'yaw': float(data[3].strip().split(" ")[0]),
                'lat': float(data[4].strip().split(" ")[0]),
                'long': float(data[5].strip().split(" ")[0]),
                'alt': float(data[6].strip().split(" ")[0]),
            }
    except:
        pass
        