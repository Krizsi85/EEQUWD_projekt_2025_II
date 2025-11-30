class ProgramLoader:
    @staticmethod
    def load_paths(path):
        result = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                result.append(line)
        return result
