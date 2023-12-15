# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cached_notion', 'cached_notion.models']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=15.0.1,<16.0.0',
 'notion-client>=2.0.0,<3.0.0',
 'pydantic>=2.5.2,<3.0.0',
 'sqlitedict>=2.1.0,<3.0.0',
 'tenacity>=8.2.3,<9.0.0',
 'tqdm>=4.66.1,<5.0.0']

setup_kwargs = {
    'name': 'cached-notion',
    'version': '0.1.6',
    'description': '',
    'long_description': '# CachedNotion 🔧\n**CachedNotion** offers an enhanced, caching-enabled interface for interacting with Notion APIs. While it\'s a work in progress 🚧, its core functionality is fully operational, ensuring efficient and smooth integration.\n\n## What\'s New 🌟\n- **Critical Caching Issue Resolved:** We\'ve tackled a significant caching problem to ensure more reliable and faster access to your Notion data.\n- Stay tuned for ongoing updates and improvements! 💼\n\n## Installation 📦\n\n**CachedNotion** is currently available on TestPyPI. You can install it using either pip or Poetry.\n\n### Using pip\n\nTo install `CachedNotion` using pip, run the following command:\n\n```bash\npip install cached-notion\n```\n\n### Using Poetry\n\nFor those using Poetry, you can add `CachedNotion` to your project as follows:\n\n```bash\npoetry add cached-notion\n```\n\n---\n\n## New Feature: Notion to Markdown Conversion 📝\n\n**CachedNotion** now offers an innovative feature to convert Notion pages into Markdown format. This is invaluable for users wanting to document, backup, or share their Notion content in a standardized format.\n\n### Function Overview\n\n- `url_to_md`: Converts a Notion URL into a Markdown string. It handles nested content up to a specified depth, making it perfect for diverse documentation needs.\n- `id_to_md`: A complementary function to `url_to_md`, handling individual IDs and managing content depth.\n\n### Understanding Parameters\n\n- `max_depth`: This parameter in `url_to_md` specifies the recursive depth for crawling through the Notion content. A value of `-1` indicates no limit, ensuring a comprehensive conversion that includes all nested elements. Adjust this parameter to control how deep the function traverses through nested pages or blocks.\n- `subs`: Short for "sub-items," this parameter represents the remaining sub-items that are yet to be processed for further depths. It\'s crucial for managing and tracking the conversion process across nested levels of content.\n\n### Using `url_to_md`\n\nQuickly convert any Notion page into Markdown:\n```python\nfrom cached_notion.utils import url_to_md\n\n# Initialize CachedClient\nclient = CachedClient(auth=os.environ["NOTION_TOKEN"], cache_delta=24)\n\n# Convert a Notion URL to Markdown, specifying the depth of content to include\nnotion_url = "https://www.notion.so/xxx/xxx"\nmarkdown_string, remaining_subs = url_to_md(client, notion_url, max_depth=-1)\n\n# Markdown string is now ready, along with any remaining sub-items for further processing\nprint(markdown_string)\n```\n\nThis function is especially useful for thorough documentation, platform exports, or content backups.\n\n### Using `id_to_md`\n\n`id_to_md` can also be used independently for tailored Markdown generation processes, providing flexibility and control over the depth and content of the conversion.\n\n---\n## Basic Usage 📖\nEffortlessly replace `NotionClient` with `CachedClient` for an optimized experience:\n```python\nfrom cached_notion.cached_client import CachedClient\nfrom cached_notion.utils import normalize_url, get_id_with_object_type\nimport os\n\n# Initialize CachedClient with your Notion token and desired cache settings\nclient = CachedClient(auth=os.environ["NOTION_TOKEN"], cache_delta=24)\nurl = "https://www.notion.so/xxx/xxx"\nnormalized_url = normalize_url(url)\nnid, object_type = get_id_with_object_type(normalized_url)\n\n# Use CachedClient to interact with Notion by providing the Notion ID\npage = client.pages.retrieve(nid)\ndatabase = client.databases.retrieve(nid)\nblock = client.blocks.retrieve(nid)\n```\n\n## Utility Functions 🛠️\nMaximize your productivity with these handy functions:\n```python\nfrom cached_notion.cached_client import CachedClient\nfrom cached_notion.utils import normalize_url, get_id_with_object_type, retrieve_object\nimport os\n\nclient = CachedClient(auth=os.environ["NOTION_TOKEN"], cache_delta=24)\n\n# Normalize the URL and extract the Notion ID and object type\nurl = "https://www.notion.so/xxx/xxx"\nnormalized_url = normalize_url(url)\nnid, object_type = get_id_with_object_type(normalized_url)\n\n# Use the retrieve_object utility function to get the object from Notion\nobj = retrieve_object(client, nid, object_type)\n\n# Now you can work with the retrieved object\nprint(obj)\n```\n\n```python\nfrom cached_notion.cached_client import CachedClient\nfrom cached_notion.utils import normalize_url, get_id_with_object_type, retrieve_all_content\nimport os\nclient = CachedClient(auth=os.environ["NOTION_TOKEN"], cache_delta=24)\n\n# Normalize the URL and extract the Notion ID and object type\nurl = "https://www.notion.so/xxx/xxx"\nnormalized_url = normalize_url(url)\nnid, object_type = get_id_with_object_type(normalized_url)\n\n# Use the retrieve_all_content function to get the full content from Notion\nfull_content = retrieve_all_content(client, nid, object_type)\n\n# Now you can work with the full content retrieved from Notion\nprint(full_content)\n```\n\n## Enhanced Caching Strategy 💡\n- **Cache Delta Explained:** Set `cache_delta` to manage how often the API calls the Notion API. A positive value uses cached content within the specified hours, reducing API calls. A zero value always fetches fresh content but minimizes API usage when used with `retrieve_all_content`.\n',
    'author': 'tim-watcha',
    'author_email': 'tim@watcha.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.1,<4.0.0',
}


setup(**setup_kwargs)
