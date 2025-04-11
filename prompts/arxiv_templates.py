EXTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any documents yet. Specifically, your task is to simulate 5 extractive queries and their answers for the given markdown text that users would type BEFORE finding any relevant documents. Here are your guidelines:
- An extractive query (or factoid query) is a question that seeks a concise, fact-based answer extracted from a given text, rather than requiring reasoning or synthesis. It MUST be answerable with a specific, concise piece of factual information from the given text.
- Your extractive queries MUST consist of both wh- questions and yes/no questions.
- Your extractive queries MUST be realistic search queries users ask without assuming knowledge of the specific text.
- Your extractive queries MUST avoid the authors, publication date, references, tables, images, or any other meta-information.{table_instruction}{image_instruction}

Here are some example extractive queries and answers based on their markdown text:
Example 1:
Markdown text:
```
# Towards a Quantitative Theory of <br> DigRAPH-BASEd COMPLEXES AND ITS APPLICATIONS in Brain Network Analysis
# Directed and Weighted Graphs \n\nMost of the definitions made for undirected graphs in the previous section are straightforwardly extended to digraphs. For instance, we say that a digraph is simple if it has no directed loops (arcs in which their tails coincide with their heads) and no multiple arcs (more than one arc with the same tail and head). The Definition 2.1.8 of subgraphs in a graph is the same as for a digraph, with the difference that now we are dealing with subdigraphs in a digraph. The definitions of walk, trail, path, and cycle are easily extended for the directed case, as we will see in the next definition.\n\nHenceforth, all digraphs will be considered non-empty, non-null, finite, simple, and labeled, unless said otherwise.\n\nDefinition 2.1.21. A directed walk from $v_0$ to $v_k$ (or directed $\\left(v_0, v_k\\right)$-walk) is a sequence of vertices and arcs (not necessarily distinct). If $v_0=v_k$, the directed walk is called closed, and is called open otherwise. If the arcs of a directed walk are all distinct, it is said to be a directed trail. If the vertices of a directed walk are all distinct (and consequently all of the arcs), then it is said to be a directed path. A closed directed walk with all distinct vertices and with $k \\geq 2$ is a directed cycle. Also, the length of a directed walk is equal to its number of arcs.\n\nNote that a directed cycle of length 2 is actually a double-edge.\nDefinition 2.1.22. Given a digraph $G=(V, E)$, the underlying undirected graph of $G$ is the undirected graph, with the same set of vertices $V$, formed by replacing all directed edges in $E$ with undirected edges.\n\nDefinition 2.1.23. A directed acyclic graph (DAG), or acyclic digraph, is a digraph that has no directed cycles.\n\nA notable property of (finite) DAGs is that they have at least one source and at least one sink (see [25], p. 32, for proof).\n\nDefinition 2.1.24. Two graphs $G_1=\\left(V_1, E_1\\right)$ and $G_2=\\left(V_2, E_2\\right)$ are said to be isomorphic if there is a bijection $f: V_1 \\rightarrow V_2$ such that if the vertices $v, u \\in V_1$ are adjacent, then the vertices $f(v)$ and $f(u)$ are adjacent in $V_2$ and vice versa, i.e. if and only if the bijection $f$ preserves adjacencies. Likewise, if $G_1$ and $G_2$ are digraphs, $f$ is an isomorphism if and only if $(u, v)$ is an arc in $V_1$ then $(f(u), f(v))$ is an arc in $V_2$.
```
Output:::
Query: What does it mean for two digraphs to be isomorphic?
Answer: Two digraphs are isomorphic if there is a bijection $f: V_1\\rightarrow V_2$ such that if $(u,v)$ is an arc in $V_1​$, then $(f(u),f(v))$ is an arc in $V_2$​.


