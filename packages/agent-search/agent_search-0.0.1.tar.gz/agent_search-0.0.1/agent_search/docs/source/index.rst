Welcome to AgentSearch [ΨΦ]
================

.. image:: https://github.com/emrgnt-cmplxty/sciphi/assets/68796651/195367d8-54fd-4281-ace0-87ea8523f982
   :width: 716
   :alt: AgentSearch Logo
   :align: center

.. raw:: html

   <p style="text-align:center">
   <strong>AI's Knowledge Engine.
   </strong>
   </p>

   <p style="text-align:center">
   <script async defer src="https://buttons.github.io/buttons.js"></script>
   <a class="github-button" href="https://github.com/AgentSearch-AI/sciphi" data-show-count="true" data-size="large" aria-label="Star">Star</a>
   <a class="github-button" href="https://github.com/AgentSearch-AI/sciphi/subscription" data-icon="octicon-eye" data-size="large" aria-label="Watch">Watch</a>
   <a class="github-button" href="https://github.com/AgentSearch-AI/sciphi/fork" data-icon="octicon-repo-forked" data-size="large" aria-label="Fork">Fork</a>
   </p>



AgentSearch [ΨΦ]: A Comprehensive Agent-First Framework and Dataset for Webscale Search
----------------------------------------------------------------------------------------

AgentSearch is a powerful new tool that allows you to operate a webscale search engine locally, catering to both Large Language Models (LLMs) and human users. This open-source initiative provides access to over one billion high-quality embeddings sourced from a wide array of content, including selectively filtered Creative Commons data and the entirety of Arxiv, Wikipedia, and Project Gutenberg.

Features of AgentSearch
------------------------

- **Gated Access**: Controlled and secure access to the search engine, ensuring data integrity and privacy.
- **Offline Support**: Ability to operate in a fully offline environment.
- **Customizable**: Upload your own local data or tailor the provided datasets according to your needs.
- **API Endpoint**: Fully managed access through a dedicated API, facilitating easy and efficient integration into various workflows.
Quickstart Guide for AgentSearch
--------------------------------

### Prerequisites

- Docker installed on your system.

### Quick Setup

1. Clone and install the AgentSearch client:

   .. code-block:: shell

      git clone https://github.com/SciPhi-AI/agent-search.git && cd agent-search
      pip install -e .

### Running a Query

- Execute a query with:

  .. code-block:: shell

     python agent_search/script/run_query.py query --query="What is Fermat's last theorem?"

Local Setup and Initialization
-------------------------------

1. **Database Population**:

   .. code-block:: shell

      python agent_search/script/populate_dbs.py populate_sqlite

2. **Start Qdrant Service with Docker**:

   .. code-block:: shell

      docker run -p 6333:6333 -p 6334:6334 \
          -v $(pwd)/qdrant_storage:/qdrant/storage:z \
          qdrant/qdrant

3. **Run the Server**:

   .. code-block:: shell

      python agent_search/app/server.py

Citing Our Work
---------------

.. code-block:: none

   @software{AgentSearch,
      author = {Colegrove, Owen},
      doi = {Pending},
      month = {09},
      title = {{AgentSearch: An agent-first search engine.}},
      url = {https://github.com/sciphi-ai/agent-search},
      year = {2023}
   }

Documentation
-------------

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   setup/installation
   setup/quickstart

.. toctree::
   :maxdepth: 1
   :caption: API

   api/main
