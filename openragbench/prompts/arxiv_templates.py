###### GENERATION PROMPTS ######
# SINGLE MODALITY
TEXT_EXTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of documents. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any documents yet. Specifically, your task is to simulate 5 extractive queries and their answers for the given markdown text that users would type BEFORE finding any relevant documents. Here are your guidelines:
- An extractive query (or factoid query) is a question that seeks a concise, fact-based answer extracted from a given text, rather than requiring reasoning or synthesis. It MUST be answerable with a specific, concise piece of factual information from the given text.
- Your extractive queries MUST consist of both wh- questions and yes/no questions.
- Your extractive queries MUST be realistic search queries users ask without assuming knowledge of the specific text.
- Your extractive queries MUST avoid the authors, publication date, references, tables, images, or any other meta-information.

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
- Your extractive queries MUST avoid the authors, publication date, references, tables, images, or any other meta-information.

Now, provide your extractive queries and answers based on the markdown text.
Markdown text:
```
{title}
{text}
```
Output:::
"""

TEXT_ABSTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of documents. Here's the information search process:
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
# Complement or substitute? How AI increases the demand for human skills
# Conclusion \n\nThis study aimed to expand our understanding of AI\'s internal and external effects on knowledge-worker skills-specifically, how AI complements certain competencies (e.g., technology literacy, ethics, analytical thinking) while potentially\n\nsubstituting others (e.g., basic data tasks, office and financial administration). Following Acemoglu et al. (2021) and Deming and Noray (2020), we relied on job postings-employers\' "footprints" indicating evolving skill demands and wage offers-to analyse around 12 million online vacancies.\n\nOur work illuminates the relationship between AI creation/usage and the complementarity or substitution of knowledge-worker skills, yielding five key contributions. First, we find that AI roles are positively associated with demand for complementary skills and negatively associated with demand for substitutable skills. Second, job postings that include AI requirements display proportionally more requests for complementary skills and fewer requests for substitutable skills compared to non-AI postings. Third, we identify powerful complementarities between particular AI roles and clusters of complementary skills, as well as strong substitution effects for certain AI roles and substitutable skills-most notably an increasing emphasis on ethics across many AI categories. Fourth, we show that AI jobs demanding substitutable skills carry lower salaries than AI jobs without such requirements; basic data skills, customer service, and office/financial administration skills in computer vision and image processing roles suffer the highest wage penalty. However, we find no evidence of a wage premium for complementary skills. Finally, we uncover external complementation effects: as AI roles grow, the number of non-AI roles that demand complementary skills also rises. Crucially, the complementarity effect exceeds the substitution effect.\n\nFuture research directions include extending our analysis to other regions (e.g., Europe and Asia) to capture potential geographic variations, employing qualitative methods (such as interviews with recruitment managers) to explore perceptions of skill demand and valuation, and pursuing experimental or longitudinal studies to establish causality. As debates on the benefits and risks of "AI at work" (Brynjolfsson et al., 2023) persist, researchers, policymakers, employers, and job-seekers all stand to benefit from an empirically grounded understanding of these influential effects.
```
Output:::
Query: What impact does AI have on the demand for human skills?
Answer: AI alters skill demand by increasing the need for competencies such as technology literacy, ethics, and analytical thinking while reducing the reliance on tasks like basic data processing and administrative work. Job postings requiring AI skills tend to emphasize complementary skills and downplay substitutable ones.


Example 3:
Markdown text:
```
# Generalized Gaussian Model for Learned Image Compression
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

TABLE_EXTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of tables. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any table yet. Specifically, your task is to simulate 5 extractive queries and their answers for the given markdown table that users would type BEFORE retrieving any relevant table. Here are your guidelines:
- An extractive query (or factoid query) is a question that seeks a concise, fact-based answer extracted from a given table, rather than requiring reasoning or synthesis. It MUST be answerable with a specific, concise piece of factual information from the given table.
- Your extractive queries MUST consist of both wh- questions and yes/no questions.
- Your extractive queries MUST be realistic search queries users ask without assuming knowledge of the specific table.

You must provide 5 different queries and answers in the following format:
Query 1: (your extractive query)
Answer 1: (your answer)
Query 2: (your extractive query)
Answer 2: (your answer)
...
Query 5: (your extractive query)
Answer 5: (your answer)

The table belongs to a document titled '# {title}'. Now, provide your extractive queries and answers based on the markdown tables:
Markdown table:
```
{table}
```
Output:::
"""

TABLE_ABSTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of tables. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any table yet. Specifically, your task is to simulate 5 abstractive queries and their answers for the given markdown table that users would type BEFORE retrieving any relevant table. Here are your guidelines:
- An abstractive query (or generalized query) is a general question that requires generating a summary or rephrased response using understanding and synthesis, rather than directly extracting exact words from a given table.
- Your abstractive queries MUST be wh- questions.
- Your abstractive queries MUST be realistic search queries users ask without assuming knowledge of the specific table.