Example 2:
Markdown text:
```
# Learning to Manipulate under Limited Information
# By classic results in social choice theory, any reasonable preferential voting method sometimes gives individuals an incentive to report an insincere preference. The extent to which different voting methods are more or less resistant to such strategic manipulation has become a key consideration for comparing voting methods. Here we measure resistance to manipulation by whether neural networks of various sizes can learn to profitably manipulate a given voting method in expectation, given different types of limited information about how other voters will vote. We trained over 100,000 neural networks of 26 sizes to manipulate against 8 different voting methods, under 6 types of limited information, in committee-sized elections with 5–21 voters and 3–6 candidates. We find that some voting methods, such as Borda, are highly manipulable by networks with limited information, while others, such as Instant Runoff, are not, despite being quite profitably manipulated by an ideal manipulator with full information. For the three probability models for elections that we use, the overall least manipulable of the 8 methods we study are Condorcet methods, namely Minimax and Split Cycle.
```
Output:::
Query: Is the Borda voting method highly manipulable by neural networks with limited information?
Answer: Yes.


Example 3:
Markdown text:
```
# Ultra-rapid, Quantitative, Label-free Antibiotic Susceptibility Testing via Optically Detected Purine Metabolites
# A detailed phenomenological example of how SERS provides ultra-rapid ( $\\sim 1$ hour) drug susceptibility information is illustrated in Fig. 2 for E. coli ATCC 2452. Following the gold standard CLSI growth-based procedure for determining quantitative drug susceptibilities, this Gram-negative strain is found to be susceptible to the broad spectrum bacteriostatic antibiotic, tetracycline, but resistant to the $\\beta$-lactam, ampicillin.  SERS-AST determinations take $\\sim$ one hour including incubation time. The SERS intensity independence indicates this strain is resistant to ampicillin as found both by the 24hour growth (d.) and $\\sim$ one hour SERS AST approaches (e., f.). The (c) and (s) designations indicate if the antibiotic is bactericidal or bacteriostatic.\nthe growth of this strain after 24 hours as evidenced by the unchanged OD for all E. coli 2452 samples with ampicillin concentrations in this range and is thus ampicillin resistant.\n\nThe corresponding 785 nm excited SERS spectra of E. coli 2452 as a function of doubling tetracycline concentrations during a 30-minute incubation period are displayed in Fig. 2b. Following this incubation in MHB growth media and a specific antibiotic concentration, bacterial solutions are water washed and centrifuged three times before a bacterial solution is dropped on the Au SERS substrate a Raman signal is acquired, as described above. A SERS spectral measurement is completed within one hour including the 30 -minute drug incubation, washing and SERS signal acquisition. The spectra shown in Fig. 2b are all normalized to the maximum intensity of the most intense SERS spectral feature observed for this series of E. coli 2452/tetracycline spectra which is the $\\sim 730 cm$ band in the E. coli sample lacking any tetracycline during the 30 minute incubation period. The relative intensities of these SERS spectra decrease as a function of tetracycline concentration over the 0 to $16 mg / L$ range (Fig. 2b).
```
Output:::
Query: How long does the SERS-AST methodology take to determine MIC values?
Answer: Approximately 1 hour.


The examples only provided one query and answer each, but you must provide 5 different queries and answers in the following format:
Query 1: (your extractive query)
Answer 1: (your answer)
Query 2: (your extractive query)
Answer 2: (your answer)
...
Query 5: (your extractive query)
Answer 5: (your answer)

Remember,
- Your extractive queries MUST consist of both wh- questions and yes/no questions.
- Your extractive queries MUST be realistic search queries users ask without assuming knowledge of the specific text.
- Your extractive queries MUST avoid the authors, publication date, references, tables, images, or any other meta-information.{table_instruction}{image_instruction}

