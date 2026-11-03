import ollama

MODEL = "llama3.2"


def ask_llm(question, system_prompt="You are a helpful Linux assistant.", temperature=0.1):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        options={"temperature": temperature},
    )
    print(f"[tokens] input={response['prompt_eval_count']} output={response['eval_count']}")
    return response["message"]["content"]


def ask_llm_json(question, schema, system_prompt="You are a helpful Linux assistant.", temperature=0):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        format=schema,
        options={"temperature": temperature},
    )
    print(f"[tokens] input={response['prompt_eval_count']} output={response['eval_count']}")
    return response["message"]["content"]


if __name__ == "__main__":
    answer = ask_llm("What does the command df -h show? Answer in 3 lines.")
    print(answer)