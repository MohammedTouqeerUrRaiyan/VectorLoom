import chardet

class TxtLoader:
    def load(self,  file_path: str) -> list[str]:
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # Read the first 10KB for encoding detection
            result = chardet.detect(raw_data)
            encoding = result['encoding']
        
        with open(file_path, 'r', encoding=encoding) as f:
            text = f.read()
        
        return [text]