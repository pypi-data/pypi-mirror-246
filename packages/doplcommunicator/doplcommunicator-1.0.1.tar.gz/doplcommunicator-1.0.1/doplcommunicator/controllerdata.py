import json

class ControllerData():
    def __init__(self, x: float, y: float, z: float, rx: float, ry: float, rz: float, rw: float):
        self.position = Position(x, y, z)
        self.rotation = Quaternion(rx, ry, rz, rw)

    @classmethod
    def fromJSON(self, controller_data_json):
        controller_data = ControllerData.__new__(ControllerData)
        controller_data.position = Position.fromJSON(json.loads(controller_data_json["position"]))
        controller_data.rotation = Quaternion.fromJSON(json.loads(controller_data_json["rotation"]))
        return controller_data

    def toJSON(self):
        return {
            "position": self.position.toJSON(),
            "rotation": self.rotation.toJSON(),
        }

    def __eq__(self, other): 
        if not isinstance(other, ControllerData):
            # don't attempt to compare against unrelated types
            return NotImplemented
        
        return self.position == other.position and \
            self.rotation == other.rotation

class Position:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def fromJSON(self, position_json):
        position = Position.__new__(Position)
        print(json)
        position.x = float(position_json["x"])
        position.y = float(position_json["y"])
        position.z = float(position_json["z"])
        return position

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __eq__(self, other): 
        if not isinstance(other, Position):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and \
            self.y == other.y and \
            self.z == other.z
    
class Quaternion:
    def __init__(self, x: float, y: float, z: float, w: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    
    @classmethod
    def fromJSON(self, quaternion_json):
        quaternion = Quaternion.__new__(Quaternion)
        quaternion.x = float(quaternion_json["x"])
        quaternion.y = float(quaternion_json["y"])
        quaternion.z = float(quaternion_json["z"])
        quaternion.w = float(quaternion_json["w"])
        return quaternion

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __eq__(self, other): 
        if not isinstance(other, Quaternion):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and \
            self.y == other.y and \
            self.z == other.z and \
            self.w == other.w