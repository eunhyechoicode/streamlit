from langsmith import Client
import openai
from langsmith import traceable
from langsmith.wrappers import wrap_openai
import os
import importlib.util
from typing import Dict, List, Any

from dotenv import load_dotenv
from index import list_board_game_indices
from config import load_config
from llm_service_config import get_llm_model, get_judge_llm
from rag import get_retriever
from langsmith.evaluation import evaluate
from langchain import hub

load_dotenv()


def load_dataset_from_file(file_path: str) -> Dict[str, List[Any]]:
    """Load dataset variables from a Python file."""
    spec = importlib.util.spec_from_file_location("dataset_module", file_path)
    if not spec or not spec.loader:
        raise ImportError(f"Could not load file: {file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return {
        'inputs': getattr(module, 'inputs', []),
        'outputs': getattr(module, 'outputs', []),
        'metadata': getattr(module, 'metadata', [])
    }


def create_evaluation_datasets():
    client = Client()
    config = load_config()
    base_directory = config['paths']['board_games_dir']

    # Get all board game directories
    game_folders = list_board_game_indices()

    for game_folder in game_folders:
        dataset_file = os.path.join(base_directory, game_folder, "dataset.py")

        # Skip if dataset file doesn't exist
        if not os.path.exists(dataset_file):
            print(f"No dataset.py file found for {game_folder}")
            continue

        try:
            # Load dataset from file
            dataset_content = load_dataset_from_file(dataset_file)

            # Create dataset in LangSmith
            dataset_name = game_folder
            dataset = client.create_dataset(dataset_name)

            # Create examples
            client.create_examples(
                inputs=dataset_content['inputs'],
                outputs=dataset_content['outputs'],
                metadata=dataset_content['metadata'],
                dataset_id=dataset.id
            )

            print(f"Successfully created evaluation dataset for {game_folder}")

        except Exception as e:
            print(f"Error processing dataset for {game_folder}: {e}")

class RagBot:
    def __init__(self):
        self._retriever = get_retriever()
        self._client = wrap_openai(openai.Client())
        self._model = get_llm_model()

    @traceable()
    def retrieve_docs(self, question):
        return self._retriever.invoke(question)

    @traceable()
    def invoke_llm(self, question, docs):
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a Board Game Master."
                               "Please answer questions using the game rules below.\n\n"
                               f"## Game Rules\n\n{docs}",
                },
                {"role": "user", "content": question},
            ],
        )

        return {
            "answer": response.choices[0].message.content,
            "contexts": [str(doc) for doc in docs],
        }

    @traceable()
    def get_answer(self, question: str):
        docs = self.retrieve_docs(question)
        return self.invoke_llm(question, docs)
rag_bot = RagBot()


def predict_rag_answer(example: dict):
    """Used when evaluating only the answer"""
    response = rag_bot.get_answer(example["input_question"])
    return {"answer": response["answer"]}

def predict_rag_answer_with_context(example: dict):
    """Used when evaluating hallucination using context"""
    response = rag_bot.get_answer(example["input_question"])
    return {"answer": response["answer"], "contexts": response["contexts"]}

# Grade prompt
# Prompt used to measure answer accuracy

grade_prompt_answer_accuracy = prompt = hub.pull("langchain-ai/rag-answer-vs-reference")

def answer_evaluator(run, example) -> dict:
    """
    Evaluator for measuring RAG answer performance
    """

    # `example` is the Question-Answer pair from dataset creation. `run` is the LLM answer generated using RagBot
    input_question = example.inputs["input_question"]
    reference = example.outputs["output_answer"]
    prediction = run.outputs["answer"]

    # LLM to be used as Judge
    judge = get_judge_llm()

    # Using LCEL for LLM response
    answer_grader = grade_prompt_answer_accuracy | judge

    # Execute Evaluator
    score = answer_grader.invoke({"question": input_question,
                                  "correct_answer": reference,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_v_reference_score", "score": score}

# Grade prompt
# Prompt used to determine how helpful the answer is to the user's question
grade_prompt_answer_helpfulness = prompt = hub.pull("langchain-ai/rag-answer-helpfulness")

def answer_helpfulness_evaluator(run, example) -> dict:
    """
    Evaluator to determine how helpful the answer is to the user's question
    """

    # Evaluates the value of LLM's answer to the dataset question without comparing to dataset answer
    input_question = example.inputs["input_question"]
    prediction = run.outputs["answer"]

    # LLM to be used as Judge
    judge = get_judge_llm()

    # Using LCEL for LLM response
    answer_grader = grade_prompt_answer_helpfulness | judge

    # Execute Evaluator
    score = answer_grader.invoke({"question": input_question,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_helpfulness_score", "score": score}

# Prompt
# Prompt for determining hallucination
grade_prompt_hallucinations = prompt = hub.pull("langchain-ai/rag-answer-hallucination")

def answer_hallucination_evaluator(run, example) -> dict:
    """
    Evaluator for determining hallucination
    """

    # Uses the question from dataset and context used by LLM when generating the answer
    input_question = example.inputs["input_question"]
    contexts = run.outputs["contexts"]

    # LLM's answer
    prediction = run.outputs["answer"]

    # LLM to be used as Judge
    judge = get_judge_llm()

    # Using LCEL for LLM response
    answer_grader = grade_prompt_hallucinations | judge

    # Execute Evaluator
    score = answer_grader.invoke({"documents": contexts,
                                  "student_answer": prediction})
    score = score["Score"]

    return {"key": "answer_hallucination", "score": score}


def run_evaluation():
    """
    Runs evaluation for each board game dataset.
    """
    # Get all available board game datasets
    game_datasets = list_board_game_indices()
    llm_model = get_llm_model()

    if not game_datasets:
        raise ValueError("No board game datasets found")

    for dataset_name in game_datasets:
        print(f"Evaluating dataset: {dataset_name}")
        experiment_results = evaluate(
            predict_rag_answer_with_context,
            data=dataset_name,
            evaluators=[
                answer_evaluator,
                answer_helpfulness_evaluator,
                answer_hallucination_evaluator
            ],
            experiment_prefix=f"{dataset_name}-evaluator-hallucination",
            metadata={"version": f"{dataset_name} v1, {llm_model}"},
        )
        print(f"Completed evaluation for {dataset_name}")

# create_evaluation_datasets()
# run_evaluation()