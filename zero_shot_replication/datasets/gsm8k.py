import os
from typing import Any, Generator, List, Tuple

from zero_shot_replication.helpers import BaseDataset, ProblemType
from zero_shot_replication.helpers.utils import (
    get_pset_inputs_dir,
    load_file_or_raise,
)


class GSM8KDataset(BaseDataset):
    """A concrete class to provide GSM8K problems for the runner."""

    INPUT_FILE = "test.jsonl"

    @property
    def raw_prompt(selfdict) -> str:
        """Concrete method the raw prompt for a GSM8K problem."""
        raise NotImplementedError("GSM8KDataset does not have a raw prompt.")

    @property
    def input_paths(self) -> List[str]:
        """Concrete method to get a list over the GMS8K dataset paths."""
        return [
            os.path.join(
                get_pset_inputs_dir(),
                ProblemType.GSM8K.value.upper(),
                GSM8KDataset.INPUT_FILE,
            )
        ]

    @property
    def generator(self) -> Generator[Tuple[str, Any], None, None]:
        """Concrete method to get a generator over the GMS8K problems."""
        problems = load_file_or_raise(self.input_paths[0])
        problems.index = [
            f"GSM8K/{int(index)}" for index in range(len(problems))
        ]

        #  Fields on the yielded problem are ['question', 'answer']
        yield from problems.iterrows()

    def get_formatted_prompt(self, problem: dict) -> str:
        question = problem.get("question")
        if not question:
            raise ValueError("No question found in problem.")
        return question