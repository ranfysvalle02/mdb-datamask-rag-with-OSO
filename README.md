# mdb-datamask-rag-with-OSO

## Unleashing Insights While Protecting Privacy: A Look at Privacy-Focused RAG

Imagine AI models that can understand your questions and generate informative responses by tapping into vast stores of knowledge. That's the power of RAG. However, with great power comes great responsibility, especially when handling sensitive data. This is where **privacy-focused RAG** comes in.

**Retrieval-Augmented Generation (RAG)**, while powerful, poses unique privacy challenges. Here's a deeper look into the strategies to mitigate these risks:

### Data Anonymization: A Closer Look

* **Generalization:** Replace specific values with broader categories. For example, instead of "New York City," use "Urban area."
* **Permutation:** Shuffle data elements to obscure relationships. For instance, rearrange the order of attributes in a dataset.
* **Differential Privacy:** Add random noise to data to hide individual contributions.

**Example:** A chatbot can answer user questions about medical conditions while protecting the privacy of both the user and the underlying data.

## Conditional Masking for GenAI Systems

**OSO Cloud** is a powerful authorization platform that can significantly enhance the security and privacy of your generative AI (GenAI) systems. By integrating OSO Cloud into your GenAI pipeline, you can dynamically determine whether to apply masking techniques based on the authorization status of the user or process.

Here's how OSO Cloud can help you implement conditional masking:

1. **Define Policies:** Create policies that specify which users or roles are authorized to access unmasked data. For example, you might define a policy that allows data scientists to access unmasked data for research purposes, while limiting access to production data to authorized personnel.
2. **Enforce Policies:** OSO Cloud enforces these policies at runtime, ensuring that only authorized users can access unmasked data.
3. **Conditional Masking:** Based on the authorization status returned by OSO Cloud, your GenAI pipeline can decide whether to apply masking techniques. If the user is authorized to access unmasked data, the pipeline can proceed without masking. If the user is not authorized, the pipeline can apply appropriate masking techniques to protect sensitive information.

### The Importance of Conditional Masking

Conditional masking offers several benefits:

* **Enhanced Privacy:** By masking sensitive data only when necessary, you can minimize the exposure of private information while still providing valuable insights.
* **Improved Efficiency:** When masking is not required, you can avoid the computational overhead associated with the masking process, improving the performance of your GenAI system.
* **Compliance:** Conditional masking can help you comply with data privacy regulations like GDPR and HIPAA by ensuring that sensitive data is only accessible to authorized individuals.

## Data Masking Example with Atlas Sample Dataset

**Important Notes:**

* Ensure proper access controls (RBAC) are implemented to restrict access to sensitive data.

This example provides a basic understanding of data masking using MongoDB's aggregation pipeline. You can customize it further to meet your specific data security needs. 

## Protecting Privacy: Unveiling the Power of Aggregation Framework for Data Masking

Have you ever found yourself needing to analyze data that contains sensitive information? You might be a movie reviewer analyzing comments on "The Godfather", but sharing user emails could be a privacy nightmare. This is where data masking comes in, and the good news? You don't need fancy code –  MongoDB's Aggregation Framework offers a powerful solution!

**What is Data Masking?**

Data masking is the art of obfuscating sensitive data while preserving its usability for analysis.  Imagine replacing a user's name with initials or their email with "[email address removed]". This allows you to understand trends and patterns without compromising privacy.  

