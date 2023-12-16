# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_mamba']

package_data = \
{'': ['*']}

install_requires = \
['swarms', 'torch', 'torchvision', 'zetascale']

setup_kwargs = {
    'name': 'simple-mamba',
    'version': '0.0.4',
    'description': 'Simple Mambda - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Simple Mamba\n\n## Install\n`pip install simple-mamba`\n\n\n## Usage\n```python\nimport torch\nfrom simple_mamba import MambaBlock\n\n\n# Define block parameters\ndim = 512\nhidden_dim = 128\nheads = 8\nin_channels = 3\nout_channels = 3\nkernel_size = 3\n\n# Create an instance of MambaBlock\nmamba_block = MambaBlock(\n    dim, hidden_dim, heads, in_channels, out_channels, kernel_size\n)\n\n# Create a sample input tensor\nx = torch.randn(1, dim, dim)\n\n# Pass the tensor through the MambaBlock\noutput = mamba_block(x)\nprint("Output shape:", output.shape)\n\n\n```\n\n### `SSM`\n```python\nimport torch \nfrom simple_mamba import SSM\n\n\n# # Example usage\nvocab_size = 10000  # Example vocabulary size\nembed_dim = 256  # Example embedding dimension\nstate_dim = 512  # State dimension\nnum_layers = 2  # Number of state-space layers\n\nmodel = SSM(vocab_size, embed_dim, state_dim, num_layers)\n\n# Example input (sequence of word indices)\ninput_seq = torch.randint(\n     0, vocab_size, (32, 10)\n )  # Batch size of 32, sequence length of 10\n\n # Forward pass\nlogits = model(input_seq)\nprint(logits.shape)  # Should be [32, 10, vocab_size]\n\n```\n\n\n# License\nMIT\n\n\n# Citation\n```bibtex\n@misc{gu2023mamba,\n    title={Mamba: Linear-Time Sequence Modeling with Selective State Spaces}, \n    author={Albert Gu and Tri Dao},\n    year={2023},\n    eprint={2312.00752},\n    archivePrefix={arXiv},\n    primaryClass={cs.LG}\n}\n\n```',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/SimpleMamba ',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
