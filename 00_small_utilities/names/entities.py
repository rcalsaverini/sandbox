from typing import List, TypedDict
from dataclasses import dataclass

class PromptMessage(TypedDict):
    role: str
    content: str

Prompt = List[PromptMessage]

class Example(TypedDict):
    item: str
    label: str

@dataclass
class Task:
    description: str
    examples: List[Example]
    unclassified: List[str]
    
    def render_example(self):
        return ",\n".join([f"        '{example['item']}': '{example['label']}'" for example in self.examples])
    
    def render_unclassified(self):
        return ",\n".join([f"        '{item}'" for item in self.unclassified])
    
    def render(self) -> str:
        return (
            "CREATE TASK(\n"
            f"    DESCRIPTION='{self.description}',\n"
            f"    EXAMPLES={{\n{self.render_example()}\n    }},\n"
            f"    UNCLASSIFIED={{\n{self.render_unclassified()}\n    }}\n"
            ")"
        )
        
    def read_examples(self):
        print("Enter examples as item,label pairs. Leave empty to finish.")
        has_new_example = True
        while has_new_example:
            user_input = input("Enter item,label $>")
            if user_input.strip() == "":
                has_new_example = False
            else:
                item, label = user_input.split(",")
                self.examples.append({"item": item.strip(), "label": label.strip()})
        
    def read_unclassified(self):
        print("Enter unclassified items. Leave empty to finish.")
        has_new_item = True
        while has_new_item:
            item = input("Enter item $>")
            if item.strip() == "":
                has_new_item = False
            else:
                self.unclassified.append(item.strip())
                
    @classmethod
    def from_file(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()
            
        description = lines[0].strip()
        examples = []
        unclassified = []
        for line in lines[1:]:
            if line.strip() == "":
                continue
            elif ',' in line:
                item, label = line.split(",")
                examples.append({"item": item.strip(), "label": label.strip()})
            else:
                unclassified.append(line.strip())
        return Task(description, examples, unclassified)