[Learn More Here
](https://www.practical-mongodb-aggregations.com/examples/securing-data/mask-sensitive-fields.html)

**The Aggregation Framework: Your Masking Superhero**

The Aggregation Framework in MongoDB is a superhero when it comes to data manipulation.  It lets you perform various operations on data sets, including masking. Let's see how it works in our "Godfather" comment analysis case:

1. **Joining the Dots:** We start by joining the "comments" and "movies" collections. This allows us to filter comments on "The Godfather" specifically.
2. **Projecting What Matters:** Using the `$project` operator, we select the desired fields for analysis – date, name (initially masked), text, movie ID, movie title, and a masked email address.
3. **Masking Names and Emails:** Here's the magic! 
    - For names, we use `$substr` to grab the first character and concatenate it with "****" to hide the rest.
    - Emails get a similar treatment. We extract the first character, add "****@" and then use `$split` and `$arrayElemAt` to get the domain name (e.g., gmail.com) without revealing the full address. 
4. **Filtering for The Godfather:**  Finally, we use `$match` to filter for comments related to "The Godfather".

**Unveiling the Masked Data:**

Now, with our masked data set, we can feed it to a separate tool (like OpenAI's GPT-4) to generate a detailed report on the comments, focusing on content and sentiment without revealing private information.

**Benefits of Using the Aggregation Framework:**

- **Flexibility:** You can choose which fields to mask and the masking method (e.g., initials, redaction, etc.).
- **Efficiency:** It operates directly on your data set, avoiding complex code or data exports.
- **Security:**  Original data remains untouched, protecting sensitive information.

### Prerequisites

* **MongoDB Tools:**
  * **mongosh:** The official MongoDB shell for interacting with MongoDB databases.
  * **mongorestore:** A tool for restoring data from a dump file to a MongoDB database.
* **Docker:** Installed on your system ([https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/))
* **wget or curl:** Installed on your system (package managers usually handle this)


### Setting Up a Local Atlas Environment

1. **Pull the Docker Image:**

   * **Latest Version:**
     ```bash
     docker pull mongodb/mongodb-atlas-local
     ```

2. **Run the Database:**

   ```bash
   docker run -p 27017:27017 mongodb/mongodb-atlas-local
   ```
   This command runs the Docker image, exposing port 27017 on your machine for connecting to the database.

### Using Sample Datasets with MongoDB

This section demonstrates downloading and exploring a sample dataset for MongoDB on your local system.

#### Downloading the Dataset

There's a complete sample dataset available for MongoDB. Download it using either `wget` or `curl`:

* **Using wget:**

```bash
wget https://atlas-education.s3.amazonaws.com/sampledata.archive
```

* **Using curl:**

```bash
curl https://atlas-education.s3.amazonaws.com/sampledata.archive -o sampledata.archive
```

**Note:**

* Ensure you have `wget` or `curl` installed.
* The downloaded file will be named `sampledata.archive`.

#### Restoring the Dataset

Before restoring, ensure you have a local `mongod` instance running (either existing or newly started). This instance will host the dataset.

**To restore the dataset:**

```bash
mongorestore --archive=sampledata.archive
```

This command uses the `mongorestore` tool to unpack the downloaded archive (`sampledata.archive`) and populate your local `mongod` instance with the sample data.

#### Run the Script:

* From your terminal, run ```python3 demo.py```

**Full Code:**
```python
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
    
"""
The context provided contains a list of comments about the movie "The Godfather" from various users. The comments span from the year 1970 to 2017. The users have used pseudonyms and their emails have been partially hidden for privacy reasons. 

The comments are generally vague and do not provide specific feedback about the movie. They seem to be randomly generated text and do not provide any meaningful insights about the movie. The comments do not mention any specific characters, scenes, or aspects of the movie. 

The users who have commented multiple times include 'M****', 'J****', 'D****', 'G****', 'P****', 'T****', 'S****', 'K****', 'L****', 'R****', 'C****', 'B****', 'E****', 'I****', 'V****', 'Y****', 'A****', and 'O****'. 

The comments are not time-bound to the release of the movie, as they span over several decades. This could suggest that the movie has a lasting impact and continues to be discussed years after its release. However, without specific content in the comments related to the movie, it is hard to draw any concrete conclusions. 

In conclusion, while the data shows that "The Godfather" continues to generate discussion, the lack of specific content in the comments makes it difficult to understand the viewers' opinions about the movie.
"""

```

**Conclusion:**

The Aggregation Framework empowers you to analyze sensitive data responsibly. By leveraging its capabilities, you can unlock valuable insights while safeguarding privacy.  So, next time you need to analyze data with a privacy twist, remember – the Aggregation Framework is your data masking hero!
