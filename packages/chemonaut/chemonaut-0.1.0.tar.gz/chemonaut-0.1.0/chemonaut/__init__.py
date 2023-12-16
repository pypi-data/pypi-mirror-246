from pydantic import BaseModel, Field, validate_call, ConfigDict

# set configuration for @validate_call decorators
config = ConfigDict(strict=True)


class Chemistry(BaseModel):
    left: int = Field(strict=True)
    right: int = Field(strict=True)

    def add(self) -> int:
        return self.left + self.right


@validate_call(config=config)
def concat(param1: int, param2: str = "last") -> str:
    return param2
