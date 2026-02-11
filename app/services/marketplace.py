def generate_market_links(recipe):
    base_url = "https://www.amazon.in/s?k="

    links = []
    # Only generate links if ingredients exist
    if recipe and recipe.ingredients:
        for ing in recipe.ingredients:
            # Basic cleanup for search query
            q = ing.name.replace(" ", "+")
            links.append({
                "ingredient": ing.name,
                "url": base_url + q
            })

    return links
