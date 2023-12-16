<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->

<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<!-- 
***[![MIT License][license-shield]][license-url]
-->

<!-- PROJECT LOGO -->

<br />
<div align="center">
  <a href="https://github.com/microsoft/promptbench">
    <img src="imgs/promptbench_logo.png" alt="Logo" width="300">
  </a>

<!-- <h3 align="center">USB</h3> -->

<p align="center">
    <strong>PromptBench</strong>: A Unified Library for Evaluating and Understanding Large Language Models.
    <!-- <br />
    <a href="https://github.com/microsoft/promptbench"><strong>Explore the docs »</strong></a>
    <br /> -->
    <br />
    <a href="https://arxiv.org/abs/2312.07910">Paper</a>
    ·
    <a href="https://promptbench.readthedocs.io/en/latest/">Documentation</a>
    ·
    <a href="https://llm-eval.github.io/pages/leaderboard.html">Leaderboard</a>
    ·
    <a href="https://llm-eval.github.io/pages/papers.html">More papers</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#news-and-updates">News and Updates</a></li>
    <li><a href="#introduction">Introduction</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#supported-datasets-and-models">Datasets and Models</a></li>
    <li><a href="#benchmark-results">Benchmark Results</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- News and Updates -->

## News and Updates
- [15/12/2023] Add detailed instructions for users to add new modules (models, datasets, etc.) `examples/add_new_modules.md`. 
- [05/12/2023] Published promptbench 0.0.1.


<!-- Introduction -->

## Introduction

**PromptBench** is a Pytorch-based Python package for Evaluation of Large Language Models (LLMs). It provides user-friendly APIs for researchers to conduct evaluation on LLMs. Check the technical report: https://arxiv.org/abs/2312.07910.

![Code Structure](./imgs/promptbench.png)



