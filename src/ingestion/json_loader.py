import json


class JsonLoader:

    def load(self, file_path):
        data = ["data/raw/enterprise_rag/documents_sample.json",
                "data/raw/enterprise_rag/questions_sample.json"]

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if line:
                    data.append(json.loads(line))

        return json.dumps(data, ensure_ascii=False)