Now, provide your extractive queries and answers based on the markdown text.
Markdown text:
```
{title}
{text}
```
Output:::
"""

ABSTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any documents yet. Specifically, your task is to simulate 5 abstractive queries and their answers for the given markdown text that users would type BEFORE finding any relevant documents. Here are your guidelines:
- An abstractive query (or generalized query) is a general question that requires generating a summary or rephrased response using understanding and synthesis, rather than directly extracting exact words from a given text.
- Your abstractive queries MUST be wh- questions.
- Your abstractive queries MUST be realistic search queries users ask without assuming knowledge of the specific text.
- Your abstractive queries MUST avoid the authors, publication date, references, tables, images, or any other meta-information.

Here are some example abstractive queries and answers based on their markdown text:
Example 1:
Markdown text:
```
# Learning to Manipulate under Limited Information
# Abstract\n\nBy classic results in social choice theory, any reasonable preferential voting method sometimes gives individuals an incentive to report an insincere preference. The extent to which different voting methods are more or less resistant to such strategic manipulation has become a key consideration for comparing voting methods. Here we measure resistance to manipulation by whether neural networks of various sizes can learn to profitably manipulate a given voting method in expectation, given different types of limited information about how other voters will vote. We trained over 100,000 neural networks of 26 sizes to manipulate against 8 different voting methods, under 6 types of limited information, in committee-sized elections with 5–21 voters and 3–6 candidates. We find that some voting methods, such as Borda, are highly manipulable by networks with limited information, while others, such as Instant Runoff, are not, despite being quite profitably manipulated by an ideal manipulator with full information. For the three probability models for elections that we use, the overall least manipulable of the 8 methods we study are Condorcet methods, namely Minimax and Split Cycle.
```
Output:::
Query: How can neural networks assess the susceptibility of voting methods to manipulation?
Answer: Neural networks of different sizes can be trained to determine the extent to which various voting methods are susceptible to strategic manipulation. By providing these networks with different levels of information about other voters' choices, researchers can measure how effectively they can learn to manipulate election outcomes. The study found that some methods, like Borda, are highly vulnerable even with limited information, whereas others, like Instant Runoff, resist manipulation despite being susceptible under full information.


Example 2:
Markdown text:
```
# Complement or substitute? How AI increases the demand for human skills \n\nElina Mäkelä $\\cdot$ Fabian Stephany $\\cdot$ :<br>February 2025*
# Conclusion \n\nThis study aimed to expand our understanding of AI\'s internal and external effects on knowledge-worker skills-specifically, how AI complements certain competencies (e.g., technology literacy, ethics, analytical thinking) while potentially\n\nsubstituting others (e.g., basic data tasks, office and financial administration). Following Acemoglu et al. (2021) and Deming and Noray (2020), we relied on job postings-employers\' "footprints" indicating evolving skill demands and wage offers-to analyse around 12 million online vacancies.\n\nOur work illuminates the relationship between AI creation/usage and the complementarity or substitution of knowledge-worker skills, yielding five key contributions. First, we find that AI roles are positively associated with demand for complementary skills and negatively associated with demand for substitutable skills. Second, job postings that include AI requirements display proportionally more requests for complementary skills and fewer requests for substitutable skills compared to non-AI postings. Third, we identify powerful complementarities between particular AI roles and clusters of complementary skills, as well as strong substitution effects for certain AI roles and substitutable skills-most notably an increasing emphasis on ethics across many AI categories. Fourth, we show that AI jobs demanding substitutable skills carry lower salaries than AI jobs without such requirements; basic data skills, customer service, and office/financial administration skills in computer vision and image processing roles suffer the highest wage penalty. However, we find no evidence of a wage premium for complementary skills. Finally, we uncover external complementation effects: as AI roles grow, the number of non-AI roles that demand complementary skills also rises. Crucially, the complementarity effect exceeds the substitution effect.\n\nFuture research directions include extending our analysis to other regions (e.g., Europe and Asia) to capture potential geographic variations, employing qualitative methods (such as interviews with recruitment managers) to explore perceptions of skill demand and valuation, and pursuing experimental or longitudinal studies to establish causality. As debates on the benefits and risks of "AI at work" (Brynjolfsson et al., 2023) persist, researchers, policymakers, employers, and job-seekers all stand to benefit from an empirically grounded understanding of these influential effects.
```
Output:::
Query: What impact does AI have on the demand for human skills?
Answer: AI alters skill demand by increasing the need for competencies such as technology literacy, ethics, and analytical thinking while reducing the reliance on tasks like basic data processing and administrative work. Job postings requiring AI skills tend to emphasize complementary skills and downplay substitutable ones.


Example 3:
Markdown text:
```
# Generalized Gaussian Model for Learned Image Compression \n\nHaotian Zhang, Li Li, Member, IEEE, and Dong Liu, Senior Member, IEEE
## I. INTRODUCTION\n\nImage compression is one of the most fundamental problems in image processing and information theory. Over the past four decades, many researchers have worked on developing and optimizing image compression codecs. Most image compression codecs follow the transform coding scheme [1], where images are transformed to a latent space for decorrelation, followed by quantization and entropy coding. In traditional image compression codecs, such as JPEG [2], JPEG2000 [3], BPG, and VVC [4], different modules are artificially designed and separately optimized.\n\nIn recent years, learned image compression methods have achieved superior performance by exploiting the advantages of deep neural networks. In contrast to traditional approaches, learned image compression [5] optimizes different modules in an end-to-end manner. A typical learned image compression method involves an analysis transform, synthesis transform, quantizer, and entropy model. First, the image is transformed into a latent representation through the analysis transform, and then the latent is quantized for digital transmission. The\n\n[^0]discrete latent is then losslessly coded by the entropy model to further reduce its size. Finally, the synthesis transform reconstructs an image from the discrete latent. These modules are jointly optimized to minimize the rate-distortion cost during training.\n\nIn learned image compression, the probabilistic model is part of the entropy model and is essential in characterizing the distribution of latent variables. The degree of matching between the probabilistic model and the actual distribution of latent variables significantly influences the bitrate of compressed images. A more precise probabilistic model can reduce the bitrate. Probabilistic models with more parameters can fit the distribution of latent variables more precisely, but the corresponding complexity will also be higher. In [6], a zeromean Gaussian scale model is used. The scale parameters are estimated based on side information. In [7], the probabilistic model is extended to the Gaussian Model (GM) with mean and scale parameters. Some studies further propose mixture probabilistic models, such as the Gaussian Mixture Model (GMM) with 9 parameters [8] for more accurate distribution modeling. These mixture models improve compression performance compared to the Gaussian model while introducing more parameters that need to be estimated and higher complexity.
```
Output:::
Query: Why is probabilistic modeling important in image compression?
Answer: It helps characterize the distribution of latent variables, which directly influences the bitrate of compressed images. A more accurate probabilistic model can reduce the bitrate by better approximating the true distribution of the latent space.


The examples only provided one query and answer each, but you must provide 5 different queries and answers in the following format:
Query 1: (your abstractive query)
Answer 1: (your answer)
Query 2: (your abstractive query)
Answer 2: (your answer)
...
Query 5: (your abstractive query)
Answer 5: (your answer)

Remember,
- Your abstractive queries MUST be wh- questions.
- Your abstractive queries MUST be realistic search queries users ask without assuming knowledge of the specific text.
- Your abstractive queries MUST avoid the authors, publication date, references, tables, images, or any other meta-information.

Now, provide your abstractive queries and answers based on the markdown text:
Markdown text:
```
{title}
{text}
```
Output:::
"""

