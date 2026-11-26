from jsonschema import Draft202012Validator, ValidationError
from cs329z_hw1.types import ToolResult

class ToolRegistry:
    def __init__(self,tools):
        #把tool存放进去
        self.tool={}
        for tool in tools:
            self.tool[tool.name] = tool


    def schemas(self)->list[dict]:
        # 每个工具返回一个dict，只能有name, description, 和 parameter
        schemas = []
        for tool in self.tool.values():
            schemas.append({"name": tool.name, "description": tool.description, "parameters": tool.parameters})
        return schemas

    def validate(self, name: str, args: dict):
        # 名字不在 self.tools 里 → return ToolResult("unknown_tool", "说明文字")
        if name not in self.tool:
            return ToolResult("unknown_tool", f"Tool '{name}' is not registered.")
        # 用 jsonschema 检查 args；不合格 → return ToolResult("invalid_args", "说明文字")
        # 都没问题 → return None
        spec=self.tool[name]
        validator=Draft202012Validator(spec.parameters)
        try:
            validator.validate(args)
            return None
        except ValidationError as e:
            return ToolResult("invalid_args", f"Invalid arguments for tool '{name}': {e.message}")
        



    def execute(self, name: str, args: dict) -> ToolResult:
        # 先调用 self.validate；如果返回的不是 None，直接把它返回
        # try: 调用 fn(**args)，成功 → ToolResult("ok", str(返回值))
        # except Exception as e: → ToolResult("tool_error", 包含 str(e) 的说明文字)
        validation_result = self.validate(name, args)
        if validation_result != None:
            return validation_result
        try:
            result = self.tool[name].fn(**args)
            return ToolResult("ok", str(result))
        except Exception as e:
            return ToolResult("tool_error", f"Tool '{name}' raised an error: {e}")
    