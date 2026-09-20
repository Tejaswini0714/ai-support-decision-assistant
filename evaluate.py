import json

from src.decision import make_decision
from src.retrieval import load_saved_knowledge_base, retrieve_relevant_chunks


with open("sample_test_cases.json", "r", encoding="utf-8") as file:
    test_cases = json.load(file)

knowledge_base = load_saved_knowledge_base()

correct = 0

for test_case in test_cases:
    message = test_case["message"]
    expected = test_case["expected_action"]

    chunks = retrieve_relevant_chunks(message, knowledge_base)
    decision = make_decision(message, chunks)

    actual = decision.action

    print(f"Test: {test_case['case_id']}")
    print(f"Expected: {expected}")
    print(f"Actual: {actual}")

    if actual == expected:
        correct += 1
        print("Result: PASS")
    else:
        print("Result: FAIL")

    print()

accuracy = correct / len(test_cases) * 100

print(f"Correct: {correct}/{len(test_cases)}")
print(f"Accuracy: {accuracy:.2f}%")