KEYWORD_INSTRUCTION = """You are Search Query Simulator that models how people search for information. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any documents yet. Your task is to simulate 3 keyword queries and their answers for the given markdown text that users would type BEFORE finding any relevant documents.

Here are some example keyword queries based on their markdown text:

Example 1:
Markdown text:
```
Any treatment of multiple sclerosis should preserve mental function, considering how cognitive deterioration interferes with quality of life. However, mental assessment is still realized with neuro-psychological tests without monitoring cognition on neurobiological grounds whereas the ongoing neural activity is readily observable and readable.\nObjectives: The proposed method deciphers electrical brain states which as multi-dimensional cognetoms quantitatively discriminate normal from pathological patterns in an EEG.\nMethods: Baseline recordings from a prior EEG study of 93 subjects, 37 with MS, were analyzed. Spectral bands served to compute cognetoms and categorize subsequent feature combination sets.\nResults: A significant correlation arose between brain states predictors, clinical data and disease duration. Using cognetoms and spectral bands, a cross-sectional comparison separated patients from controls with a precision of $82 \\%$ while using bands alone arrived at $64 \\%$.\nConclusions: Brain states analysis successfully distinguishes controls from patients with MS. The congruity with disease duration is a neurobiological indicator for disease accumulation over time. Our results imply that data-driven comparisons of EEG data may complement customary diagnostic methods in neurology and psychiatry. However, thinking ahead for quantitative monitoring of disease time course and treatment efficacy, we hope to have established the analytic principles applicable to longitudinal clinical studies.
```
Output:::
- multiple sclerosis
- EEG
- brain states analysis

Example 2:
Markdown text:
```
# Investigation about a statement equivalent to Riemann Hypothesis (RH) \n\nGiovanni Lodone
## ABSTRACT\n\nWe try to approach a known equivalence to RH involving relative maxima and minima of $\\xi(s)$ on critical line by a representation of the derivative of the phase of $\\xi(s)$ with respect to imaginary coordinate that involves directly Euler product. In this attempt it is found an object conjectured to be, almost everywhere, the converging \"spectrum\" of prime numbers. Reasons and consequences of the conjecture are highlighted.\n\nMSC-Class : 11M06, 11M99
```
Output:::
- Riemann hypothesis
- Prime numbers
- Euler product

Example 3:
Markdown text:
```
We propose a mathematical kinetic framework to investigate interactions between tumor cells and the immune system, focusing on the spatial dynamics of tumor progression and immune responses. We develop two kinetic models: one describes a conservative scenario where immune cells switch between active and passive states without proliferation, while the other incorporates immune cell proliferation and apoptosis. By considering specific assumptions about the microscopic processes, we derive macroscopic systems featuring linear diffusion, nonlinear cross-diffusion, and nonlinear self-diffusion. Our analysis provides insights into equilibrium configurations and stability, revealing clear correspondences among the macroscopic models derived from the same kinetic framework. Using dynamical systems theory, we examine the stability of equilibrium states and conduct numerical simulations to validate our findings. These results highlight the significance of spatial interactions in tumor-immune dynamics, paving the way for a structured exploration of therapeutic strategies and further investigations into immune responses in various pathological contexts.
```
Output:::
- Tumor-Immune dynamics
- Kinetic models
- Dynamical system theory

Now, provide your keyword queries based on the markdown text:
Markdown text:
```
{title}
{text}
```
Output:::
"""

