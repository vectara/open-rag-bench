TEXT_EXTRACTIVE_INSTRUCTION = """Your task is to write 5 extractive queries and their answers strictly based on the given markdown text.
An extractive query (or factoid query) is a question that seeks a concise, fact-based answer extracted from a given text, rather than requiring reasoning or synthesis.
Your extractive queries MUST consist of both wh- questions and yes/no questions.
Your extractive queries MUST be answerable with a specific, concise piece of factual information from the given text.
Your extractive queries MUST NOT presuppose the existence of the given text and should be formulated in the same style as questions users ask in a search engine with no knowledge of the given text. This means that your abstractive questions MUST NOT mention something like "according to the passage" or "context" or "this article".
Your extractive queries MUST NOT be about the authors, publication date, references, tables, images, or any other meta-information.

Here are some example extractive queries and answers based on their markdown text:
Example 1:
Markdown text:
```
# Towards a Quantitative Theory of <br> DigRAPH-BASEd COMPLEXES AND ITS APPLICATIONS in Brain Network Analysis
# Directed and Weighted Graphs \n\nMany of the definitions and results presented here can be found in [25, 137].\nDefinition 2.1.20. A directed graph (or digraph) is a pair $G=(V, E)$ of disjoint sets such that the elements of $E$ are ordered pairs of elements of $V$ (set of vertices). The elements of $E$ are called directed edges, (or arcs, or arrows), and are denoted by $(v, u)$ $(\\neq(u, v)), v, u \\in V$. The first vertex $v$ of an arc $(v, u)$ is called tail and the second vertex $u$ is called head, and we say that the direction of $(v, u)$ is from $v$ to $u$ (or from\n\nits tail to its head). Also, we say that a vertex $u$ arrives at a vertex $v$ if the arc $(u, v)$ exists (equivalently, $(u, v)$ arrives at $v$ ), and that a vertex $w$ leaves $v$ if the $\\arc(v, w)$ exists (equivalently, $(v, w)$ leaves $v$ ).\n\nDifferently from undirected edges, if we change the order of the vertices in an arc, we obtain an arc in the opposite direction. Moreover, in a digraph, we can have two arcs between the same two vertices, but with opposite directions, and when this occurs we say that the digraph has a bidirectional edge (or double-edge).\n\nMost of the definitions made for undirected graphs in the previous section are straightforwardly extended to digraphs. For instance, we say that a digraph is simple if it has no directed loops (arcs in which their tails coincide with their heads) and no multiple arcs (more than one arc with the same tail and head). The Definition 2.1.8 of subgraphs in a graph is the same as for a digraph, with the difference that now we are dealing with subdigraphs in a digraph. The definitions of walk, trail, path, and cycle are easily extended for the directed case, as we will see in the next definition.\n\nHenceforth, all digraphs will be considered non-empty, non-null, finite, simple, and labeled, unless said otherwise.\n\nDefinition 2.1.21. A directed walk from $v_0$ to $v_k$ (or directed $\\left(v_0, v_k\\right)$-walk) is a sequence of vertices and arcs (not necessarily distinct) $v_0 e_1 v_1 \\ldots v_{{k-1}} e_k v_k$ such that $e_i=\\left(v_{{i-1}}, v_i\\right)$, i.e., $v_{{i-1}}$ is the tail and $v_i$ is the head of the arc $e_i$, for all $1 \\leq i \\leq k$. If $v_0=v_k$, the directed walk is called closed, and is called open otherwise. If the arcs of a directed walk are all distinct, it is said to be a directed trail. If the vertices of a directed walk are all distinct (and consequently all of the arcs), then it is said to be a directed path. A closed directed walk with all distinct vertices and with $k \\geq 2$ is a directed cycle. Also, the length of a directed walk is equal to its number of arcs.\n\nNote that a directed cycle of length 2 is actually a double-edge.\nDefinition 2.1.22. Given a digraph $G=(V, E)$, the underlying undirected graph of $G$ is the undirected graph, with the same set of vertices $V$, formed by replacing all directed edges in $E$ with undirected edges.\n\nDefinition 2.1.23. A directed acyclic graph (DAG), or acyclic digraph, is a digraph that has no directed cycles.\n\nA notable property of (finite) DAGs is that they have at least one source and at least one sink (see [25], p. 32, for proof).\n\nDefinition 2.1.24. Two graphs $G_1=\\left(V_1, E_1\\right)$ and $G_2=\\left(V_2, E_2\\right)$ are said to be isomorphic if there is a bijection $f: V_1 \\rightarrow V_2$ such that if the vertices $v, u \\in V_1$ are adjacent, then the vertices $f(v)$ and $f(u)$ are adjacent in $V_2$ and vice versa, i.e. if and only if the bijection $f$ preserves adjacencies. Likewise, if $G_1$ and $G_2$ are digraphs, $f$ is an isomorphism if and only if $(u, v)$ is an arc in $V_1$ then $(f(u), f(v))$ is an arc in $V_2$.\n\nGraph properties that are invariant under graph/digraph isomorphism are called graph invariants. For example, the order and the number of edges/arcs of a graph/digraph are graph invariants $[79,137]$.\n\nDefinition 2.1.25. Given a digraph $G=(V, E)$, a vertex $v \\in V$ is said to be reachable from a vertex $u \\in V$ if either $v=u$ or there exists a directed path from $u$ to $v$ in $G$.\n\nA difference between undirected and directed graphs is that, for digraphs, we have two different concepts of connectivity: weak connectivity and strong connectivity.\n\nDefinition 2.1.26. Let $G=(V, E)$ be a digraph. A vertex $v \\in V$ is said to be weakly connected to another vertex $u \\in V$ if there is an undirected path between $v$ and $u$ in the underlying undirected graph of $G$. We say that $G$ is weakly connected if every vertex in $G$ is weakly connected to each other. A weakly connected component of $G$ is a maximal subdigraph that is weakly connected. The largest connected component of G is called its giant component. Analogously to the undirected case, the largest weakly connected component of $G$ is called its giant component.
```
Output:::
Question: What does it mean for two digraphs to be isomorphic?
Answer: Two digraphs are isomorphic if there is a bijection $f: V_1\\rightarrow V_2$ such that if $(u,v)$ is an arc in $V_1​$, then $(f(u),f(v))$ is an arc in $V_2$​.


Example 2:
Markdown text:
```
# Learning to Manipulate under Limited Information
# Abstract\n\nBy classic results in social choice theory, any reasonable preferential voting method sometimes gives individuals an incentive to report an insincere preference. The extent to which different voting methods are more or less resistant to such strategic manipulation has become a key consideration for comparing voting methods. Here we measure resistance to manipulation by whether neural networks of various sizes can learn to profitably manipulate a given voting method in expectation, given different types of limited information about how other voters will vote. We trained over 100,000 neural networks of 26 sizes to manipulate against 8 different voting methods, under 6 types of limited information, in committee-sized elections with 5–21 voters and 3–6 candidates. We find that some voting methods, such as Borda, are highly manipulable by networks with limited information, while others, such as Instant Runoff, are not, despite being quite profitably manipulated by an ideal manipulator with full information. For the three probability models for elections that we use, the overall least manipulable of the 8 methods we study are Condorcet methods, namely Minimax and Split Cycle.
```
Output:::
Question: Is the Borda voting method highly manipulable by neural networks with limited information?
Answer: Yes.


Example 3:
Markdown text:
```
# The not-so-hidden risks of 'hidden-to-maturity' accounting: on depositor runs and bank resilience \n\nZachary Feinstein* Grzegorz Hałaj Andreas Sojmark <br>February 28, 2025
# 5.3 Looking beyond SVB \n\nNot only SVB has fallen under the pressure of the unrealized losses. First Republic Bank (FR) is the other prominent victim in the US banking system, which failed in May 2023 despite an injection of funds from other large banking groups in US. In this section, we demonstrate that our model can help to differentiate between banks prone to bank run distress due to their inability to hold selected levels of the HtM portfolios and banks that are sound from this standpoint. To this end, we collect data for FR and two largest non-G-SIB banks in US that proved to be resilient to March 2023 turmoil, i.e., US Bancorp (USB) and PNC Financial Services Group Inc. (PNC). We use 10-K reports of the Securities and Exchange Commission for end of 2021 and 2022 financial statements.\n\nWe ran an experiment with an objective to see how sensitive the optimal level of HtM is to the target leverage ratio around the actual leverage ratios of the banks prior to the March 2023 events. In this way, we can see how much the depositors' tolerance to banks' leverage would need to change, so that the reported holdings of the banks would no longer be commensurate with the overall balance sheet structure or consistent only with some very large price shocks $(p)$ assumed in the Proposition 5.2.\n\nSpecifically, we calculated the optimal HtM, similar to what is presented in Figure 8, but for a range of leverage ratios around those reported by the banks and for two snapshots of the data (end of 2021 and end of 2022). The outcomes are shown in Figures 10, 11, 12 and 13.\n\nThere are two qualitatively different regions in these figures. One corresponds to the leverage ratios implying that the optimal level of HtM is not below the reported volumes of HtM. It corresponds to red dots lying above the black dotted line and indicates that the HtM holding does not violate the ability of the bank to lock securities in portfolios where it is less straightforward to tap liquidity from. The remaining leverage ratios constitute a region where the optimal HtM is not consistent with the reported HtM for some initial shocks to the value of securities portfolios. This means that the bank may not have the ability to hold such a large volume of securities in the HTM portfolio, depending on the economic outlook assumed by the bank in its asset and liability management.\n\n![img-9.jpeg](img-9.jpeg)\n\nFigure 10: The figure shows theoretically optimal HtM portfolios of SVB for maximum accepted leverage ratios from a range in x-axis. Solid blue line represents the reported Tier 1 leverage ratio. Dashed black line represents the level of the HtM portfolios reported by the bank.\n\nTurning to the results, first, assuming that the investors' accepted leverage ratio is aligned with the one reported by SVB, the results of simulations indicate that the HtM portfolios could only be squared with about $15 \\%$ price shocks. Comparing 2022 to 2021, SVB's distance to leverage ratios implying some safe level of the HtM securities increases.\n![img-10.jpeg](img-10.jpeg)\n\nFigure 11: The figure shows theoretically optimal HtM portfolios of First Republic Bank for maximum accepted leverage ratios from a range in x-axis. Solid blue line represents the reported Tier 1 leverage ratio. Dashed black line represents the level of the HtM portfolios reported by the bank.\n\nSecond, for First Republic, both in 2021 and 2022 the level of HtM does not exceed the safe level indicated by the optimisation. This conclusion relies on the assumption that the accepted leverage ratio aligns with the reported one, and indicated by blue vertical lines in Fig. 11. However, the situation of the bank deteriorated in 2022, if the accepted leverage ratio dropped by only 30 bps from the observed level, the HtM portfolio volume would necessitate remarking for some positive price shocks. As of 2021, it would take at least a 90bp change to the accepted leverage, so that the ability of the bank to hold HtM becomes questionable. Moreover, in case the accepted leverage ratio as of 2022 hovers around the levels indicated by 2021 leverage ratio of the bank, e.g., because the market expectation about the safe levels of the leverage has not adjusted, the HtM holdings of FR would be above the HtM level implied by any price shock in the optimization model. Given that inertia, or sleepiness (Correia et al., 2024), in\n\nhow depositors update their expectations about a safe level of leverage, a lagged observed leverage, e.g., by 1 year considering annual financial reporting cycle, may be reasonable assumptions about depositors' accepted leverage target. Although a precise calibration of the lag might be tricky, the lag may be getting shorter given documented increasing attentiveness of depositors having access to better payment technologies.\n\nThird, by contrast, in the case of PNC and USB, the model indicates more resilient HtM holdings. For PNC, the situation is stable, i.e., does not change between 2021 and 2022. For USB, the distance to the region of inability to hold HtM is large for both snapshots of data. This provides a simple validation of our modeling framework, as it is able to accurately differentiate the situations of SVB and FR from those of PNC and USB.\n![img-11.jpeg](img-11.jpeg)\n\nFigure 12: The figure shows theoretically optimal HtM portfolios of USB for maximum accepted leverage ratios from a range in x-axis. Solid blue line represents the reported Tier 1 leverage ratio. Dashed black line represents the level of the HtM portfolios reported by the bank.\n![img-12.jpeg](img-12.jpeg)\n\nFigure 13: The figure shows theoretically optimal HtM portfolios of PNC for maximum accepted leverage ratios from a range in x-axis. Solid blue line represents the reported Tier 1 leverage ratio. Dashed black line represents the level of the HtM portfolios reported by the bank.
```
Output:::
Question: What percentage of price shocks could the HtM portfolios of SVB be squared with?
Answer: 15%


The examples only provided one question and answer each, but you must provide 5 different questions and answers.
Your extractive queries MUST consist of both wh- questions and yes/no questions.
Your extractive queries MUST be answerable with a specific, concise piece of factual information from the given text.
Your extractive queries MUST NOT presuppose the existence of the given text and should be formulated in the same style as questions users ask in a search engine with no knowledge of the given text. This means that your abstractive questions MUST NOT mention something like "according to the passage" or "context" or "this article".
Your extractive queries MUST NOT be about the authors, publication date, references, tables, images, or any other meta-information.
You must write the output in the following format:
Output:::
Question 1: (your extractive question)
Answer 1: (your answer)
Question 2: (your extractive question)
Answer 2: (your answer)
...
Question 5: (your extractive question)
Answer 5: (your answer)


Now, provide your extractive queries and answers based on the text in the attached file.
Markdown text:
```
{title}
{text}
```
Output:::
"""