You must provide 5 different queries and answers in the following format:
Query 1: (your abstractive query)
Answer 1: (your answer)
Query 2: (your abstractive query)
Answer 2: (your answer)
...
Query 5: (your abstractive query)
Answer 5: (your answer)

The table belongs to a document titled '# {title}'. Now, provide your abstractive queries and answers based on the markdown tables:
Markdown table:
```
{table}
```
Output:::
"""

IMAGE_EXTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of images. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any image yet. Specifically, your task is to simulate 5 extractive queries and their answers for the given image that users would type BEFORE retrieving any relevant image. Here are your guidelines:
- An extractive query (or factoid query) is a question that seeks a concise, fact-based answer extracted from a given image, rather than requiring reasoning or synthesis. It MUST be answerable with a specific, concise piece of factual information from the given image.
- Your extractive queries MUST consist of both wh- questions and yes/no questions.
- Your extractive queries MUST be realistic search queries users ask without assuming knowledge of the specific image.

You must provide 5 different queries and answers in the following format:
Query 1: (your extractive query)
Answer 1: (your answer)
Query 2: (your extractive query)
Answer 2: (your answer)
...
Query 5: (your extractive query)
Answer 5: (your answer)

The image belongs to a document titled '# {title}'. Now, provide your extractive queries and answers based on the images:
"""

IMAGE_ABSTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of images. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any image yet. Specifically, your task is to simulate 5 abstractive queries and their answers for the given image that users would type BEFORE retrieving any relevant image. Here are your guidelines:
- An abstractive query (or generalized query) is a general question that requires generating a summary or rephrased response using understanding and synthesis, rather than directly extracting exact words from a given image.
- Your abstractive queries MUST be wh- questions.
- Your abstractive queries MUST be realistic search queries users ask without assuming knowledge of the specific image.

You must provide 5 different queries and answers in the following format:
Query 1: (your abstractive query)
Answer 1: (your answer)
Query 2: (your abstractive query)
Answer 2: (your answer)
...
Query 5: (your abstractive query)
Answer 5: (your answer)

The image belongs to a document titled '# {title}'. Now, provide your abstractive queries and answers based on the images:
"""

# MULTI MODALITY
CONTEXT_SUMMARIZATION_INSTRUCTION = """Your task is to summarize the context of a passage around the table and/or image placeholders. The placeholders have the format of `![placeholder_id](placeholder_id)`. The context is the text surrounding the placeholders, and it may contain crucial information about the table or image. Your summary should capture such information in the context. Your summary should be concise and informative, providing a clear understanding of the content without needing to refer to the table or image itself. The summary should be in a single paragraph and should not include any references to the placeholders or their content.

You must ONLY output the summary content. Avoid writing any additional text or explanations. Avoid writing the "Summary:" prefix.

Passage:
{text}

Summary:
"""

TEXT_TABLE_EXTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of tables. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any tables yet. Specifically, your task is to simulate 5 extractive queries and their answers for the given tables that users would type BEFORE retrieving any relevant tables. Here are your guidelines:
- An extractive query (or factoid query) is a question that seeks a concise, fact-based answer extracted from the given tables, rather than requiring reasoning or synthesis. It MUST be answerable with a specific, concise piece of factual information from the given tables.
- Your extractive queries MUST consist of both wh- questions and yes/no questions.
- Your extractive queries MUST be realistic search queries users ask without assuming knowledge of the specific tables.

You must provide 5 different queries and answers in the following format:
Query 1: (your extractive query)
Answer 1: (your answer)
Query 2: (your extractive query)
Answer 2: (your answer)
...
Query 5: (your extractive query)
Answer 5: (your answer)

Here are the context of the tables:
- Document Title: {title}
- Document Context: {context}
- Markdown tables:
```
{table}
```

Now, provide your extractive queries and answers:
Output:::
"""

TEXT_TABLE_ABSTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of tables. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any tables yet. Specifically, your task is to simulate 5 abstractive queries and their answers for the given tables that users would type BEFORE retrieving any relevant tables. Here are your guidelines:
- An abstractive query (or generalized query) is a general question that requires generating a summary or rephrased response using understanding and synthesis, rather than directly extracting exact wordsquery_type
You must provide 5 different queries and answers in the following format:
Query 1: (your abstractive query)
Answer 1: (your answer)
Query 2: (your abstractive query)
Answer 2: (your answer)
...
Query 5: (your abstractive query)
Answer 5: (your answer)

Here are the context of the tables:
- Document Title: {title}
- Document Context: {context}
- Markdown tables:
```
{table}
```

