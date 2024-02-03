import requests

query = 'Salmon'
api_url = 'https://api.api-ninjas.com/v1/recipe?query={}'.format(query)
headers = {'X-Api-Key': 'zGKQ2YkpGrjgPf2P/1jrEw==pZaNKj9JEPhitfdg'}
response = requests.get(api_url, headers=headers)

if response.status_code == 200:
    recipes_data = response.json()

    if recipes_data and isinstance(recipes_data, list):
        first_recipe = recipes_data[0]
        instructions = first_recipe.get('instructions')
        if instructions is not None:
            print("Instructions:", instructions)
        else:
            print("Instructions:No instructions")
    else:
        print("No recipe found.")
else:
    print("Error:", response.status_code, response.text)
