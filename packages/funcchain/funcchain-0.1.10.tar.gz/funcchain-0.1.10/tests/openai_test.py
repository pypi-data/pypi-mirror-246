from funcchain import chain, settings
from pydantic import BaseModel, Field


class Task(BaseModel):
    name: str
    description: str


class TodoList(BaseModel):
    tasks: list[Task]


def todo_list(job_title: str) -> TodoList:
    """
    Create a todo list for a perfect day for the given job.
    """
    return chain()


def test_gpt_35_turbo() -> None:
    settings.MODEL_NAME = "openai/gpt-3.5-turbo"

    assert isinstance(
        todo_list("software engineer"),
        TodoList,
    )


def test_gpt4() -> None:
    settings.MODEL_NAME = "openai/gpt-4"

    assert isinstance(
        todo_list("software engineer"),
        TodoList,
    )


def test_vision() -> None:
    from PIL import Image

    settings.MODEL_NAME = "openai/gpt-4-vision-preview"

    class Analysis(BaseModel):
        description: str = Field(description="A description of the image")
        objects: list[str] = Field(description="A list of objects found in the image")

    def analyse(image: Image.Image) -> Analysis:
        """
        Analyse the image and extract its
        theme, description and objects.
        """
        return chain()

    assert isinstance(
        analyse(Image.open("examples/assets/old_chinese_temple.jpg")),
        Analysis,
    )


def test_api_key_failure() -> None:
    settings.MODEL_NAME = "gpt-3.5-turbo-1106"
    settings.OPENAI_API_KEY = "test"

    try:
        print(todo_list("software engineer"))
    except Exception:
        assert True
    else:
        assert False, "API Key failure did not occur."


if __name__ == "__main__":
    # test_gpt_35_turbo()
    # test_gpt4()
    # test_vision()
    test_api_key_failure()
