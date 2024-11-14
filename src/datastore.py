import json

class DataStore:
    def __init__(self, path: str):
        self.data = {}
        self.path = path
        try:
            with open(path, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open(path, 'w') as f:
                json.dump(self.data, f)
    
    def save(self):
        # self.data를 json 파일로 저장
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def get(self, key: str):
        # key에 해당하는 값을 반환
        return self.data.get(key)
    
    def set(self, key: str, value):
        # key와 value를 저장
        self.data[key] = value
        
    def delete(self, key: str):
        # key에 해당하는 값을 삭제
        del self.data[key]
    