TABLE_INSTRUCTION = "\n- Tables are represented in the Markdown format. You should simulate at least 1 realistic search query about the tables without assuming prior knowledge."

IMAGE_INSTRUCTION = "\n- Images mentioned in the Markdown text are attached at the end. You should simulate at least 1 realistic search query about the images without assuming prior knowledge."

POST_FILTERING_INSTRUCTION = """You are an evaluator analyzing search queries for their suitability in an information retrieval system, like search engine or RAG. Your task is to determine if the provided query is a valid retrieval query instead of a QA query conditioned on the prior knowledge of a document. A valid retrieval query represents a genuine information need a user might have before seeing any specific document. It stands alone and makes sense without the context of a particular document. A user would plausibly type this query into a retrieval system to seek information on a topic. On the other hand, a document-conditioned QA query assumes the user is looking at a specific document and often refers explicitly or implicitly to the context of that document (e.g., "in this paper," "according to the study," "the authors," uses acronyms defined only within the document).

Here are some examples of how to validate the queries:
Example 1:
Query: Is the Borda voting method manipulable by neural networks with limited information?
Validity: Yes

Example 2:
Query: What impact does AI have on the demand for human skills?
Validity: Yes

Example 3:
Query: What are the eight preferential voting methods in the paper?
Validity: No

Example 4:
Query: What methodology was used in section 3?
Validity: No

Example 5:
Query: Explain Generalized Gaussian model in image compression
Validity: Yes

Example 6:
Query: Explain Generalized Gaussian model in image compression according to the table
Validity: No

Your turn:
Query: {query}
Validity:"""
