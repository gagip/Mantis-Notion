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
        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def get(self, key: str) -> list[int]:
        result = self.data.get(key)
        assert isinstance(result, list | None)
        if not result:
            return []
        return result
    
    def add(self, key: str, value):
        if key not in self.data:
            self.data[key] = [value]
            return
        
        if isinstance(self.data[key], list):
            self.data[key].append(value)
        else:
            raise TypeError(f'키 \'{key}\'에 대한 값이 리스트가 아닙니다.')