Now, provide your abstractive queries and answers:
Output:::
"""

TEXT_IMAGE_EXTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of documents with images. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any images yet. Specifically, your task is to simulate 5 extractive queries and their answers for the given images that users would type BEFORE retrieving any relevant images. Here are your guidelines:
- An extractive query (or factoid query) is a question that seeks a concise, fact-based answer extracted from a given document with images, rather than requiring reasoning or synthesis. It MUST be answerable with a specific, concise piece of factual information from the given images.
- Your extractive queries MUST consist of both wh- questions and yes/no questions.
- Your extractive queries MUST be realistic search queries users ask without assuming knowledge of the specific images.

You must provide 5 different queries and answers in the following format:
Query 1: (your extractive query)
Answer 1: (your answer)
Query 2: (your extractive query)
Answer 2: (your answer)
...
Query 5: (your extractive query)
Answer 5: (your answer)

Here are the context of the images:
- Document Title: {title}
- Document Context: {context}

The images are attached below:
"""

TEXT_IMAGE_ABSTRACTIVE_INSTRUCTION = """You are Search Query Simulator that models how people search for information among a set of documents with images. Here's the information search process:
1. User has an information need
2. User types a search query into a search engine
3. User receives relevant search results

You are simulating the queries for Step 2, when users have an information need but haven't seen any images yet. Specifically, your task is to simulate 5 abstractive queries and their answers for the given images that users would type BEFORE retrieving any relevant images. Here are your guidelines:
- An abstractive query (or generalized query) is a general question that requires generating a summary or rephrased response using understanding and synthesis, rather than directly extracting exact words from the given images.
- Your abstractive queries MUST be wh- questions.
- Your abstractive queries MUST be realistic search queries users ask without assuming knowledge of the specific images.

You must provide 5 different queries and answers in the following format:
Query 1: (your abstractive query)
Answer 1: (your answer)
Query 2: (your abstractive query)
Answer 2: (your answer)
...
Query 5: (your abstractive query)
Answer 5: (your answer)

Here are the context of the images:
- Document Title: {title}
- Document Context: {context}

The images are attached below:
"""

PROMPT_MAP = {
    "text": {
        "extractive": TEXT_EXTRACTIVE_INSTRUCTION,
        "abstractive": TEXT_ABSTRACTIVE_INSTRUCTION,
    },
    "table": {
        "extractive": TABLE_EXTRACTIVE_INSTRUCTION,
        "abstractive": TABLE_ABSTRACTIVE_INSTRUCTION,
    },
    "image": {
        "extractive": IMAGE_EXTRACTIVE_INSTRUCTION,
        "abstractive": IMAGE_ABSTRACTIVE_INSTRUCTION,
    },
    "text_table": {
        "extractive": TEXT_TABLE_EXTRACTIVE_INSTRUCTION,
        "abstractive": TEXT_TABLE_ABSTRACTIVE_INSTRUCTION,
    },
    "text_image": {
        "extractive": TEXT_IMAGE_EXTRACTIVE_INSTRUCTION,
        "abstractive": TEXT_IMAGE_ABSTRACTIVE_INSTRUCTION,
    },
}

###### EVALUATION PROMPTS ######
STYLE_VALIDATION_INSTRUCTION = """You are an evaluator analyzing search queries for their suitability in an information retrieval system, like search engine or RAG. Your task is to determine if the provided query is a valid retrieval query instead of a QA query conditioned on the prior knowledge of a document. A valid retrieval query represents a genuine information need a user might have before seeing any specific document. It stands alone and makes sense without the context of a particular document. A user would plausibly type this query into a retrieval system to seek information on a topic. On the other hand, a document-conditioned QA query assumes the user is looking at a specific document and often refers explicitly or implicitly to the context of that document (e.g., "in this paper," "according to the study," "the authors," uses acronyms defined only within the document).

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

TYPE_VALIDATION_INSTRUCTION = """You are an evaluator of query types in an information retrieval system. Your task is to classify whether the query is extractive or abstractive.
- An extractive query (or factoid query) is a question that seeks a concise, fact-based answer, rather than requiring reasoning or synthesis. It MUST be answerable with a specific, concise piece of factual information.
- An abstractive query (or generalized query) is a general question that requires generating a summary or rephrased response using understanding and synthesis, rather than directly extracting exact words from a certain document.
- All "yes/no" queries are considered extractive queries.

Here are some examples:
Example 1:
Query: Is the Borda voting method manipulable by neural networks with limited information?
Type: Extractive

Example 2:
Query: How long does the SERS-AST methodology take to determine MIC values?
Type: Extractive

Example 3:
Query: How does uncertainty in data affect standard quadratic optimization problems?
Type: Abstractive

Example 4:
Query: How can neural networks assess the susceptibility of voting methods to manipulation?
Type: Abstractive

Example 5:
Query: Why is probabilistic modeling important in image compression?
Type: Abstractive

Example 6:
Query: What is the shape of the Doppler spectrum for mobile antenna motion perpendicular to the mean scattering direction?
Type: Extractive

Your turn:
Query: {query}
Type:"""
