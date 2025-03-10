# DatanetHybridRAG
A hybrid RAG design to combine vector db with DPML to provide better performance

# Setup
1. Start ollama: https://ollama.com/download
   - Download the latest version of Ollama.
   - Use Ollama to pull llms used for the project.
     - ollama pull nomic-embed-text
     - ollama run deepseek-r1:7b
   - Use docker start the Milvus vector db
     - https://milvus.io/docs/zh/install_standalone-docker.md
       - Start service
         - curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
         - Start milvus: standalone_embed.sh start
       - other operations
         - Stop milvus: bash standalone_embed.sh stop
         - Delete milvus: bash standalone_embed.sh delete
         - Upgrade milvus: bash standalone_embed.sh upgrade
2. Docker-compose up Datanet
   - docker compose up -d

