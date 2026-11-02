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

    input_tokens = response["prompt_eval_count"]
    output_tokens = response["eval_count"]
    print(f"[tokens] input={input_tokens} output={output_tokens}")

    return response["message"]["content"]


if __name__ == "__main__":
    answer = ask_llm("What does the command df -h show? Answer in 3 lines.")
    print(answer)