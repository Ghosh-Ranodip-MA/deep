"""Synthetic research paper data for seeding the local database."""

SYNTHETIC_PAPERS = [
    {
        "paper_id": "SYN-001", "title": "Deep Learning Approaches for Medical Image Segmentation: A Comprehensive Survey",
        "abstract": "This paper presents a comprehensive survey of deep learning techniques applied to medical image segmentation. We review convolutional neural networks, U-Net architectures, attention mechanisms, and transformer-based models for segmenting anatomical structures in CT, MRI, and X-ray images. Our analysis covers 150+ papers published between 2018-2024, evaluating performance metrics including Dice coefficient, IoU, and Hausdorff distance across multiple organ segmentation tasks. We identify key challenges including limited labeled data, class imbalance, and domain shift, proposing future research directions in few-shot learning and self-supervised pre-training for medical imaging.",
        "authors": [{"name": "Dr. Priya Sharma", "affiliation": "IIT Delhi"}, {"name": "Dr. Rajesh Kumar", "affiliation": "AIIMS Delhi"}],
        "methodology": "Systematic literature review with meta-analysis. Papers collected from PubMed, IEEE Xplore, and ArXiv. Quantitative comparison using standardized benchmarks (ACDC, Synapse, ISIC). Statistical analysis of performance trends across architectures.",
        "year": 2024, "citation_count": 89, "university": "IIT Delhi",
        "journal": "IEEE Transactions on Medical Imaging", "url": "https://example.com/syn001"
    },
    {
        "paper_id": "SYN-002", "title": "Federated Learning for Privacy-Preserving Healthcare Analytics",
        "abstract": "We propose FedHealth, a novel federated learning framework for training machine learning models on distributed electronic health records without sharing raw patient data. Our approach incorporates differential privacy guarantees, secure aggregation protocols, and adaptive client selection to handle non-IID data distributions across hospitals. Experiments on MIMIC-III and eICU datasets demonstrate that FedHealth achieves 94.2% accuracy on mortality prediction while maintaining epsilon-differential privacy of 3.0, outperforming centralized baselines by only 1.8% while ensuring complete data privacy.",
        "authors": [{"name": "Dr. Ankit Patel", "affiliation": "IIT Bombay"}, {"name": "Dr. Sarah Chen", "affiliation": "Stanford University"}],
        "methodology": "Federated optimization using FedAvg with differential privacy noise injection. Communication-efficient gradient compression. Evaluated on 4 hospital nodes with heterogeneous data distributions. Privacy budget analysis using Renyi divergence.",
        "year": 2024, "citation_count": 67, "university": "IIT Bombay",
        "journal": "Nature Digital Medicine", "url": "https://example.com/syn002"
    },
    {
        "paper_id": "SYN-003", "title": "Transformer-Based Natural Language Processing for Legal Document Analysis",
        "abstract": "This research introduces LegalBERT-XL, a domain-specific transformer model pre-trained on 10 million legal documents spanning case law, statutes, and contracts. We fine-tune the model for key legal NLP tasks including contract clause extraction, legal judgment prediction, and statutory interpretation. Our model achieves state-of-the-art results on the LexGLUE benchmark with an average F1 score of 91.3%, significantly outperforming general-purpose language models. We also release a new annotated dataset of 50,000 Indian legal documents for multi-label classification.",
        "authors": [{"name": "Dr. Vikram Singh", "affiliation": "NLU Delhi"}, {"name": "Dr. Meera Iyer", "affiliation": "IIT Madras"}],
        "methodology": "Pre-training with masked language modeling and next sentence prediction on legal corpora. Fine-tuning with task-specific heads. Cross-validation on LexGLUE, CaseHOLD, and custom Indian legal dataset. Ablation studies on model size and pre-training data volume.",
        "year": 2023, "citation_count": 124, "university": "IIT Madras",
        "journal": "ACL Proceedings", "url": "https://example.com/syn003"
    },
    {
        "paper_id": "SYN-004", "title": "Reinforcement Learning for Autonomous Drone Navigation in Urban Environments",
        "abstract": "We present UrbanFly, a deep reinforcement learning system for autonomous drone navigation through complex urban environments with dynamic obstacles. Our approach uses a hierarchical policy architecture combining a high-level path planner with a low-level control policy trained using Proximal Policy Optimization (PPO). The system integrates LiDAR point clouds, RGB camera feeds, and GPS data through a multi-modal fusion network. Simulation experiments in AirSim and real-world tests demonstrate collision-free navigation with 98.7% success rate in environments with moving pedestrians and vehicles.",
        "authors": [{"name": "Dr. Arjun Mehta", "affiliation": "IISc Bangalore"}, {"name": "Dr. Kenji Tanaka", "affiliation": "University of Tokyo"}],
        "methodology": "Hierarchical deep RL with PPO for low-level and options framework for high-level policy. Multi-modal sensor fusion using cross-attention transformers. Trained in AirSim simulator with domain randomization. Real-world validation on DJI Matrice platform in controlled urban environment.",
        "year": 2024, "citation_count": 45, "university": "IISc Bangalore",
        "journal": "IEEE Robotics and Automation Letters", "url": "https://example.com/syn004"
    },
    {
        "paper_id": "SYN-005", "title": "Blockchain-Based Decentralized Identity Management for IoT Ecosystems",
        "abstract": "This paper proposes ChainID, a blockchain-based decentralized identity management system designed for Internet of Things ecosystems. ChainID leverages Ethereum smart contracts and verifiable credentials to enable self-sovereign identity for IoT devices, eliminating single points of failure inherent in centralized PKI systems. Our protocol supports lightweight authentication suitable for resource-constrained devices using zero-knowledge proofs. Evaluation on a testbed of 1,000 simulated IoT devices shows authentication latency under 200ms with 99.99% availability and resistance to Sybil attacks.",
        "authors": [{"name": "Dr. Rohit Gupta", "affiliation": "IIT Kanpur"}, {"name": "Dr. Lisa Wang", "affiliation": "MIT"}],
        "methodology": "Smart contract development on Ethereum with Solidity. Zero-knowledge proof implementation using zk-SNARKs. Performance evaluation on Hyperledger Caliper benchmark. Security analysis against known attack vectors including Sybil, replay, and man-in-the-middle attacks.",
        "year": 2023, "citation_count": 78, "university": "IIT Kanpur",
        "journal": "IEEE Internet of Things Journal", "url": "https://example.com/syn005"
    },
    {
        "paper_id": "SYN-006", "title": "Graph Neural Networks for Drug-Drug Interaction Prediction",
        "abstract": "We introduce DrugGNN, a heterogeneous graph neural network framework for predicting adverse drug-drug interactions. Our model represents drugs as molecular graphs and integrates protein-protein interaction networks, pathway databases, and clinical trial data into a unified heterogeneous information network. Using message-passing neural networks with edge-type-specific attention, DrugGNN achieves an AUROC of 0.967 on the DrugBank DDI dataset, identifying 23 previously unknown critical interactions later validated by pharmacological experts. The framework enables interpretable predictions through attention visualization.",
        "authors": [{"name": "Dr. Neha Agarwal", "affiliation": "IIT Hyderabad"}, {"name": "Dr. James Wilson", "affiliation": "University of Cambridge"}],
        "methodology": "Heterogeneous graph construction from DrugBank, STRING, and KEGG databases. Message-passing with typed attention mechanism. 5-fold cross-validation with temporal split. Expert validation of novel predictions by clinical pharmacologists.",
        "year": 2024, "citation_count": 56, "university": "IIT Hyderabad",
        "journal": "Bioinformatics", "url": "https://example.com/syn006"
    },
    {
        "paper_id": "SYN-007", "title": "Generative Adversarial Networks for Synthetic Data Augmentation in Rare Disease Diagnosis",
        "abstract": "This study addresses the critical challenge of limited training data for rare disease diagnosis by proposing MedGAN-Pro, a progressive growing GAN architecture for generating high-fidelity synthetic medical images. Applied to retinal imaging for rare genetic eye diseases, our approach generates realistic fundus photographs that pass expert ophthalmologist evaluation with 73% indistinguishability rate. Augmenting training sets with synthetic data improves diagnostic model accuracy from 78.3% to 92.1% for rare conditions with fewer than 50 real training samples. We provide rigorous privacy analysis ensuring no patient re-identification risk.",
        "authors": [{"name": "Dr. Sanjay Krishnan", "affiliation": "CMC Vellore"}, {"name": "Dr. Emily Zhang", "affiliation": "Johns Hopkins University"}],
        "methodology": "Progressive growing GAN with spectral normalization. Frechet Inception Distance and expert visual Turing test for quality assessment. Downstream classification using EfficientNet-B4. Membership inference attack analysis for privacy evaluation.",
        "year": 2023, "citation_count": 93, "university": "CMC Vellore",
        "journal": "The Lancet Digital Health", "url": "https://example.com/syn007"
    },
    {
        "paper_id": "SYN-008", "title": "Energy-Efficient Edge Computing for Real-Time Video Analytics",
        "abstract": "We present EdgeVision, an energy-efficient edge computing framework for real-time video analytics that dynamically partitions deep neural network inference between edge devices and cloud servers. Our approach uses neural architecture search to generate device-specific compact models and employs adaptive frame sampling based on scene complexity. Deployed on NVIDIA Jetson platforms, EdgeVision reduces energy consumption by 62% compared to cloud-only processing while maintaining 95.8% accuracy on person detection and tracking tasks. The system processes 30 FPS video streams with end-to-end latency under 50ms.",
        "authors": [{"name": "Dr. Kavitha Raman", "affiliation": "IIT Kharagpur"}, {"name": "Dr. Michael Brown", "affiliation": "University of Melbourne"}],
        "methodology": "Neural architecture search with hardware-aware optimization. Dynamic computation offloading using Lyapunov optimization. Energy profiling on Jetson Xavier NX and Nano. Evaluated on MOT17 and KITTI benchmarks for accuracy; custom energy measurement framework.",
        "year": 2024, "citation_count": 34, "university": "IIT Kharagpur",
        "journal": "ACM Computing Surveys", "url": "https://example.com/syn008"
    },
    {
        "paper_id": "SYN-009", "title": "Attention-Based Models for Multilingual Sentiment Analysis in Social Media",
        "abstract": "This paper presents MultiSent, a cross-lingual sentiment analysis framework that handles code-mixed social media text across 12 Indian languages and English. Using a novel language-agnostic attention mechanism built on top of XLM-RoBERTa, MultiSent effectively captures sentiment in posts containing script mixing, transliteration, and slang. Our approach achieves macro-F1 scores of 0.847 on the SAIL 2024 benchmark and 0.891 on our newly released HindiMix dataset. We demonstrate that the attention weights provide interpretable sentiment triggers, making the model suitable for content moderation applications.",
        "authors": [{"name": "Dr. Amit Sharma", "affiliation": "IIIT Hyderabad"}, {"name": "Dr. Deepika Verma", "affiliation": "JNU Delhi"}],
        "methodology": "XLM-RoBERTa fine-tuning with language-agnostic attention layer. Data collection from Twitter and Instagram with crowd-sourced annotation. Evaluation on SAIL, SemEval, and custom HindiMix benchmarks. Interpretability analysis using attention rollout.",
        "year": 2024, "citation_count": 41, "university": "IIIT Hyderabad",
        "journal": "EMNLP Proceedings", "url": "https://example.com/syn009"
    },
    {
        "paper_id": "SYN-010", "title": "Quantum Machine Learning for Optimization in Supply Chain Management",
        "abstract": "We explore the application of quantum computing to solve complex supply chain optimization problems that are intractable for classical computers. Using variational quantum eigensolver (VQE) and Quantum Approximate Optimization Algorithm (QAOA) on IBM quantum hardware, we solve vehicle routing, inventory optimization, and demand forecasting problems. Our hybrid quantum-classical approach achieves near-optimal solutions for problems with up to 50 nodes, demonstrating a 3.2x speedup over classical simulated annealing for constrained routing problems. We also provide a noise mitigation strategy that improves solution quality by 18% on NISQ devices.",
        "authors": [{"name": "Dr. Suresh Nair", "affiliation": "IIT Roorkee"}, {"name": "Dr. Anna Mueller", "affiliation": "ETH Zurich"}],
        "methodology": "QAOA implementation on IBM Qiskit with error mitigation using zero-noise extrapolation. Classical baseline comparison using Google OR-Tools and simulated annealing. Benchmarked on standard CVRP instances (Augerat Set A). Noise analysis on IBM Brisbane 127-qubit processor.",
        "year": 2024, "citation_count": 28, "university": "IIT Roorkee",
        "journal": "Quantum Science and Technology", "url": "https://example.com/syn010"
    },
    {
        "paper_id": "SYN-011", "title": "Self-Supervised Learning for Speech Recognition in Low-Resource Languages",
        "abstract": "We address the challenge of building automatic speech recognition systems for low-resource Indian languages by leveraging self-supervised learning. Our model, IndicWav2Vec, is pre-trained on 10,000 hours of unlabeled speech data spanning 22 scheduled Indian languages and fine-tuned with as few as 1 hour of labeled data per language. IndicWav2Vec achieves word error rates of 15.3% for Hindi, 19.7% for Tamil, and 22.1% for Assamese, representing relative improvements of 35-45% over previous best systems. We release the pre-trained model and a new benchmark dataset covering all 22 languages.",
        "authors": [{"name": "Dr. Raghav Mittal", "affiliation": "IIT Guwahati"}, {"name": "Dr. Pallavi Deshpande", "affiliation": "Microsoft Research India"}],
        "methodology": "Wav2Vec 2.0 architecture with contrastive learning objective. Pre-training on All India Radio archives and YouTube. Fine-tuning with CTC loss. Evaluation using WER on Mozilla Common Voice and custom IndicSpeech benchmark.",
        "year": 2023, "citation_count": 112, "university": "IIT Guwahati",
        "journal": "Interspeech Proceedings", "url": "https://example.com/syn011"
    },
    {
        "paper_id": "SYN-012", "title": "Explainable AI for Credit Risk Assessment in Emerging Markets",
        "abstract": "This paper introduces FairCredit, an explainable AI framework for credit risk assessment specifically designed for emerging markets where traditional credit scores are unavailable for a majority of the population. Our approach combines gradient-boosted decision trees with SHAP-based explanations and fairness constraints to prevent discrimination based on gender, caste, and geography. Tested on datasets from 3 Indian microfinance institutions covering 500,000 loan applications, FairCredit reduces default prediction error by 23% compared to traditional scorecards while maintaining demographic parity within 5%. Each decision is accompanied by a human-readable explanation compliant with RBI guidelines.",
        "authors": [{"name": "Dr. Pooja Bhandari", "affiliation": "ISB Hyderabad"}, {"name": "Dr. Robert Kim", "affiliation": "Wharton School"}],
        "methodology": "LightGBM with fairness-aware regularization. SHAP for local and global explanations. Bias audit using demographic parity and equalized odds metrics. A/B testing with microfinance loan officers for explanation utility assessment.",
        "year": 2023, "citation_count": 87, "university": "ISB Hyderabad",
        "journal": "Journal of Financial Economics", "url": "https://example.com/syn012"
    },
    {
        "paper_id": "SYN-013", "title": "Vision Transformers for Satellite Image Analysis and Crop Yield Prediction",
        "abstract": "We present AgriViT, a vision transformer architecture optimized for multi-spectral satellite image analysis to predict crop yields at district level across India. Our model processes Sentinel-2 time-series imagery and integrates weather data, soil maps, and historical yield records through a cross-modal attention mechanism. AgriViT achieves R-squared of 0.89 for wheat and 0.84 for rice yield prediction, outperforming CNN baselines by 12% and traditional remote sensing indices by 31%. Deployed in collaboration with the Indian Agriculture Ministry, the system provides 2-month advance yield forecasts for 640 districts.",
        "authors": [{"name": "Dr. Manish Tiwari", "affiliation": "IIT BHU"}, {"name": "Dr. Sunita Rao", "affiliation": "ISRO Ahmedabad"}],
        "methodology": "Vision Transformer with temporal positional encoding for satellite time-series. Cross-modal attention for weather-image fusion. Transfer learning from ImageNet-21K. District-level validation against government yield statistics (2018-2023).",
        "year": 2024, "citation_count": 52, "university": "IIT BHU",
        "journal": "Remote Sensing of Environment", "url": "https://example.com/syn013"
    },
    {
        "paper_id": "SYN-014", "title": "Adversarial Robustness of Large Language Models in Cybersecurity Applications",
        "abstract": "This paper systematically evaluates the adversarial robustness of large language models deployed in cybersecurity contexts including malware classification, phishing detection, and vulnerability analysis. We propose CyberAttack, a framework of 15 novel adversarial attack strategies specifically targeting LLM-based security tools, including semantic-preserving code mutations, prompt injection attacks, and evasion through obfuscation. Our experiments on GPT-4, Llama-3, and Claude reveal that even state-of-the-art models suffer 28-45% accuracy degradation under targeted attacks. We propose CyberShield, a defense mechanism using adversarial training and input sanitization that recovers 80% of lost accuracy.",
        "authors": [{"name": "Dr. Karthik Sundaram", "affiliation": "IIT Madras"}, {"name": "Dr. Elena Popova", "affiliation": "Technical University of Munich"}],
        "methodology": "Systematic adversarial attack generation using gradient-based and black-box methods. Evaluation on VirusTotal, PhishTank, and CVE databases. Defense via adversarial training with PGD attacks and input preprocessing pipeline. Red-team evaluation with cybersecurity professionals.",
        "year": 2024, "citation_count": 73, "university": "IIT Madras",
        "journal": "USENIX Security Proceedings", "url": "https://example.com/syn014"
    },
    {
        "paper_id": "SYN-015", "title": "Multi-Agent Reinforcement Learning for Traffic Signal Control in Indian Cities",
        "abstract": "We develop SmartSignal, a multi-agent reinforcement learning system for adaptive traffic signal control optimized for the heterogeneous and chaotic traffic conditions of Indian cities. Unlike western traffic systems, Indian traffic involves mixed vehicle types, lane discipline violations, and pedestrian interactions. Our approach uses a decentralized execution with centralized training paradigm, where each intersection agent learns cooperative policies through a shared value decomposition network. Deployed at 15 intersections in Bangalore, SmartSignal reduces average waiting time by 37% and fuel consumption by 22% compared to fixed-cycle controllers.",
        "authors": [{"name": "Dr. Vivek Sharma", "affiliation": "IISc Bangalore"}, {"name": "Dr. Arun Nair", "affiliation": "NUS Singapore"}],
        "methodology": "QMIX-based multi-agent RL with custom reward shaping for Indian traffic. Microscopic traffic simulation using SUMO with calibrated Indian traffic parameters. Real-world deployment with adaptive phase timing. Before-after study with GPS trajectory data from Uber Movement.",
        "year": 2023, "citation_count": 65, "university": "IISc Bangalore",
        "journal": "Transportation Research Part C", "url": "https://example.com/syn015"
    },
    {
        "paper_id": "SYN-016", "title": "Neural Architecture Search for Efficient On-Device Machine Learning",
        "abstract": "This paper presents MobileNAS, an efficient neural architecture search framework that discovers optimal neural network architectures for mobile and IoT deployment. Our search algorithm combines progressive space pruning with hardware-aware latency prediction to find architectures that achieve optimal accuracy-latency trade-offs on ARM and RISC-V processors. MobileNAS discovers architectures achieving 79.2% ImageNet top-1 accuracy with only 3.2ms latency on Snapdragon 888, outperforming MobileNetV3 by 1.8% accuracy with 15% lower latency. The complete search process requires only 8 GPU-hours, making it practical for resource-constrained research groups.",
        "authors": [{"name": "Dr. Ruchi Patel", "affiliation": "IIT Gandhinagar"}, {"name": "Dr. Hiroshi Yamamoto", "affiliation": "Sony Research"}],
        "methodology": "Progressive neural architecture search with hardware-in-the-loop latency measurement. Surrogate predictor using graph neural networks. Search space based on inverted residual blocks with squeeze-excite. Evaluation on ImageNet, COCO detection, and custom on-device benchmark.",
        "year": 2024, "citation_count": 38, "university": "IIT Gandhinagar",
        "journal": "NeurIPS Proceedings", "url": "https://example.com/syn016"
    },
    {
        "paper_id": "SYN-017", "title": "Knowledge Graph Embedding for Scientific Literature Recommendation",
        "abstract": "We present SciKG-Rec, a knowledge graph-based recommendation system for scientific literature that captures fine-grained relationships between papers, authors, institutions, and research topics. Our approach constructs a heterogeneous knowledge graph from citation networks, co-authorship data, and semantic content analysis, then learns entity embeddings using a novel relation-aware graph attention network. Evaluated on datasets from ACL Anthology and PubMed, SciKG-Rec achieves NDCG@10 of 0.721, outperforming collaborative filtering baselines by 28% and content-based methods by 19%. The system particularly excels at recommending interdisciplinary papers bridging multiple research fields.",
        "authors": [{"name": "Dr. Aishwarya Nair", "affiliation": "IIIT Bangalore"}, {"name": "Dr. Thomas Schmidt", "affiliation": "Max Planck Institute"}],
        "methodology": "Knowledge graph construction from DBLP, Semantic Scholar, and OpenAlex APIs. Relation-aware graph attention network for embedding learning. Evaluation using recall, NDCG, and user study with 200 researchers. Cold-start analysis for newly published papers.",
        "year": 2023, "citation_count": 49, "university": "IIIT Bangalore",
        "journal": "WWW Proceedings", "url": "https://example.com/syn017"
    },
    {
        "paper_id": "SYN-018", "title": "Continual Learning for Evolving Malware Detection in Enterprise Networks",
        "abstract": "We address the concept drift problem in malware detection by proposing EvoMal, a continual learning framework that adapts to evolving malware families without catastrophic forgetting of previously learned patterns. Our approach combines elastic weight consolidation with replay buffers curated using a novel threat-relevance sampling strategy. EvoMal maintains detection rates above 96% even after processing 18 months of streaming malware samples from VirusTotal, while baseline models degrade to 71% accuracy. The system integrates with existing SIEM tools and processes 10,000 samples per hour on a single GPU server.",
        "authors": [{"name": "Dr. Dhruv Kapoor", "affiliation": "IIT Kanpur"}, {"name": "Dr. Jennifer Adams", "affiliation": "Georgia Tech"}],
        "methodology": "Elastic weight consolidation with task-specific replay buffers. Feature extraction using static analysis (PE headers, API calls) and dynamic analysis (system call sequences). Temporal evaluation protocol with monthly model updates. Integration testing with Splunk SIEM.",
        "year": 2024, "citation_count": 31, "university": "IIT Kanpur",
        "journal": "IEEE S&P Proceedings", "url": "https://example.com/syn018"
    },
    {
        "paper_id": "SYN-019", "title": "Multimodal Learning for Automated Clinical Report Generation from Medical Images",
        "abstract": "This paper introduces ClinicalGPT-Rad, a multimodal model that generates structured clinical radiology reports from chest X-rays and CT scans. Our architecture combines a medical image encoder pre-trained on 2 million radiographs with a fine-tuned Llama-2 language model through a cross-modal projection layer. The system generates reports with clinically accurate findings, impressions, and recommendations. Evaluated by board-certified radiologists, ClinicalGPT-Rad reports achieve 87.3% clinical accuracy and 0.91 BLEU-4 score, with 62% of reports deemed suitable for clinical use with minor editing. The model also detects 14 critical findings with 95.2% sensitivity.",
        "authors": [{"name": "Dr. Swati Mishra", "affiliation": "PGIMER Chandigarh"}, {"name": "Dr. David Lee", "affiliation": "Mayo Clinic"}],
        "methodology": "Vision encoder using CheXpert-pretrained DenseNet-121. Cross-modal projection with Q-Former adapter. Fine-tuning Llama-2-7B with LoRA on MIMIC-CXR reports. Clinical evaluation by 5 radiologists using a structured rubric. Error analysis categorized by finding type.",
        "year": 2024, "citation_count": 95, "university": "PGIMER Chandigarh",
        "journal": "Nature Medicine", "url": "https://example.com/syn019"
    },
    {
        "paper_id": "SYN-020", "title": "Differential Privacy in Deep Learning: A Practical Framework for Production Systems",
        "abstract": "We present DP-Train, a practical framework for training deep learning models with formal differential privacy guarantees suitable for production deployment. Our framework addresses three key challenges: (1) tighter privacy accounting using Renyi differential privacy composition, (2) adaptive clipping strategies that maintain model utility, and (3) efficient implementation achieving only 2.3x training time overhead compared to non-private training. Applied to recommendation systems at scale with 100M users, DP-Train achieves epsilon=1.0 privacy guarantee while maintaining 97.8% of non-private model accuracy. We open-source the framework with integration for PyTorch and TensorFlow.",
        "authors": [{"name": "Dr. Nikhil Joshi", "affiliation": "IIT Delhi"}, {"name": "Dr. Maria Garcia", "affiliation": "Google Research"}],
        "methodology": "DP-SGD with adaptive per-sample gradient clipping. Privacy accounting using PRV accountant for tight composition. Distributed training with secure aggregation. Benchmark on MovieLens, Amazon Reviews, and production recommendation dataset. Utility-privacy Pareto frontier analysis.",
        "year": 2023, "citation_count": 156, "university": "IIT Delhi",
        "journal": "ICML Proceedings", "url": "https://example.com/syn020"
    },
]
