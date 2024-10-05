import pymongo, openai
from oso_cloud import Oso

api_key = "<api-key-goes-here>"
oso = Oso(url="https://cloud.osohq.com", api_key=api_key)
actor = {"type": "User", "id": "1233"}
resource = {"type": "Repository", "id": "456"}

def test_oso():
  if not oso.authorize(actor, "view", resource):
    # Handle authorization failure
    return "unauthorized by oso"
  return "authorized by oso"

AZURE_OPENAI_ENDPOINT = "https://.openai.azure.com"
AZURE_OPENAI_API_KEY = "" 
deployment_name = "gpt-4-32k"  # The name of your model deployment
az_client = openai.AzureOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,api_version="2023-03-15-preview",api_key=AZURE_OPENAI_API_KEY)
USER_ROLE='user' # user or admin
mdb_client = pymongo.MongoClient('mongodb://localhost:27017?directConnection=true')
db = mdb_client['sample_mflix']
pipeline = []
if test_oso() != "authorized by oso":    
    pipeline = [
        {
            '$lookup': {
                'from': 'movies', 
                'localField': 'movie_id', 
                'foreignField': '_id', 
                'as': 'movie_info'
            }
        }, {
            '$project': {
                'movie_title': {
                    '$arrayElemAt': [
                        '$movie_info.title', 0
                    ]
                }, 
                'name': 1, 
                'date': 1, 
                'text': 1, 
                'email': 1
            }
        },
        {"$match": {"movie_title": {"$eq": "The Godfather"}}},
        {
            '$project': {
                'date': 1, 
                'name': {
                    '$concat': [
                        {
                            '$substr': [
                                '$name', 0, 1
                            ]
                        }, '****'
                    ]
                }, 
                'text': 1, 
                'movie_id': 1, 
                'movie_title': 1,
                'email': {
                    '$concat': [
                        {
                            '$substr': [
                                '$email', 0, 1
                            ]
                        }, '****@', {
                            '$arrayElemAt': [
                                {
                                    '$split': [
                                        '$email', '@'
                                    ]
                                }, 1
                            ]
                        }
                    ]
                }
            }
        }
    ]
elif test_oso() == "authorized by oso":
    pipeline = [
        {
            '$lookup': {
                'from': 'movies', 
                'localField': 'movie_id', 
                'foreignField': '_id', 
                'as': 'movie_info'
            }
        }, {
            '$project': {
                'movie_title': {
                    '$arrayElemAt': [
                        '$movie_info.title', 0
                    ]
                }, 
                'name': 1, 
                'date': 1, 
                'text': 1, 
                'email': 1
            }
        },
        {"$match": {"movie_title": {"$eq": "The Godfather"}}},
        {
            '$project': {
                'date': 1, 
                'name': 1, 
                'text': 1, 
                'movie_id': 1, 
                'movie_title': 1,
                'email': 1
            }
        }
    ]
result = list(db.comments.aggregate(pipeline))
for doc in result:
    print(doc)
response = az_client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "user", "content": f"""
            [context]
            {str(result)}
            [end context]

            [task]
                Use the provided context to create a detailed report on the comments.
            [end task]
"""},
    ],
    temperature=0,
)
print(response.choices[0].message.content)
    
