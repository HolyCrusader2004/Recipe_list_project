import requests

query = 'Salmon'
api_url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={query}'
response = requests.get(api_url)
picture_if_not_found = ''

if response.status_code == 200:
    recipes_data = response.json()

    if recipes_data and 'meals' in recipes_data and recipes_data['meals']:
        first_recipe = recipes_data['meals'][0]
        picture = first_recipe.get('strMealThumb')
        if picture is not None:
            print("Picture:", picture)
        else:
            image_path = r'https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png'
            print("Picture:", image_path)
    else:
        print("No recipe found.")
        image_path = r'https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png'
        print("Picture:", image_path)
else:
    print("Error:", response.status_code, response.text)
