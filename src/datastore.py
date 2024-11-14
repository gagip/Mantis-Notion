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
    
    def add(self, key: str, value):
        # key에 해당하는 값이 리스트인지 확인하고, 아니면 리스트로 초기화
        if key in self.data:
            if isinstance(self.data[key], list):
                self.data[key].append(value)
            else:
                raise TypeError(f"키 '{key}'에 대한 값이 리스트가 아닙니다.")
        else:
            self.data[key] = [value]