from phospho.collection import Collection

from typing import Dict, Optional, List


class Task:
    def __init__(self, client, task_id: str, _content: Optional[dict] = None):
        from phospho.client import Client

        self._client: Client = client
        self._task_id: str = task_id
        self._content: Optional[dict] = _content

    @property
    def id(self):
        return self._task_id

    @property
    def content(self):
        """
        WARNING : can cause divergence with the server
        """
        if self._content is None:
            # Query the server
            response = self._client._get(f"/tasks/{self._task_id}")
            self._content = response.json()

        return self._content

    def refresh(self) -> None:
        """
        Refresh the content of the task from the server
        Done inplace
        """
        response = self._client._get(f"/tasks/{self._task_id}")
        self._content = response.json()

    # def update(self, metadata: Optional[dict] = None, data: Optional[dict] = None):
    #     if metadata is None and data is None:
    #         raise ValueError(
    #             "You must provide either metadata or data to update a task"
    #         )

    #     payload = {
    #         "metadata": metadata or {},
    #         "data": data or {},
    #     }

    #     response = self._client._post(f"/tasks/{self._task_id}/update", payload=payload)

    #     return Task(self._client, response.json()["task_id"])

    # List steps
    # def list_steps(self):
    #     """
    #     Use a Generator? -> would enable streaming
    #     TODO : add filters, limits and pagination
    #     """
    #     response = self._client._get(f"/tasks/{self._task_id}/steps")

    #     steps_list = []

    #     for step_content in response.json()["steps"]:
    #         steps_list.append(
    #             Step(self._client, step_content["step_id"], _content=step_content)
    #         )

    #     return steps_list


class TaskCollection(Collection):
    # Get a task
    def get(self, task_id: str):
        """Get a task by id"""
        # TODO: add filters, limits and pagination

        response = self._client._get(f"/tasks/{task_id}")

        return Task(self._client, response.json()["id"], _content=response.json())

    # Create a task
    def create(
        self,
        session_id: str,
        sender_id: str,
        input: str,
        output: str,
        additional_input: Optional[dict] = None,
        additional_output: Optional[dict] = None,
        data: Optional[dict] = None,
    ):
        """
        Create a task
        """
        payload: Dict[str, object] = {
            "session_id": session_id,
            "sender_id": sender_id,
            "input": input,
            "additional_input": additional_input or {},
            "output": output,
            "additional_output": additional_output or {},
            "data": data or {},
        }

        response = self._client._post(f"/tasks", payload=payload)

        return Task(self._client, response.json()["id"])

    # Get all tasks (filters can be applied)
    def get_all(self) -> List[Task]:
        """Returns a list of all of the project tasks"""
        response = self._client._get(
            f"/projects/{self._client._project_id()}/tasks",
        )
        return [
            Task(client=self._client, task_id=task["id"], _content=task)
            for task in response.json()["tasks"]
        ]


# Create a task

# Update a task

# Get the all steps for a task
