AgentSearch API Documentation
========================

Welcome to the AgentSearch API documentation. Here, you'll find a detailed guide on how to use the different endpoints provided by the AgentSearch service. This API allows you to interact with the powerful functionalities of the AgentSearch codebase and associated AI. AgentSearch looks to become a powerful tool for exploring the world's knowledge, and we hope you enjoy using it!

Endpoint Overview
-----------------

1. **Search**: This endpoint allows you to fetch related documents based on a set of queries. The documents are retrieved by re-ranked similarity search over embeddings produced by the `facebook/contriever <https://huggingface.co/facebook/contriever>`_. As of now, only Wikipedia is embedded, but there are plans to expand this to a more comprehensive corpus using state-of-the-art embedding methods.

2. **OpenAI Formatted LLM Request (v1)**: AgentSearch models are served via an API that is compatible with the OpenAI API.

Detailed Endpoint Descriptions
------------------------------

Search Endpoint
~~~~~~~~~~~~~~~

- **URL**: ``/search``
- **Method**: ``POST``
- **Description**: This endpoint interacts with the Retriever module of the AgentSearch-Infra codebase, allowing you to search for related documents based on the provided queries.

**Request Body**:
  - ``queries``: A list of query strings for which related documents should be retrieved.
  - ``top_k``: (Optional) The number of top related documents you wish to retrieve for each query.

**Response**: 
A list of lists containing Document objects, where each list corresponds to the related documents for a specific query.

**Example**:

.. code-block:: bash

   curl -X POST https://api.sciphi.ai/search \
        -H "Authorization: Bearer $SCIPHI_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"queries": ["What is general relativity?", "Who is Albert Einstein?"], "top_k": 5}'

**Response**:

.. code-block:: none

   [
     {
       "id":14678539,
       "title":"General Relativity and Gravitation",
       "text":"...a monthly peer-reviewed scientific journal published by Springer Science+Business Media. Editors-in-chief are Abhay Ashtekar and Roy Maartens..."
     },
     {
       "id":152075,
       "title":"General relativity",
       "text":"...a geometric theory of gravitation by Albert Einstein in 1915. It generalizes special relativity and Newton's law..."
     },
     {
       "id":434606,
       "title":"Universe",
       "text":"...General relativity provides a unified description of gravity affecting the geometry of spacetime..."
     },
     {
       "id":14246698,
       "title":"Albert Einstein: Creator and Rebel",
       "text":"...a biography of Albert Einstein by Banesh Hoffmann with Helen Dukas, published in 1972 by Viking Press..."
     },
     {
       "id":2060,
       "title":"Albert Einstein",
       "text":"...German-born physicist known for the theory of relativity and the mass–energy equivalence formula. He received the 1921 Nobel Prize in Physics..."
     }
   ]

AgentSearch v1 Endpoints
~~~~~~~~~~~~~~~~~~~

AgentSearch adheres to the API specification of OpenAI's API, allowing compatibility with any application designed for the OpenAI API. Below is an example curl command:

**Example**:

.. code-block:: bash

    curl https://api.sciphi.ai/v1/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $SCIPHI_API_KEY" \
      -d '{
         "model": "AgentSearch/AgentSearch-Self-RAG-Mistral-7B-32k",
         "prompt": "Say this is a test.",
         "temperature": 0.7
       }'

**Response**:

.. code-block:: json

    {
        "id":"cmpl-f03f53c15a174ffe89bdfc83507de7a9",
        "object":"text_completion",
        "created":1698730137,
        "model":"AgentSearch/AgentSearch-Self-RAG-Mistral-7B-32k",
        "choices":[
            {
                "index":0,
                "text":"This is a test.",
                "logprobs":null,
                "finish_reason":"length"
            }
        ],
        "usage": {
            "prompt_tokens":7,
            "total_tokens":15,
            "completion_tokens":8
        }
    }

API Key and Signup
------------------

To access the AgentSearch API, you need an API key. If you don't possess one, you can sign up `here <https://www.sciphi.ai/signup>`_. Ensure you include the API key in your request headers as shown in the examples.