### What does promptbench currently provide?
1. **Quick model performance assessment:** We offer a user-friendly interface that allows for quick model building, dataset loading, and evaluation of model performance.
2. **Prompt Engineering:** We implemented several prompt engineering methods. For example: [Few-shot Chain-of-Thought](https://arxiv.org/abs/2201.11903) [1],  [Emotion Prompt](https://arxiv.org/abs/2307.11760) [2], [Expert Prompting](https://arxiv.org/abs/2305.14688) [3] and so on.
3. **Evaluating adversarial prompts:** promptbench integrated [prompt attacks](https://arxiv.org/abs/2306.04528) [4], enabling researchers to simulate black-box adversarial prompt attacks on models and evaluate their robustness.
4. **Dynamic evaluation to mitigate potential test data contamination:** we integrated the dynamic evaluation framework [DyVal](https://arxiv.org/pdf/2309.17167) [5], which generates evaluation samples on-the-fly with controlled complexity.



<!-- GETTING STARTED -->

## Installation

### Install via `pip`
We provide a Python package *promptbench* for users who want to start evaluation quickly. Simply run 
```sh
pip install promptbench
```


### Install via GitHub

First, clone the repo:
```sh
git clone git@github.com:microsoft/promptbench.git
```

Then, 

```sh
cd promptbench
```

To install the required packages, you can create a conda environment:

```sh
conda create --name promptbench python=3.9
```

then use pip to install required packages:

```sh
pip install -r requirements.txt
```

Note that this only installed basic python packages. For Prompt Attacks, it requires to install textattacks.


## Usage

promptbench is easy to use and extend. Going through the bellowing examples will help you familiar with promptbench for quick use, evaluate an existing datasets and LLMs, or creating your own datasets and models.

<!-- TODO: add quick start example and refer lighting notebook -->

Please see [Installation](#installation) to install promptbench first. We provide ipynb tutorials for:

1. **evaluate models on existing benchmarks:** please refer to the `examples/basic.ipynb` for constructing your evaluation pipeline.
2. **test the effects of different prompting techniques:** 
3. **examine the robustness for prompt attacks**, please refer to `examples/prompt_attack.ipynb` to construct the attacks.
4. **use DyVal for evaluation:** please refer to `examples/dyval.ipynb` to construct DyVal datasets.


## Supported Datasets and Models

### Datasets

We support a range of datasets to facilitate comprehensive analysis, including:

- GLUE: SST-2, CoLA, QQP, MRPC, MNLI, QNLI, RTE, WNLI
- MMLU
- SQuAD V2
- IWSLT 2017
- UN Multi
- Math
- Bool Logic (BigBench)
- Valid Parentheses (BigBench)
- Object Tracking (BigBench)
- Date (BigBench)
- GSM8K
- CSQA (CommonSense QA)
- Numersense
- QASC
- Last Letter Concatenate

### Models

- google/flan-t5-large
- databricks/dolly-v1-6b
- llama2 (7b, 13b, 7b-chat, 13b-chat)
- vicuna-13b, vicuna-13b-v1.3
- cerebras/Cerebras-GPT-13B
- EleutherAI/gpt-neox-20b
- google/flan-ul2
- palm
- chatgpt, gpt4

## Benchmark Results

Please refer to our [benchmark website](llm-eval.github.io) for benchmark results on Prompt Attacks, Prompt Engineering and Dynamic Evaluation DyVal.

## TODO
- [ ] Add prompt attacks and prompt engineering documents.

## Acknowledgements

- [textattacks](https://github.com/textattacks)
- [README Template](https://github.com/othneildrew/Best-README-Template)
- We thank the volunteers: Hanyuan Zhang, Lingrui Li, Yating Zhou for conducting the semantic preserving experiment in Prompt Attack benchmark.


## Reference
[1] Jason Wei, et al. "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." arXiv preprint arXiv:2201.11903 (2022).

[2] Cheng Li, et al. "Emotionprompt: Leveraging psychology for large language models enhancement via emotional stimulus." arXiv preprint arXiv:2307.11760 (2023).

[3] BenFeng Xu, et al. "ExpertPrompting: Instructing Large Language Models to be Distinguished Experts" arXiv preprint arXiv:2305.14688 (2023).

[4] Zhu, Kaijie, et al. "PromptBench: Towards Evaluating the Robustness of Large Language Models on Adversarial Prompts." arXiv preprint arXiv:2306.04528 (2023).

[5] Zhu, Kaijie, et al. "DyVal: Graph-informed Dynamic Evaluation of Large Language Models." arXiv preprint arXiv:2309.17167 (2023).

<!-- CITE -->

## Citing promptbench and other research papers

Please cite us if you fine this project helpful for your project/paper:

```
@article{zhu2023promptbench2,
  title={PromptBench: A Unified Library for Evaluation of Large Language Models},
  author={Zhu, Kaijie and Zhao, Qinlin and Chen, Hao and Wang, Jindong and Xie, Xing},
  journal={arXiv preprint arXiv:2312.07910},
  year={2023}
}

@article{zhu2023promptbench,
  title={PromptBench: Towards Evaluating the Robustness of Large Language Models on Adversarial Prompts},
  author={Zhu, Kaijie and Wang, Jindong and Zhou, Jiaheng and Wang, Zichen and Chen, Hao and Wang, Yidong and Yang, Linyi and Ye, Wei and Gong, Neil Zhenqiang and Zhang, Yue and others},
  journal={arXiv preprint arXiv:2306.04528},
  year={2023}
}

@article{zhu2023dyval,
  title={DyVal: Graph-informed Dynamic Evaluation of Large Language Models},
  author={Zhu, Kaijie and Chen, Jiaao and Wang, Jindong and Gong, Neil Zhenqiang and Yang, Diyi and Xie, Xing},
  journal={arXiv preprint arXiv:2309.17167},
  year={2023}
}

@article{chang2023survey,
  title={A survey on evaluation of large language models},
  author={Chang, Yupeng and Wang, Xu and Wang, Jindong and Wu, Yuan and Zhu, Kaijie and Chen, Hao and Yang, Linyi and Yi, Xiaoyuan and Wang, Cunxiang and Wang, Yidong and others},
  journal={arXiv preprint arXiv:2307.03109},
  year={2023}
}

```

<!-- CONTRIBUTING -->

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

If you have a suggestion that would make promptbench better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the project
2. Create your branch (`git checkout -b your_name/your_branch`)
3. Commit your changes (`git commit -m 'Add some features'`)
4. Push to the branch (`git push origin your_name/your_branch`)
5. Open a Pull Request


<!-- TRADEMARKS -->

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft&#39;s Trademark &amp; Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.





<!-- MARKDOWN LINKS & IMAGES -->

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/microsoft/promptbench.svg?style=for-the-badge
[contributors-url]: https://github.com/microsoft/promptbench/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/microsoft/promptbench.svg?style=for-the-badge
[forks-url]: https://github.com/microsoft/promptbench/network/members
[stars-shield]: https://img.shields.io/github/stars/microsoft/promptbench.svg?style=for-the-badge
[stars-url]: https://github.com/microsoft/promptbench/stargazers
[issues-shield]: https://img.shields.io/github/issues/microsoft/promptbench.svg?style=for-the-badge
[issues-url]: https://github.com/microsoft/promptbench/issues
[license-shield]: https://img.shields.io/github/license/microsoft/promptbench.svg?style=for-the-badge
[license-url]: https://github.com/microsoft/promptbench/blob/main/LICENSE.txt
