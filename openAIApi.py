import openai
def get_recipe(instructions):
    openai.api_key = ("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")
    model_engine = "text-davinci-003" # text-curie-001, text-davinci-003
    prompt = instructions
    # print(openai.Model.list())

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5
    )
    response = completion.choices[0].text
    # response = completion

    return response

    # print(response)