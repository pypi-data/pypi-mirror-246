# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swarms',
 'swarms.agents',
 'swarms.cli',
 'swarms.memory',
 'swarms.models',
 'swarms.prompts',
 'swarms.structs',
 'swarms.swarms',
 'swarms.tools',
 'swarms.utils',
 'swarms.workers']

package_data = \
{'': ['*']}

install_requires = \
['Pillow',
 'PyPDF2',
 'accelerate',
 'asyncio',
 'attrs',
 'backoff',
 'beautifulsoup4',
 'black',
 'chromadb',
 'cohere',
 'datasets',
 'diffusers',
 'einops',
 'faiss-cpu',
 'ggl',
 'google-generativeai',
 'httpx',
 'huggingface-hub',
 'langchain',
 'langchain-experimental',
 'marshmallow',
 'open_clip_torch',
 'openai==0.28.0',
 'opencv-python-headless',
 'optimum==1.15.0',
 'playwright',
 'pydantic==1.10.12',
 'ratelimit',
 'rich',
 'safetensors',
 'sentencepiece',
 'soundfile',
 'tabulate',
 'tenacity',
 'tensorflow==2.15.0',
 'termcolor',
 'tiktoken',
 'torch==2.1.1',
 'torchvision',
 'transformers==2.10',
 'vllm',
 'weaviate-client',
 'wget']

