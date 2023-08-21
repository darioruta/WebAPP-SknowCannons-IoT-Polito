import json

def getLocalities():
    #RITORNA UNA LISTA DI LOCALITY NAMES [bardo, sauze,...]
    file  = open("data/network.json")
    data = json.load(file)
    output = []
    print("\n\n\n\n\n\n\nRITORNO LE LOCALITA\n\n\n\n\n\n")
    for l in data["localities"]:
       output.append(l["name"])
    out_d = { "data": output}
    return json.dumps(out_d)

def getSlopesByLocalityName(loc):
    # http://127.0.0.1:8080/edit/getSlopesByLocalityName?loc=Bardonecchia
    # body: empty
    # return: ["SlopeA", "SlopeB"] 

    file  = open("data/network.json")
    data = json.load(file)
    slope_names = []
    for locality in data['localities']:
        if str(locality["name"]) == str(loc):
            for slope  in locality["slopes"]:
                slope_names.append(slope["name"])
    out_d = { "data": slope_names}

    print(out_d)
    return json.dumps(out_d)
    

def getSectorsBySlopeNameByLocalityName(loc, slope):
    file  = open("data/network.json")
    data = json.load(file)
    sec_names = []
    for l in data["localities"]:
        if l["name"]==loc:
            for s in l["slopes"]:
                if s["name"]== slope:
                    for sec in s["sectors"]:
                        sec_names.append(sec["name"])
    out_d = { "data": sec_names}

    print(out_d)
    return json.dumps(out_d)
    


getSlopesByLocalityName("Bardonecchia")

getSectorsBySlopeNameByLocalityName("Bardonecchia", "SlopeA")