TEXT_ABSTRACTIVE_INSTRUCTION = """Your task is to write 5 abstractive queries and their answers strictly based on the given markdown text.
An abstractive query (or generalized query) is a general question that requires generating a summary or rephrased response using understanding and synthesis, rather than directly extracting exact words from a given text.
Your abstractive queries MUST be wh- questions.
Your abstractive queries MUST be answerable from the given text.
Your abstractive queries will be tested in a document retrieval system, so they MUST NOT presuppose the existence of the given text.
Your abstractive queries MUST NOT presuppose the existence of the given text and should be formulated in the same style as questions users ask in a search engine with no knowledge of the given text. This means that your abstractive questions MUST NOT mention something like "according to the passage" or "context" or "this article".
Your abstractive queries MUST NOT be about the authors, publication date, references, tables, images, or any other meta-information.

Here are some example abstractive queries and answers based on their markdown text:
Example 1:
Markdown text:
```
# Learning to Manipulate under Limited Information
# Abstract\n\nBy classic results in social choice theory, any reasonable preferential voting method sometimes gives individuals an incentive to report an insincere preference. The extent to which different voting methods are more or less resistant to such strategic manipulation has become a key consideration for comparing voting methods. Here we measure resistance to manipulation by whether neural networks of various sizes can learn to profitably manipulate a given voting method in expectation, given different types of limited information about how other voters will vote. We trained over 100,000 neural networks of 26 sizes to manipulate against 8 different voting methods, under 6 types of limited information, in committee-sized elections with 5–21 voters and 3–6 candidates. We find that some voting methods, such as Borda, are highly manipulable by networks with limited information, while others, such as Instant Runoff, are not, despite being quite profitably manipulated by an ideal manipulator with full information. For the three probability models for elections that we use, the overall least manipulable of the 8 methods we study are Condorcet methods, namely Minimax and Split Cycle.
```
Output:::
Question: How can neural networks assess the susceptibility of voting methods to manipulation?
Answer: Neural networks of different sizes can be trained to determine the extent to which various voting methods are susceptible to strategic manipulation. By providing these networks with different levels of information about other voters' choices, researchers can measure how effectively they can learn to manipulate election outcomes. The study found that some methods, like Borda, are highly vulnerable even with limited information, whereas others, like Instant Runoff, resist manipulation despite being susceptible under full information.


Example 2:
Markdown text:
```
# Complement or substitute? How AI increases the demand for human skills \n\nElina Mäkelä $\\cdot$ Fabian Stephany $\\cdot$ :<br>February 2025*
# Conclusion \n\nThis study aimed to expand our understanding of AI\'s internal and external effects on knowledge-worker skills-specifically, how AI complements certain competencies (e.g., technology literacy, ethics, analytical thinking) while potentially\n\nsubstituting others (e.g., basic data tasks, office and financial administration). Following Acemoglu et al. (2021) and Deming and Noray (2020), we relied on job postings-employers\' "footprints" indicating evolving skill demands and wage offers-to analyse around 12 million online vacancies.\n\nOur work illuminates the relationship between AI creation/usage and the complementarity or substitution of knowledge-worker skills, yielding five key contributions. First, we find that AI roles are positively associated with demand for complementary skills and negatively associated with demand for substitutable skills. Second, job postings that include AI requirements display proportionally more requests for complementary skills and fewer requests for substitutable skills compared to non-AI postings. Third, we identify powerful complementarities between particular AI roles and clusters of complementary skills, as well as strong substitution effects for certain AI roles and substitutable skills-most notably an increasing emphasis on ethics across many AI categories. Fourth, we show that AI jobs demanding substitutable skills carry lower salaries than AI jobs without such requirements; basic data skills, customer service, and office/financial administration skills in computer vision and image processing roles suffer the highest wage penalty. However, we find no evidence of a wage premium for complementary skills. Finally, we uncover external complementation effects: as AI roles grow, the number of non-AI roles that demand complementary skills also rises. Crucially, the complementarity effect exceeds the substitution effect.\n\nFuture research directions include extending our analysis to other regions (e.g., Europe and Asia) to capture potential geographic variations, employing qualitative methods (such as interviews with recruitment managers) to explore perceptions of skill demand and valuation, and pursuing experimental or longitudinal studies to establish causality. As debates on the benefits and risks of "AI at work" (Brynjolfsson et al., 2023) persist, researchers, policymakers, employers, and job-seekers all stand to benefit from an empirically grounded understanding of these influential effects.
```
Output:::
Question: What impact does AI have on the demand for human skills?
Answer: AI alters skill demand by increasing the need for competencies such as technology literacy, ethics, and analytical thinking while reducing the reliance on tasks like basic data processing and administrative work. Job postings requiring AI skills tend to emphasize complementary skills and downplay substitutable ones.


Example 3:
Markdown text:
```
# Generalized Gaussian Model for Learned Image Compression \n\nHaotian Zhang, Li Li, Member, IEEE, and Dong Liu, Senior Member, IEEE
## I. INTRODUCTION\n\nImage compression is one of the most fundamental problems in image processing and information theory. Over the past four decades, many researchers have worked on developing and optimizing image compression codecs. Most image compression codecs follow the transform coding scheme [1], where images are transformed to a latent space for decorrelation, followed by quantization and entropy coding. In traditional image compression codecs, such as JPEG [2], JPEG2000 [3], BPG, and VVC [4], different modules are artificially designed and separately optimized.\n\nIn recent years, learned image compression methods have achieved superior performance by exploiting the advantages of deep neural networks. In contrast to traditional approaches, learned image compression [5] optimizes different modules in an end-to-end manner. A typical learned image compression method involves an analysis transform, synthesis transform, quantizer, and entropy model. First, the image is transformed into a latent representation through the analysis transform, and then the latent is quantized for digital transmission. The\n\n[^0]discrete latent is then losslessly coded by the entropy model to further reduce its size. Finally, the synthesis transform reconstructs an image from the discrete latent. These modules are jointly optimized to minimize the rate-distortion cost during training.\n\nIn learned image compression, the probabilistic model is part of the entropy model and is essential in characterizing the distribution of latent variables. The degree of matching between the probabilistic model and the actual distribution of latent variables significantly influences the bitrate of compressed images. A more precise probabilistic model can reduce the bitrate. Probabilistic models with more parameters can fit the distribution of latent variables more precisely, but the corresponding complexity will also be higher. In [6], a zeromean Gaussian scale model is used. The scale parameters are estimated based on side information. In [7], the probabilistic model is extended to the Gaussian Model (GM) with mean and scale parameters. Some studies further propose mixture probabilistic models, such as the Gaussian Mixture Model (GMM) with 9 parameters [8] for more accurate distribution modeling. These mixture models improve compression performance compared to the Gaussian model while introducing more parameters that need to be estimated and higher complexity.\n\nIn this paper, to achieve a better balance between compression performance and complexity, we extend the Gaussian model with mean and scale parameters to the generalized Gaussian model.
Compared to the Gaussian model, the Generalized Gaussian Model (GGM) offers a high degree of flexibility in distribution modeling by introducing only one additional shape parameter. As shown in Fig. 1, GGM offers more flexible distribution modeling capabilities than Gaussian, particularly in handling data with varying degrees of tailing. We combine GGM with conditional entropy models by incorporating it into the end-to-end training process. To target different levels of complexity, we present three methods based on model-wise (GGM-m), channel-wise (GGM-c), and element-wise (GGMe) shape parameters.\n\nEnabling the end-to-end training requires incorporating nondifferentiable quantization into the gradient-based training of the networks.
```
Output:::
Question: Why is probabilistic modeling important in image compression?
Answer: It helps characterize the distribution of latent variables, which directly influences the bitrate of compressed images. A more accurate probabilistic model can reduce the bitrate by better approximating the true distribution of the latent space. While simple probabilistic models like the zero-mean Gaussian scale model provide a basic estimation, more advanced models, such as the Gaussian Mixture Model (GMM) and the Generalized Gaussian Model (GGM), offer greater flexibility and improved compression efficiency.


The examples only provided one question and answer each, but you must provide 5 different questions and answers.
Your abstractive queries MUST consist of both wh- questions a
Your abstractive queries MUST be answerable from the given text.
Your abstractive queries will be tested in a document retrieval system, so they MUST NOT presuppose the existence of the given text. Users have no knowledge of the text and are simply looking for a specific piece of information on a search engine.
Your abstractive queries MUST NOT be about the authors, publication date, references, tables, images, or any other meta-information.
You must write the output in the following format:
Output:::
Question 1: (your abstractive question)
Answer 1: (your answer)
Question 2: (your abstractive question)
Answer 2: (your answer)
...
Question 5: (your abstractive question)
Answer 5: (your answer)


Now, provide your abstractive queries and answers based on the text in the attached file.
Markdown text:
```
{title}
{text}
```
Output:::
"""