setup_kwargs = {
    'name': 'swarms',
    'version': '2.7.8',
    'description': 'Swarms - Pytorch',
    'long_description': '![Swarming banner icon](images/swarmslogobanner.png)\n\n<div align="center">\n\nSwarms is a modular framework that enables reliable and useful multi-agent collaboration at scale to automate real-world tasks.\n\n\n[![GitHub issues](https://img.shields.io/github/issues/kyegomez/swarms)](https://github.com/kyegomez/swarms/issues) [![GitHub forks](https://img.shields.io/github/forks/kyegomez/swarms)](https://github.com/kyegomez/swarms/network) [![GitHub stars](https://img.shields.io/github/stars/kyegomez/swarms)](https://github.com/kyegomez/swarms/stargazers) [![GitHub license](https://img.shields.io/github/license/kyegomez/swarms)](https://github.com/kyegomez/swarms/blob/main/LICENSE)[![GitHub star chart](https://img.shields.io/github/stars/kyegomez/swarms?style=social)](https://star-history.com/#kyegomez/swarms)[![Dependency Status](https://img.shields.io/librariesio/github/kyegomez/swarms)](https://libraries.io/github/kyegomez/swarms) [![Downloads](https://static.pepy.tech/badge/swarms/month)](https://pepy.tech/project/swarms)\n\n[![Join the Agora discord](https://img.shields.io/discord/1110910277110743103?label=Discord&logo=discord&logoColor=white&style=plastic&color=d7b023)![Share on Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Share%20%40kyegomez/swarms)](https://twitter.com/intent/tweet?text=Check%20out%20this%20amazing%20AI%20project:%20&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms) [![Share on Facebook](https://img.shields.io/badge/Share-%20facebook-blue)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms) [![Share on LinkedIn](https://img.shields.io/badge/Share-%20linkedin-blue)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&title=&summary=&source=)\n\n[![Share on Reddit](https://img.shields.io/badge/-Share%20on%20Reddit-orange)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&title=Swarms%20-%20the%20future%20of%20AI) [![Share on Hacker News](https://img.shields.io/badge/-Share%20on%20Hacker%20News-orange)](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&t=Swarms%20-%20the%20future%20of%20AI) [![Share on Pinterest](https://img.shields.io/badge/-Share%20on%20Pinterest-red)](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms&media=https%3A%2F%2Fexample.com%2Fimage.jpg&description=Swarms%20-%20the%20future%20of%20AI) [![Share on WhatsApp](https://img.shields.io/badge/-Share%20on%20WhatsApp-green)](https://api.whatsapp.com/send?text=Check%20out%20Swarms%20-%20the%20future%20of%20AI%20%23swarms%20%23AI%0A%0Ahttps%3A%2F%2Fgithub.com%2Fkyegomez%2Fswarms)\n\n</div>\n\n\n----\n\n## Installation\n`pip3 install --upgrade swarms`\n\n---\n\n## Usage\n\nRun example in Collab: <a target="_blank" href="https://colab.research.google.com/github/kyegomez/swarms/blob/master/playground/swarms_example.ipynb">\n<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>\n</a>\n\n### `Agent` Example\n- Reliable Structure that provides LLMS autonomy\n- Extremely Customizeable with stopping conditions, interactivity, dynamical temperature, loop intervals, and so much more\n- Enterprise Grade + Production Grade: `Agent` is designed and optimized for automating real-world tasks at scale!\n\n```python\nimport os\n\nfrom dotenv import load_dotenv\n\n# Import the OpenAIChat model and the Agent struct\nfrom swarms.models import OpenAIChat\nfrom swarms.structs import Agent\n\n# Load the environment variables\nload_dotenv()\n\n# Get the API key from the environment\napi_key = os.environ.get("OPENAI_API_KEY")\n\n# Initialize the language model\nllm = OpenAIChat(\n    temperature=0.5,\n    model_name="gpt-4",\n    openai_api_key=api_key,\n    max_tokens=4000\n)\n\n\n## Initialize the workflow\nagent = Agent(llm=llm, max_loops=1, autosave=True, dashboard=True)\n\n# Run the workflow on a task\nout = agent.run("Generate a 10,000 word blog on health and wellness.")\nprint(out)\n\n\n```\n\n------\n\n### `SequentialWorkflow`\n- A Sequential swarm of autonomous agents where each agent\'s outputs are fed into the next agent\n- Save and Restore Workflow states!\n- Integrate Agent\'s with various LLMs and Multi-Modality Models\n\n```python\nimport os \nfrom swarms.models import OpenAIChat\nfrom swarms.structs import Agent\nfrom swarms.structs.sequential_workflow import SequentialWorkflow\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\n# Load the environment variables\napi_key = os.getenv("OPENAI_API_KEY")\n\n\n# Initialize the language agent\nllm = OpenAIChat(\n    temperature=0.5,\n    model_name="gpt-4",\n    openai_api_key=api_key,\n    max_tokens=4000\n)\n\n\n# Initialize the agent with the language agent\nagent1 = Agent(llm=llm, max_loops=1)\n\n# Create another agent for a different task\nagent2 = Agent(llm=llm, max_loops=1)\n\n# Create another agent for a different task\nagent3 = Agent(llm=llm, max_loops=1)\n\n# Create the workflow\nworkflow = SequentialWorkflow(max_loops=1)\n\n# Add tasks to the workflow\nworkflow.add(\n    agent1, "Generate a 10,000 word blog on health and wellness.", \n)\n\n# Suppose the next task takes the output of the first task as input\nworkflow.add(\n    agent2, "Summarize the generated blog",\n)\n\n# Run the workflow\nworkflow.run()\n\n# Output the results\nfor task in workflow.tasks:\n    print(f"Task: {task.description}, Result: {task.result}")\n\n\n```\n\n## `Multi Modal Autonomous Agents`\n- Run the agent with multiple modalities useful for various real-world tasks in manufacturing, logistics, and health.\n\n```python\n# Description: This is an example of how to use the Agent class to run a multi-modal workflow\nimport os\nfrom dotenv import load_dotenv\nfrom swarms.models.gpt4_vision_api import GPT4VisionAPI\nfrom swarms.structs import Agent\n\n# Load the environment variables\nload_dotenv()\n\n# Get the API key from the environment\napi_key = os.environ.get("OPENAI_API_KEY")\n\n# Initialize the language model\nllm = GPT4VisionAPI(\n    openai_api_key=api_key,\n    max_tokens=500,\n)\n\n# Initialize the task\ntask = (\n    "Analyze this image of an assembly line and identify any issues such as"\n    " misaligned parts, defects, or deviations from the standard assembly"\n    " process. IF there is anything unsafe in the image, explain why it is"\n    " unsafe and how it could be improved."\n)\nimg = "assembly_line.jpg"\n\n## Initialize the workflow\nagent = Agent(\n    llm=llm,\n    max_loops="auto",\n    autosave=True,\n    dashboard=True,\n    multi_modal=True\n)\n\n# Run the workflow on a task\nout = agent.run(task=task, img=img)\nprint(out)\n\n\n```\n\n\n### `OmniModalAgent`\n- An agent that can understand any modality and conditionally generate any modality.\n\n```python\nfrom swarms.agents.omni_modal_agent import OmniModalAgent, OpenAIChat\nfrom swarms.models import OpenAIChat\nfrom dotenv import load_dotenv\nimport os\n\n# Load the environment variables\nload_dotenv()\n\n# Get the API key from the environment\napi_key = os.environ.get("OPENAI_API_KEY")\n\n# Initialize the language model\nllm = OpenAIChat(\n    temperature=0.5,\n    model_name="gpt-4",\n    openai_api_key=api_key,\n)\n\n\nagent = OmniModalAgent(llm)\nresponse = agent.run("Generate a video of a swarm of fish and then make an image out of the video")\nprint(response)\n```\n\n\n---\n\n# Features 🤖 \nThe Swarms framework is designed with a strong emphasis on reliability, performance, and production-grade readiness. \nBelow are the key features that make Swarms an ideal choice for enterprise-level AI deployments.\n\n## 🚀 Production-Grade Readiness\n- **Scalable Architecture**: Built to scale effortlessly with your growing business needs.\n- **Enterprise-Level Security**: Incorporates top-notch security features to safeguard your data and operations.\n- **Containerization and Microservices**: Easily deployable in containerized environments, supporting microservices architecture.\n\n## ⚙️ Reliability and Robustness\n- **Fault Tolerance**: Designed to handle failures gracefully, ensuring uninterrupted operations.\n- **Consistent Performance**: Maintains high performance even under heavy loads or complex computational demands.\n- **Automated Backup and Recovery**: Features automatic backup and recovery processes, reducing the risk of data loss.\n\n## 💡 Advanced AI Capabilities\n\nThe Swarms framework is equipped with a suite of advanced AI capabilities designed to cater to a wide range of applications and scenarios, ensuring versatility and cutting-edge performance.\n\n### Multi-Modal Autonomous Agents\n- **Versatile Model Support**: Seamlessly works with various AI models, including NLP, computer vision, and more, for comprehensive multi-modal capabilities.\n- **Context-Aware Processing**: Employs context-aware processing techniques to ensure relevant and accurate responses from agents.\n\n### Function Calling Models for API Execution\n- **Automated API Interactions**: Function calling models that can autonomously execute API calls, enabling seamless integration with external services and data sources.\n- **Dynamic Response Handling**: Capable of processing and adapting to responses from APIs for real-time decision making.\n\n### Varied Architectures of Swarms\n- **Flexible Configuration**: Supports multiple swarm architectures, from centralized to decentralized, for diverse application needs.\n- **Customizable Agent Roles**: Allows customization of agent roles and behaviors within the swarm to optimize performance and efficiency.\n\n### Generative Models\n- **Advanced Generative Capabilities**: Incorporates state-of-the-art generative models to create content, simulate scenarios, or predict outcomes.\n- **Creative Problem Solving**: Utilizes generative AI for innovative problem-solving approaches and idea generation.\n\n### Enhanced Decision-Making\n- **AI-Powered Decision Algorithms**: Employs advanced algorithms for swift and effective decision-making in complex scenarios.\n- **Risk Assessment and Management**: Capable of assessing risks and managing uncertain situations with AI-driven insights.\n\n### Real-Time Adaptation and Learning\n- **Continuous Learning**: Agents can continuously learn and adapt from new data, improving their performance and accuracy over time.\n- **Environment Adaptability**: Designed to adapt to different operational environments, enhancing robustness and reliability.\n\n\n## 🔄 Efficient Workflow Automation\n- **Streamlined Task Management**: Simplifies complex tasks with automated workflows, reducing manual intervention.\n- **Customizable Workflows**: Offers customizable workflow options to fit specific business needs and requirements.\n- **Real-Time Analytics and Reporting**: Provides real-time insights into agent performance and system health.\n\n## 🌐 Wide-Ranging Integration\n- **API-First Design**: Easily integrates with existing systems and third-party applications via robust APIs.\n- **Cloud Compatibility**: Fully compatible with major cloud platforms for flexible deployment options.\n- **Continuous Integration/Continuous Deployment (CI/CD)**: Supports CI/CD practices for seamless updates and deployment.\n\n## 📊 Performance Optimization\n- **Resource Management**: Efficiently manages computational resources for optimal performance.\n- **Load Balancing**: Automatically balances workloads to maintain system stability and responsiveness.\n- **Performance Monitoring Tools**: Includes comprehensive monitoring tools for tracking and optimizing performance.\n\n## 🛡️ Security and Compliance\n- **Data Encryption**: Implements end-to-end encryption for data at rest and in transit.\n- **Compliance Standards Adherence**: Adheres to major compliance standards ensuring legal and ethical usage.\n- **Regular Security Updates**: Regular updates to address emerging security threats and vulnerabilities.\n\n## 💬 Community and Support\n- **Extensive Documentation**: Detailed documentation for easy implementation and troubleshooting.\n- **Active Developer Community**: A vibrant community for sharing ideas, solutions, and best practices.\n- **Professional Support**: Access to professional support for enterprise-level assistance and guidance.\n\nSwarms framework is not just a tool but a robust, scalable, and secure partner in your AI journey, ready to tackle the challenges of modern AI applications in a business environment.\n\n\n## Documentation\n- For documentation, go here, [swarms.apac.ai](https://swarms.apac.ai)\n\n\n## 🫶 Contributions:\n\nSwarms is an open-source project, and contributions are welcome. If you want to contribute, you can create new features, fix bugs, or improve the infrastructure. Please refer to the [CONTRIBUTING.md](https://github.com/kyegomez/swarms/blob/master/CONTRIBUTING.md) and our [contributing board](https://github.com/users/kyegomez/projects/1) file in the repository for more information on how to contribute.\n\nTo see how to contribute, visit [Contribution guidelines](https://github.com/kyegomez/swarms/blob/master/CONTRIBUTING.md)\n\n<a href="https://github.com/kyegomez/swarms/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=kyegomez/swarms" />\n</a>\n\n\n## Community\n- [Join the Swarms community on Discord!](https://discord.gg/AJazBmhKnr)\n- Join our Swarms Community Gathering every Thursday at 1pm NYC Time to unlock the potential of autonomous agents in automating your daily tasks [Sign up here](https://lu.ma/5p2jnc2v)\n\n\n\n## Discovery Call\nBook a discovery call with the Swarms team to learn how to optimize and scale your swarm! [Click here to book a time that works for you!](https://calendly.com/swarm-corp/30min?month=2023-11)\n\n# License\nApache License\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/swarms',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
