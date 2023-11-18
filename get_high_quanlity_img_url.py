import facebook

def get_high_quanity_img(post_id):
    # Declare Facebook application information
    access_token = 'EAABwzLixnjYBO4k5DLrD5Ct5ZBCnqqaW2PW3xn5ySrY0wxFfsmkjZAjuaCRbKlpB5WpnqMW593SYzrC3NLW7sR3kztwVOzO3Y8KF8AZBWeOON3ZAUZCMFW1OnJLHHBpGptsupVgORB9LJHFZAdX80rjvj0isPZA1G3LLBUAM7zgvJp7aao5QnemQgZCdZBjt6z5RRavJ48XyDPDIZD'

    # Create a Facebook Graph API object
    graph = facebook.GraphAPI(access_token=access_token)

    # Add the 'images' field to retrieve information about image paths
    fields = 'images'
    post = graph.get_object(post_id, fields=fields)

    # Check if the 'images' field exists
    if 'images' in post:
        # Get the path to the high-quality image (usually the first image in the images list)
        high_quality_image_url = post['images'][0]['source']
        return high_quality_image_url
    else:
        return None
