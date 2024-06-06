from .shared import shared_responses


# Users related API router responses
get_profile_responses = {401: shared_responses[401]}

update_password_responses = {
    400: {
        "description": "Bad Request Error",
        "content": {
            "application/json": {
                "example": {
                    "message": "Please check your credentials and try again."
                }
            }
        },
    },
    401: shared_responses[401],
    404: shared_responses[404],
}

update_profile_responses = {401: shared_responses[401]}


# API Keys related API router responses
get_api_keys_responses = {401: shared_responses[401]}

update_api_keys_responses = {401: shared_responses[401]}

# AI models related API router responses
get_ai_models_responses = {401: shared_responses[401]}
