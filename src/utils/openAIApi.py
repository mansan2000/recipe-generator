import openai

def GPTGenerator(message):
    openai.api_key = ('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')
    # Emannuel's key ^^^
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': message}
        ],
        temperature=0
    )
    return(completion['choices'][0]['message']['content'])

#Selection: Path of what type of recipe user needs
#allergies: Concatenated string of food allergies
#flavor: Types of food we know the user likes

encase = "Each idea of recipies starting from the Title, then the ingredients, finished off with the instructions. " \
         "EACH TITLE MUST start and end with a $ e.x $Cookies$, $Beans$, etc.')"
wantidea = ", give me 3 ideas for something else I could make that is similar to what I wanted but without what I ran out of. "

haveidea = ". Based on this list of ingredients give me 3 ideas for something I could make with them. "
def recipeSelectionwant(wanted, ranout, allergies):
    return GPTGenerator("I wanted to make a " + wanted + "but I ran out of " + ranout + allergies + wantidea + encase)

def recipeSelectionhave(have, allergies):
    return GPTGenerator(have + haveidea + allergies + encase)

def get_recipe(recipe_text):
    recipes = {}
    recipe_parts = recipe_text.split('$')
    # Remove empty strings and trim spaces
    recipe_parts = [part.strip() for part in recipe_parts if part.strip()]

    # Iterate through recipe_parts in chunks of 2 (title, ingredients, instructions)
    for i in range(0, len(recipe_parts), 2):
        title = recipe_parts[i]
        ingredients_instructions = recipe_parts[i + 1].strip().split('\n')[1:]

        ingredients_instructions = "\n".join(ingredients_instructions)

        # Store the recipe as a dictionary entry
        recipes[title] = {
            "Ingredients": ingredients_instructions,
        }

    return recipes

# The way to call recipes
# recipe_data = recipeSelectionwant("cake", "eggs", "I am allergic to, nuts.")
# recipes = get_recipe(recipe_data)
# print(recipes.keys())
# print(recipes.values())
