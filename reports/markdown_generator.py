class MarkdownGenerator:
    def generate(self, data):
        res = f"# {data.title}\n"
        for sec in data.sections:
            res += f"## {sec.title}\n{sec.content}\n"
        return res
