
import pandas as pd
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from dotenv import load_dotenv

load_dotenv()


def read_excel(excel_name):
    df = pd.read_excel(excel_name, sheet_name="Sheet1")
    excel_data = []

    for row in df.itertuples(index=False):
        excel_data.append({
            "question": row.Questions,
            "answer": row.RAG_Answer,
        })

    return excel_data

def test_relevancy():
    excel_name = "RAG_evaluation.xlsx"
    excel_data = read_excel(excel_name)
    results = []

    metric = AnswerRelevancyMetric(threshold=0.7)
    test_cases = []

    for index, data in enumerate(excel_data, start=1):
        if pd.isna(data["question"]) or pd.isna(data["answer"]):
            continue

        test_case = LLMTestCase(
            input=str(data["question"]),
            actual_output=str(data["answer"]),
        )

        metric = AnswerRelevancyMetric(
            threshold=0.7,
            include_reason=True,
            async_mode=False,
        )

        try:
            metric.measure(test_case)

            score = metric.score
            reason = str(metric.reason).strip()
            passed = metric.success

            print(f"Error in test case {index}")
            print(f"Question: {data['question']}")
            print(f"Score: {score}")
            print(f"Reason: {reason}")
    
            if passed:
                passed_or_failed = 'Passed'
            else:
                passed_or_failed = 'Failed'
            print(f"Passed: {passed_or_failed}")

            results.append({
                "Question": data['question'],
                "Score": score,
                "Reason": reason,
                "Passed": passed_or_failed,
            })

        except Exception as e:
            print(f"Error in test case {index}: {e}")

            results.append({
                "Question": data['question'],
                "Score": None,
                "Reason": str(e),
                "Passed": None,
            })


    df = pd.read_excel(excel_name, sheet_name='Sheet1')
    for column in ["Deepeval_Score", "Deepeval_Reason"]:
            if column in df.columns:
                print(f"Column exists: {column}")
            else:
                df[column] = ''
    
    while len(results) != 0:
        for question in df['Questions']:
            if results[0]["Question"] == question:
                print(question)
                df.loc[df['Questions'] == question, "Deepeval_Score"] = results[0]["Passed"]
                df.loc[df['Questions'] == question, "Deepeval_Reason"] = results[0]["Reason"]
                df.to_excel(excel_name, sheet_name='Sheet1', index=False)

        results.pop(0)
        print(f"Updated Score for {question}")
    return


if __name__ == "__main__":
    test_relevancy()
