"""
Programmatic synthetic paper generator.
Generates 1500+ realistic research papers by combining domain templates,
author pools, university pools, methodology templates, and journal names.
"""
import random
import hashlib


UNIVERSITIES = [
    "IIT Delhi", "IIT Bombay", "IIT Madras", "IIT Kanpur", "IIT Kharagpur",
    "IIT Roorkee", "IIT Guwahati", "IIT Hyderabad", "IIT BHU", "IIT Gandhinagar",
    "IIT Indore", "IIT Patna", "IIT Jodhpur", "IIT Tirupati", "IIT Dhanbad",
    "IISc Bangalore", "IIIT Hyderabad", "IIIT Bangalore", "IIIT Delhi",
    "NIT Trichy", "NIT Warangal", "NIT Surathkal", "NIT Calicut", "NIT Rourkela",
    "BITS Pilani", "BITS Goa", "ISB Hyderabad", "CMC Vellore", "PGIMER Chandigarh",
    "JNU Delhi", "Delhi University", "Anna University", "Jadavpur University",
    "Manipal Institute of Technology", "VIT Vellore", "SRM University",
    "Amrita Vishwa Vidyapeetham", "IISER Pune", "IISER Kolkata",
    "MIT", "Stanford University", "Carnegie Mellon University",
    "University of Cambridge", "University of Oxford", "ETH Zurich",
    "University of Toronto", "University of Tokyo", "NUS Singapore",
    "Tsinghua University", "Peking University", "KAIST South Korea",
    "Technical University of Munich", "Max Planck Institute",
    "Georgia Tech", "UC Berkeley", "University of Michigan",
    "Johns Hopkins University", "Harvard University", "Caltech",
    "University of Washington", "Columbia University", "Yale University",
    "Princeton University", "Cornell University", "Brown University",
    "EPFL Switzerland", "Imperial College London", "UCL London",
    "University of Edinburgh", "University of Melbourne",
    "Seoul National University", "Nanyang Technological University",
    "Hong Kong University of Science and Technology",
]

FIRST_NAMES = [
    "Priya", "Rajesh", "Ankit", "Neha", "Vikram", "Meera", "Arjun", "Kavitha",
    "Rohit", "Sunita", "Amit", "Deepika", "Sanjay", "Swati", "Karthik",
    "Pooja", "Manish", "Ruchi", "Vivek", "Aishwarya", "Dhruv", "Pallavi",
    "Suresh", "Raghav", "Nikhil", "Sarah", "James", "Emily", "David",
    "Michael", "Jennifer", "Robert", "Lisa", "Thomas", "Anna", "Elena",
    "Hiroshi", "Kenji", "Wei", "Yuki", "Hassan", "Maria", "Carlos",
    "Ahmed", "Fatima", "Jun", "Mei", "Sven", "Olga", "Pierre",
    "Aarav", "Diya", "Ishaan", "Ananya", "Vihaan", "Saanvi", "Aditi",
    "Kabir", "Zara", "Reyansh", "Tanvi", "Rohan", "Shruti", "Varun",
    "Nisha", "Pranav", "Kriti", "Akash", "Sneha", "Harsh",
]

LAST_NAMES = [
    "Sharma", "Patel", "Kumar", "Singh", "Gupta", "Agarwal", "Iyer",
    "Nair", "Mehta", "Raman", "Krishnan", "Mishra", "Joshi", "Verma",
    "Tiwari", "Bhandari", "Sundaram", "Kapoor", "Mittal", "Rao",
    "Chen", "Wang", "Zhang", "Lee", "Kim", "Wilson", "Brown",
    "Adams", "Garcia", "Mueller", "Schmidt", "Tanaka", "Yamamoto",
    "Popova", "Deshpande", "Thompson", "Anderson", "Martinez", "Taylor",
    "Moore", "Jackson", "White", "Harris", "Clark", "Lewis", "Walker",
    "Banerjee", "Chatterjee", "Mukherjee", "Das", "Roy", "Sen",
    "Reddy", "Menon", "Pillai", "Naidu", "Hegde", "Kulkarni", "Desai",
]
DOMAINS = {
    "deep_learning": {
        "topics": [
            "Convolutional Neural Networks for {app}",
            "Attention Mechanisms in Deep Learning for {app}",
            "Transfer Learning Approaches for {app}",
            "Self-Supervised Learning for {app}",
            "Vision Transformers for {app}",
            "Generative Adversarial Networks for {app}",
            "Neural Architecture Search for {app}",
            "Knowledge Distillation in {app}",
            "Multi-Task Learning for {app}",
            "Few-Shot Learning Approaches to {app}",
            "Contrastive Learning for {app}",
            "Deep Metric Learning for {app}",
            "Diffusion Models for {app}",
            "Foundation Models for {app}",
        ],
        "apps": [
            "Image Classification", "Object Detection", "Semantic Segmentation",
            "Video Understanding", "3D Point Cloud Processing", "Image Generation",
            "Super-Resolution", "Style Transfer", "Action Recognition",
            "Depth Estimation", "Optical Flow Prediction", "Image Captioning",
            "Scene Understanding", "Anomaly Detection", "Face Recognition",
            "Pose Estimation", "Document Analysis", "Remote Sensing",
            "Medical Imaging", "Autonomous Driving Perception",
            "Satellite Image Analysis", "Industrial Quality Inspection",
        ],
        "methods": [
            "ResNet-based backbone with custom classification head. Trained on ImageNet-pretrained weights with fine-tuning. Data augmentation including random crop, horizontal flip, and CutMix. Evaluated using top-1 and top-5 accuracy. 5-fold cross-validation with stratified splits.",
            "Transformer encoder-decoder architecture with multi-head self-attention. Pre-trained using masked image modeling on large-scale unlabeled data. Fine-tuned with supervised learning on task-specific datasets. Ablation studies on attention head count, patch size, and embedding dimension.",
            "Progressive training strategy starting from low resolution and gradually increasing. Spectral normalization for training stability. FID and IS metrics for quality evaluation. User study with 50 participants for perceptual quality assessment.",
            "Meta-learning approach using MAML with task-specific adaptation. Episode-based training with support and query sets. Evaluation on miniImageNet and tieredImageNet benchmarks. Comparison with prototypical networks and matching networks.",
            "Knowledge distillation from large teacher model to compact student model. Temperature-scaled softmax for soft target generation. Feature-level distillation using intermediate layer representations. Latency benchmarking on mobile devices (ARM Cortex-A78).",
            "Denoising diffusion probabilistic model with classifier-free guidance. U-Net backbone with cross-attention for conditional generation. FID, CLIP score, and human evaluation. Comparison with GANs and VAE baselines.",
        ],
        "journals": [
            "IEEE TPAMI", "CVPR Proceedings", "NeurIPS Proceedings",
            "ICCV Proceedings", "ECCV Proceedings", "AAAI Proceedings",
            "Pattern Recognition", "Neural Networks", "Image and Vision Computing",
        ],
    },
    "nlp": {
        "topics": [
            "Large Language Models for {app}",
            "Transformer-Based Approaches to {app}",
            "Cross-Lingual {app}",
            "Prompt Engineering for {app}",
            "Named Entity Recognition in {app}",
            "Text Classification Using {app}",
            "Machine Translation for {app}",
            "Question Answering Systems for {app}",
            "Dialogue Systems for {app}",
            "Abstractive Summarization for {app}",
            "Retrieval-Augmented Generation for {app}",
            "Low-Resource Language Processing for {app}",
            "Instruction Tuning for {app}",
            "Chain-of-Thought Reasoning for {app}",
        ],
        "apps": [
            "Scientific Document Analysis", "Social Media Mining",
            "Legal Text Processing", "Clinical Note Understanding",
            "Code Generation", "Hate Speech Detection",
            "Sentiment Analysis", "Fake News Detection",
            "Multilingual Communication", "Educational Content",
            "Financial Text Analysis", "Conversational AI",
            "Information Extraction", "Knowledge Base Construction",
            "Indian Languages", "Biomedical Text Mining",
            "Patent Analysis", "Academic Writing Assistance",
        ],
        "methods": [
            "BERT-based architecture fine-tuned on domain-specific corpus. Tokenization using WordPiece with domain vocabulary extension. Pre-training with masked language modeling and next sentence prediction. Evaluation on standard NLP benchmarks with macro-F1 and accuracy metrics.",
            "GPT-style autoregressive model with instruction tuning. RLHF training pipeline with human preference data. Evaluated using BLEU, ROUGE-L, and human evaluation scores. Comparison with ChatGPT, Claude, and open-source alternatives.",
            "XLM-RoBERTa backbone for cross-lingual transfer. Zero-shot and few-shot evaluation across 15 languages. Language-agnostic sentence representations. Evaluation on XNLI, XQuAD, and MLQA benchmarks.",
            "Retrieval-augmented generation using dense passage retrieval. Vector database indexing with FAISS. Context window optimization for long documents. Evaluation using faithfulness, relevance, and coherence metrics.",
            "Sequence labeling with BiLSTM-CRF architecture. Character-level embeddings for handling morphologically rich languages. Active learning for efficient annotation. F1-score evaluation with entity-level and token-level metrics.",
            "Chain-of-thought prompting with self-consistency decoding. Multi-step reasoning evaluation on GSM8K and ARC benchmarks. Comparison of zero-shot and few-shot prompting strategies. Error analysis on reasoning failure modes.",
        ],
        "journals": [
            "ACL Proceedings", "EMNLP Proceedings", "NAACL Proceedings",
            "TACL", "Computational Linguistics", "COLING Proceedings",
            "LREC Proceedings", "Journal of NLP", "AI Open",
        ],
    },
    "healthcare_ai": {
        "topics": [
            "Deep Learning for {app}",
            "Federated Learning in {app}",
            "Explainable AI for {app}",
            "Clinical Decision Support Using {app}",
            "Medical Image Analysis for {app}",
            "Natural Language Processing for {app}",
            "Predictive Modeling for {app}",
            "Wearable Sensor Analytics for {app}",
            "Drug Discovery Using {app}",
            "Genomics and {app}",
            "Telemedicine Enhanced by {app}",
            "Mental Health Assessment Using {app}",
            "Multimodal AI for {app}",
        ],
        "apps": [
            "Cancer Detection", "Diabetic Retinopathy Screening",
            "ECG Arrhythmia Classification", "Radiology Report Generation",
            "Pathology Slide Analysis", "Patient Readmission Prediction",
            "Drug-Drug Interaction Prediction", "Clinical Trial Matching",
            "Rare Disease Diagnosis", "Surgical Planning",
            "Epidemic Forecasting", "ICU Mortality Prediction",
            "Mental Health Screening", "Protein Structure Prediction",
            "Medical Chatbot Development", "Sleep Disorder Detection",
            "Skin Lesion Classification", "Brain Tumor Segmentation",
        ],
        "methods": [
            "U-Net architecture with attention gates for medical image segmentation. Trained on multi-center datasets with heterogeneous imaging protocols. Dice coefficient, IoU, and Hausdorff distance for evaluation. Cross-validation with leave-one-center-out strategy.",
            "Federated learning with differential privacy guarantees (epsilon=3.0). Secure aggregation protocol across 10 hospital nodes. Non-IID data handling using FedProx algorithm. Privacy budget tracking using Renyi divergence accounting.",
            "Gradient-boosted trees with SHAP explanations for clinical interpretability. Feature importance analysis using permutation importance and Shapley values. Clinical validation by board-certified physicians. Prospective evaluation on held-out temporal test set.",
            "Multimodal fusion of imaging, lab values, and clinical notes. Cross-attention transformer for modality alignment. Missing modality handling using dropout training. Evaluation on MIMIC-III and eICU-CRD databases.",
            "Graph neural network on molecular interaction networks. Drug representations using SMILES-based molecular fingerprints. Link prediction for novel interaction discovery. Expert validation by clinical pharmacologists.",
            "Transformer-based model pre-trained on 2M clinical notes. Fine-tuned for disease coding, named entity recognition, and relation extraction. Evaluated on n2c2, i2b2, and MIMIC-CXR benchmarks.",
        ],
        "journals": [
            "Nature Medicine", "The Lancet Digital Health", "JAMIA",
            "IEEE Trans Medical Imaging", "Medical Image Analysis",
            "Bioinformatics", "JMIR", "npj Digital Medicine",
            "Radiology: AI", "BMC Medical Informatics",
        ],
    },
    "cybersecurity": {
        "topics": [
            "Machine Learning for {app}",
            "Deep Learning-Based {app}",
            "Adversarial Robustness in {app}",
            "Zero-Day {app}",
            "Network Traffic Analysis for {app}",
            "Blockchain-Based {app}",
            "Privacy-Preserving {app}",
            "Automated {app}",
            "IoT Security Using {app}",
            "Federated {app}",
            "AI-Powered {app}",
        ],
        "apps": [
            "Malware Detection", "Intrusion Detection Systems",
            "Phishing URL Classification", "Vulnerability Assessment",
            "Ransomware Analysis", "DDoS Attack Mitigation",
            "Network Anomaly Detection", "Authentication Systems",
            "Threat Intelligence", "Firmware Analysis",
            "API Security Testing", "Cloud Security Monitoring",
            "Supply Chain Security", "Encrypted Traffic Classification",
            "Deepfake Detection", "Digital Forensics",
        ],
        "methods": [
            "Static and dynamic analysis of PE binaries. Feature extraction from API call sequences, control flow graphs, and opcode n-grams. Ensemble of gradient-boosted trees and deep neural networks. Temporal evaluation with concept drift handling.",
            "CNN-based network traffic classifier operating on raw packet payloads. Trained on CICIDS2017 and CSE-CIC-IDS2018 datasets. Real-time inference at 10 Gbps line rate using GPU acceleration. False positive rate analysis with network operator feedback.",
            "Adversarial training using PGD and FGSM attacks. Input preprocessing pipeline for attack mitigation. Robustness certification using randomized smoothing. Evaluation against AutoAttack benchmark.",
            "Smart contract vulnerability detection using graph neural networks on control flow graphs. Symbolic execution for ground truth generation. Comparison with Mythril, Slither, and Securify tools. False negative analysis on DeFi exploit database.",
            "Differential privacy mechanisms for collaborative threat intelligence sharing. Secure multi-party computation for joint model training. Privacy-utility tradeoff analysis with varying epsilon budgets. Deployment in SOC environment with SIEM integration.",
        ],
        "journals": [
            "USENIX Security", "IEEE S&P", "CCS Proceedings",
            "NDSS Proceedings", "IEEE TDSC", "Computers & Security",
            "Journal of Cybersecurity", "ACM TOPS",
        ],
    },
    "iot_edge": {
        "topics": [
            "Edge Computing for {app}",
            "TinyML Approaches to {app}",
            "Sensor Fusion for {app}",
            "Fog Computing Architecture for {app}",
            "Energy-Efficient {app}",
            "Real-Time {app}",
            "5G-Enabled {app}",
            "Digital Twin for {app}",
            "Edge AI for {app}",
        ],
        "apps": [
            "Smart Agriculture", "Industrial Predictive Maintenance",
            "Autonomous Vehicle Systems", "Smart City Infrastructure",
            "Environmental Monitoring", "Wearable Health Devices",
            "Smart Home Automation", "Supply Chain Tracking",
            "Structural Health Monitoring", "Precision Livestock Farming",
            "Air Quality Monitoring", "Water Quality Assessment",
            "Smart Parking Systems", "Energy Grid Optimization",
        ],
        "methods": [
            "Microcontroller deployment using TensorFlow Lite Micro. Model quantization (INT8) and pruning for memory reduction. Power consumption profiling on ARM Cortex-M4. Over-the-air model update mechanism.",
            "Multi-sensor data fusion using Kalman filtering and deep learning. Edge-cloud computation partitioning using Lyapunov optimization. Latency-accuracy tradeoff analysis. Deployed on NVIDIA Jetson and Raspberry Pi platforms.",
            "Digital twin simulation with physics-informed neural networks. Real-time sensor data ingestion via MQTT protocol. Anomaly detection using autoencoders on time-series data. Validated against 6-month operational dataset from industrial partner.",
            "Federated learning across distributed IoT devices. Communication-efficient gradient compression using Top-K sparsification. Battery-aware client selection strategy. Evaluation on real-world sensor network deployment.",
        ],
        "journals": [
            "IEEE IoT Journal", "ACM Trans on Sensor Networks",
            "IEEE Trans on Industrial Informatics", "Pervasive and Mobile Computing",
            "Journal of Edge Computing", "Sensors (MDPI)",
        ],
    },
    "robotics_cv": {
        "topics": [
            "Reinforcement Learning for {app}",
            "Sim-to-Real Transfer for {app}",
            "Multi-Agent Systems for {app}",
            "SLAM Approaches for {app}",
            "Human-Robot Interaction in {app}",
            "Manipulation Learning for {app}",
            "Autonomous Navigation for {app}",
            "Embodied AI for {app}",
        ],
        "apps": [
            "Drone Navigation", "Warehouse Automation",
            "Surgical Robotics", "Agricultural Robotics",
            "Search and Rescue Operations", "Underwater Exploration",
            "Last-Mile Delivery", "Construction Monitoring",
            "Space Exploration", "Traffic Management",
            "Social Robotics", "Collaborative Assembly",
        ],
        "methods": [
            "Proximal Policy Optimization with hierarchical reward shaping. Sim-to-real transfer using domain randomization in Isaac Gym. Real-world validation on custom robot platform. Safety-constrained exploration with Lagrangian relaxation.",
            "Visual SLAM using ORB features with deep learning-based loop closure detection. LiDAR-camera fusion for robust localization. Evaluation on KITTI, TUM-RGBD, and custom indoor/outdoor sequences. Real-time operation at 30Hz on embedded GPU.",
            "Multi-agent reinforcement learning with centralized training and decentralized execution. Communication protocol learning using graph attention networks. Scalability analysis from 4 to 64 agents. Deployed in simulated and real warehouse environments.",
            "Imitation learning from human demonstrations with DAgger-style correction. Tactile sensor integration for contact-rich manipulation. Force-torque feedback for compliant control. Evaluated on YCB object manipulation benchmark.",
        ],
        "journals": [
            "IEEE Robotics and Automation Letters", "ICRA Proceedings",
            "RSS Proceedings", "Autonomous Robots",
            "International Journal of Robotics Research",
        ],
    },
    "data_science": {
        "topics": [
            "Explainable AI for {app}",
            "AutoML for {app}",
            "Time Series Forecasting for {app}",
            "Causal Inference in {app}",
            "Fairness-Aware Machine Learning for {app}",
            "Graph Analytics for {app}",
            "Anomaly Detection in {app}",
            "Recommendation Systems for {app}",
            "Tabular Data Learning for {app}",
        ],
        "apps": [
            "Financial Risk Assessment", "Customer Churn Prediction",
            "Demand Forecasting", "Fraud Detection",
            "Credit Scoring", "Energy Consumption Prediction",
            "Social Network Analysis", "User Behavior Modeling",
            "Climate Change Modeling", "Workforce Planning",
            "Real Estate Valuation", "Insurance Pricing",
            "Healthcare Cost Prediction", "Retail Analytics",
        ],
        "methods": [
            "XGBoost ensemble with Bayesian hyperparameter optimization. SHAP and LIME for local and global interpretability. Fairness evaluation using demographic parity and equalized odds. A/B testing framework for production deployment.",
            "Temporal convolutional network with seasonal decomposition. Attention-based temporal fusion transformer. Backtesting on 5-year rolling window. Comparison with ARIMA, Prophet, and N-BEATS baselines.",
            "Variational autoencoder for unsupervised anomaly detection. Isolation Forest and Local Outlier Factor baselines. Evaluation on real-world and synthetic anomaly benchmarks. Online learning adaptation for concept drift.",
            "Graph convolutional network on heterogeneous information network. Knowledge graph integration for cold-start handling. Offline evaluation with recall@K and NDCG@K. Online A/B test with 1M users over 4 weeks.",
        ],
        "journals": [
            "KDD Proceedings", "ICML Proceedings", "ICLR Proceedings",
            "Machine Learning Journal", "JMLR", "Data Mining and Knowledge Discovery",
            "IEEE TKDE", "ACM TIST",
        ],
    },
    "quantum_hpc": {
        "topics": [
            "Quantum Machine Learning for {app}",
            "Variational Quantum Algorithms for {app}",
            "Quantum Error Correction for {app}",
            "Hybrid Quantum-Classical {app}",
            "High-Performance Computing for {app}",
            "Distributed Computing for {app}",
        ],
        "apps": [
            "Combinatorial Optimization", "Drug Molecule Simulation",
            "Cryptographic Protocol Design", "Portfolio Optimization",
            "Materials Discovery", "Climate Simulation",
            "Protein Folding", "Supply Chain Optimization",
            "Traffic Flow Optimization", "Scheduling Problems",
        ],
        "methods": [
            "QAOA implementation on IBM 127-qubit processor. Noise mitigation using zero-noise extrapolation and probabilistic error cancellation. Comparison with classical solvers (Gurobi, CPLEX). Scaling analysis from 10 to 50 qubits.",
            "Variational quantum eigensolver with hardware-efficient ansatz. Gradient estimation using parameter-shift rule. Noise-aware training on real quantum hardware. Molecular energy surface comparison with CCSD(T) classical results.",
            "GPU-accelerated tensor network simulation of quantum circuits. Distributed computing using MPI across 256 nodes. Memory-efficient state vector representation. Benchmarking on random circuit sampling instances.",
        ],
        "journals": [
            "Quantum Science and Technology", "Physical Review Letters",
            "Nature Physics", "Quantum", "IEEE Trans on Quantum Engineering",
            "SC Proceedings", "Journal of Parallel Computing",
        ],
    },
    "speech_audio": {
        "topics": [
            "Self-Supervised Learning for {app}",
            "End-to-End Models for {app}",
            "Multi-Modal Learning for {app}",
            "Low-Resource {app}",
            "Real-Time {app}",
            "Robust {app}",
        ],
        "apps": [
            "Speech Recognition", "Speaker Verification",
            "Speech Emotion Recognition", "Music Generation",
            "Sound Event Detection", "Voice Conversion",
            "Speech Enhancement", "Acoustic Scene Classification",
            "Language Identification", "Keyword Spotting",
        ],
        "methods": [
            "Wav2Vec 2.0 pre-training on 10,000 hours of unlabeled audio. CTC and attention-based decoding comparison. Language model integration using shallow fusion. WER evaluation on LibriSpeech, CommonVoice, and custom benchmarks.",
            "Conformer architecture combining convolution and self-attention. Streaming inference with chunk-based processing for real-time operation. Model compression via quantization-aware training. Deployment on mobile devices with ONNX Runtime.",
            "Multi-task learning with shared encoder for joint recognition and emotion detection. Data augmentation using SpecAugment and noise injection. Evaluation on IEMOCAP, RAVDESS, and custom multilingual datasets.",
        ],
        "journals": [
            "Interspeech Proceedings", "ICASSP Proceedings",
            "IEEE/ACM Trans on Audio, Speech, and Language Processing",
            "Speech Communication", "Computer Speech & Language",
        ],
    },
    "sustainability": {
        "topics": [
            "AI-Driven {app}",
            "Machine Learning for {app}",
            "Computer Vision for {app}",
            "Optimization Algorithms for {app}",
            "Predictive Analytics for {app}",
            "Deep Learning for {app}",
        ],
        "apps": [
            "Renewable Energy Forecasting", "Carbon Emission Monitoring",
            "Waste Classification and Recycling", "Water Resource Management",
            "Biodiversity Conservation", "Precision Agriculture",
            "Smart Grid Management", "Deforestation Detection",
            "Air Pollution Prediction", "Sustainable Urban Planning",
            "Electric Vehicle Charging Optimization", "Crop Disease Detection",
        ],
        "methods": [
            "Satellite imagery analysis using multi-spectral vision transformers. Time-series analysis of Sentinel-2 and Landsat data. Ground-truth validation with field surveys across 50 sites. Change detection using Siamese network architecture.",
            "Physics-informed neural networks combining physical models with data-driven learning. Ensemble of weather prediction models for renewable energy forecasting. Evaluation against NWP baselines and persistence models. Real-world deployment at 3 wind farms over 12 months.",
            "YOLOv8-based object detection for waste stream classification. Transfer learning from COCO to custom waste taxonomy with 30 categories. Edge deployment on conveyor belt cameras. Precision-recall analysis at different IoU thresholds.",
            "Reinforcement learning for real-time grid optimization with battery storage. Multi-objective optimization balancing cost, emissions, and reliability. Simulation using IEEE 39-bus test system. Comparison with rule-based and MPC controllers.",
        ],
        "journals": [
            "Nature Sustainability", "Environmental Science & Technology",
            "Applied Energy", "Renewable Energy", "Remote Sensing of Environment",
            "IEEE Trans on Sustainable Energy", "Ecological Modelling",
        ],
    },
    "blockchain_fintech": {
        "topics": [
            "Blockchain-Based {app}",
            "Decentralized Finance Protocols for {app}",
            "Smart Contract Verification for {app}",
            "Consensus Mechanism Optimization for {app}",
            "Tokenization Strategies for {app}",
            "Cross-Chain Interoperability for {app}",
        ],
        "apps": [
            "Digital Payment Systems", "Supply Chain Transparency",
            "Decentralized Identity Management", "Cross-Border Remittances",
            "Insurance Claims Processing", "Trade Finance Automation",
            "Central Bank Digital Currencies", "Asset Tokenization",
            "Peer-to-Peer Lending", "Regulatory Compliance",
            "Anti-Money Laundering", "Microfinance Platforms",
        ],
        "methods": [
            "Ethereum smart contract development with formal verification using Certora Prover. Gas optimization analysis across EVM-compatible chains. Security audit against known vulnerability patterns. Performance benchmarking on Polygon and Arbitrum L2 networks.",
            "Consensus protocol comparison (PoS, DPoS, PBFT) with throughput and finality analysis. Network simulation with up to 1000 validator nodes. Byzantine fault tolerance evaluation under adversarial conditions. Energy consumption comparison with proof-of-work baselines.",
            "Zero-knowledge proof circuits implemented using Circom and SnarkJS. Privacy-preserving transaction verification benchmarked on Zcash protocol. Proof generation time and verification overhead analysis. Integration with existing DeFi liquidity pools.",
            "Machine learning on blockchain transaction graphs for fraud detection. Temporal graph neural networks for anomaly identification. Evaluation on Ethereum and Bitcoin mainnet datasets. Real-time monitoring pipeline with sub-second alert generation.",
        ],
        "journals": [
            "IEEE Blockchain", "Financial Cryptography Proceedings",
            "Ledger Journal", "Frontiers in Blockchain",
            "Journal of Financial Technology", "ACM DLT",
        ],
    },
    "climate_ai": {
        "topics": [
            "Climate Modeling with {app}",
            "Weather Prediction Using {app}",
            "Environmental Monitoring through {app}",
            "Disaster Prediction with {app}",
            "Ocean Analytics Using {app}",
            "Atmospheric Science and {app}",
        ],
        "apps": [
            "Extreme Weather Forecasting", "Sea Level Rise Prediction",
            "Wildfire Spread Modeling", "Glacier Retreat Analysis",
            "Coral Reef Health Monitoring", "Flood Risk Assessment",
            "Drought Prediction", "Urban Heat Island Mapping",
            "Carbon Capture Optimization", "Ecosystem Service Valuation",
            "Methane Emission Detection", "Permafrost Thaw Prediction",
        ],
        "methods": [
            "Graph neural network on global climate observation network. Spatio-temporal attention for multi-resolution climate data. Evaluation against CMIP6 model ensemble. Uncertainty quantification using Monte Carlo dropout and deep ensembles.",
            "Physics-informed neural network constrained by Navier-Stokes equations. Multi-scale temporal modeling from hourly to decadal timescales. Validation against ERA5 reanalysis data. Skill score comparison with ECMWF operational forecasts.",
            "Satellite image time-series analysis using temporal vision transformers. Change detection in Sentinel-1 SAR and Sentinel-2 optical data. Ground-truth validation with in-situ sensor networks. Assessment of model generalization across geographic regions.",
            "Reinforcement learning for adaptive climate intervention strategies. Multi-objective optimization balancing temperature reduction and ecological impact. Coupled earth system model integration. Policy evaluation under multiple emission scenarios (SSP1-5).",
        ],
        "journals": [
            "Nature Climate Change", "Geophysical Research Letters",
            "Journal of Climate", "Earth System Science Data",
            "Environmental Research Letters", "Climate Dynamics",
        ],
    },
    "education_tech": {
        "topics": [
            "AI-Powered {app}",
            "Adaptive Learning Systems for {app}",
            "Learning Analytics for {app}",
            "Intelligent Tutoring for {app}",
            "Gamification Strategies for {app}",
            "Personalized Education Using {app}",
        ],
        "apps": [
            "Student Performance Prediction", "Automated Essay Scoring",
            "MOOC Completion Prediction", "Adaptive Quiz Generation",
            "Plagiarism Detection", "Learning Path Optimization",
            "Student Engagement Detection", "Question Generation",
            "Knowledge Tracing", "Peer Assessment Automation",
            "Special Education Support", "STEM Learning Enhancement",
        ],
        "methods": [
            "Knowledge tracing using deep learning on student interaction sequences. Transformer-based model capturing temporal learning patterns. Evaluation on EdNet and ASSISTments datasets. A/B testing with 5000 students across 3 universities.",
            "Natural language processing for automated essay grading. Multi-trait rubric scoring using hierarchical attention networks. Agreement analysis with human raters using quadratic weighted kappa. Bias analysis across demographic groups.",
            "Multi-armed bandit for adaptive content recommendation. Contextual bandit incorporating student knowledge state and learning style. Regret analysis and comparison with epsilon-greedy and UCB baselines. Deployed in production LMS with 10K active learners.",
            "Computer vision for student engagement detection from webcam feeds. Facial action unit analysis combined with eye-tracking data. Privacy-preserving on-device inference. Validation against self-reported engagement surveys.",
        ],
        "journals": [
            "Computers & Education", "LAK Proceedings",
            "British Journal of Educational Technology",
            "International Journal of AI in Education",
            "IEEE Trans on Learning Technologies", "AIED Proceedings",
        ],
    },
    "bioinformatics": {
        "topics": [
            "Deep Learning for {app}",
            "Graph Neural Networks in {app}",
            "Transformer Models for {app}",
            "Multi-Omics Integration for {app}",
            "AI-Driven {app}",
            "Machine Learning Approaches to {app}",
        ],
        "apps": [
            "Protein Structure Prediction", "Gene Expression Analysis",
            "Drug Target Identification", "Single-Cell RNA Sequencing",
            "Genome-Wide Association Studies", "Metagenomics Analysis",
            "Protein-Protein Interaction Prediction", "Variant Calling",
            "Epigenomics Data Analysis", "Metabolic Pathway Modeling",
            "Antibody Design", "Cancer Genomics",
        ],
        "methods": [
            "Equivariant neural network for 3D protein structure prediction. SE(3)-invariant message passing on atomic coordinate graphs. Evaluation on CASP15 targets with GDT-TS and TM-score metrics. Comparison with AlphaFold2 and RoseTTAFold baselines.",
            "Variational autoencoder for single-cell RNA-seq data integration. Batch effect correction using adversarial training. Cell type annotation using semi-supervised learning. Benchmarked on Human Cell Atlas datasets across 5 tissues.",
            "Graph attention network on protein-protein interaction network. Edge features encoding biochemical properties and co-expression patterns. Link prediction evaluated with AUROC and AUPRC. Novel interaction predictions validated via co-immunoprecipitation experiments.",
            "Multi-omics data fusion using cross-modal attention transformers. Integration of genomics, transcriptomics, and proteomics data. Patient stratification for precision medicine. Evaluated on TCGA pan-cancer cohort with survival analysis.",
        ],
        "journals": [
            "Nature Biotechnology", "Genome Biology", "Bioinformatics",
            "Nucleic Acids Research", "Cell Systems", "PLOS Computational Biology",
            "BMC Bioinformatics", "Nature Methods",
        ],
    },
    "autonomous_systems": {
        "topics": [
            "End-to-End Learning for {app}",
            "Perception Systems for {app}",
            "Planning and Control for {app}",
            "Safety Verification of {app}",
            "Multi-Sensor Fusion for {app}",
            "Sim-to-Real Transfer in {app}",
        ],
        "apps": [
            "Self-Driving Cars", "Autonomous Ships",
            "Unmanned Aerial Vehicles", "Autonomous Mining Vehicles",
            "Robot Swarms", "Automated Guided Vehicles",
            "Autonomous Tractors", "Self-Driving Trucks",
            "Personal Mobility Robots", "Autonomous Inspection Systems",
            "Delivery Robots", "Autonomous Racing",
        ],
        "methods": [
            "Bird's-eye-view perception from surround-view cameras using lift-splat-shoot architecture. Temporal fusion over 5 previous frames for motion estimation. Evaluation on nuScenes and Waymo Open Dataset. Real-time inference at 20 FPS on NVIDIA Orin.",
            "Model predictive control with learned dynamics model. Neural ODE for continuous-time trajectory prediction. Safety constraints using control barrier functions. Hardware-in-the-loop testing on CARLA and LGSVL simulators.",
            "LiDAR-camera fusion using BEVFusion architecture. 3D object detection with CenterPoint head. Multi-object tracking using graph neural network association. Evaluation on KITTI, nuScenes, and Argoverse 2 benchmarks.",
            "Formal verification of neural network controllers using abstract interpretation. Safety envelope computation for planning modules. Statistical model checking with 10M Monte Carlo simulations. Compliance analysis with ISO 26262 and SOTIF standards.",
        ],
        "journals": [
            "IEEE Trans on Intelligent Transportation Systems",
            "CVPR Autonomous Driving Workshop", "CoRL Proceedings",
            "IEEE Intelligent Vehicles Symposium",
            "Robotics and Autonomous Systems", "Journal of Field Robotics",
        ],
    },
}


def _make_paper_id(index: int) -> str:
    return f"SYN-{index:04d}"


def _pick_authors(rng: random.Random, count: int = 2):
    authors = []
    unis = rng.sample(UNIVERSITIES, min(count, len(UNIVERSITIES)))
    for i in range(count):
        first = rng.choice(FIRST_NAMES)
        last = rng.choice(LAST_NAMES)
        authors.append({
            "name": f"Dr. {first} {last}",
            "affiliation": unis[i % len(unis)],
        })
    return authors, unis[0]


def _make_abstract(rng, domain_key, domain, app, title):
    """Generate a realistic abstract for the given paper."""
    templates = [
        f"This paper presents a comprehensive study on {title.lower()}. We propose a novel framework that addresses key challenges in {app.lower()} by leveraging state-of-the-art techniques from {domain_key.replace('_', ' ')}. Our approach is evaluated on multiple benchmark datasets and demonstrates significant improvements over existing methods. Experimental results show that our method achieves {{metric1}} improvement in primary metrics while maintaining computational efficiency. We also provide detailed ablation studies analyzing the contribution of each component. The proposed system handles edge cases including data scarcity, class imbalance, and distribution shift through adaptive techniques. Our open-source implementation is available for reproducibility and further research by the community.",
        f"We address the problem of {app.lower()} using advanced {domain_key.replace('_', ' ')} methods. Our approach introduces a novel architecture that combines multiple learning paradigms to achieve robust performance across diverse conditions. Through extensive experimentation on {{num_datasets}} datasets spanning different domains, we demonstrate that our method outperforms {{num_baselines}} baseline approaches by {{metric1}} on average. We provide theoretical analysis of the convergence properties and computational complexity. The system is designed for practical deployment with latency constraints under {{latency}}ms. Human evaluation confirms the practical utility of our approach in real-world scenarios. We release our code, trained models, and evaluation scripts to facilitate future research.",
        f"In this work, we study {app.lower()} and propose an innovative solution leveraging {domain_key.replace('_', ' ')}. Unlike previous approaches that rely on simplified assumptions, our method handles the full complexity of real-world scenarios including noise, missing data, and adversarial conditions. We introduce a multi-stage pipeline that first performs robust feature extraction, followed by task-specific optimization with regularization techniques. Evaluation on industry-standard benchmarks demonstrates {{metric1}} accuracy with {{metric2}} reduction in error rate compared to the current state of the art. Ablation studies confirm the importance of each design decision. Our method scales linearly with input size, making it suitable for large-scale deployment.",
        f"This research investigates the intersection of {domain_key.replace('_', ' ')} and {app.lower()}, proposing a unified framework that bridges the gap between theoretical advances and practical applications. Our system employs a hierarchical approach combining representation learning, task decomposition, and adaptive optimization. We validate our framework on {{num_datasets}} heterogeneous datasets containing over {{data_size}} samples, achieving state-of-the-art results on {{num_baselines}} competitive benchmarks. Notably, our method demonstrates strong generalization with only {{metric2}} performance degradation on out-of-distribution test sets. We provide comprehensive error analysis, computational cost breakdown, and deployment guidelines for practitioners.",
    ]
    tpl = rng.choice(templates)
    return tpl.format(
        metric1=f"{rng.randint(3, 25)}%",
        metric2=f"{rng.randint(10, 40)}%",
        num_datasets=rng.randint(3, 8),
        num_baselines=rng.randint(4, 12),
        latency=rng.choice([50, 100, 200, 500]),
        data_size=rng.choice(["50K", "100K", "500K", "1M", "5M"]),
    )


def generate_papers(count: int = 1500, seed: int = 42) -> list:
    """Generate `count` synthetic research papers deterministically."""
    rng = random.Random(seed)
    papers = []
    domain_keys = list(DOMAINS.keys())

    for i in range(21, 21 + count):
        dk = rng.choice(domain_keys)
        domain = DOMAINS[dk]

        app = rng.choice(domain["apps"])
        title_tpl = rng.choice(domain["topics"])
        title = title_tpl.format(app=app)

        authors, main_uni = _pick_authors(rng, count=rng.randint(2, 4))
        methodology = rng.choice(domain["methods"])
        journal = rng.choice(domain["journals"])
        year = rng.randint(2019, 2025)
        citations = int(rng.expovariate(1 / 50))

        abstract = _make_abstract(rng, dk, domain, app, title)

        papers.append({
            "paper_id": _make_paper_id(i),
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "methodology": methodology,
            "year": year,
            "citation_count": min(citations, 500),
            "university": main_uni,
            "journal": journal,
            "url": f"https://doi.org/10.1234/syn{i:04d}",
        })

    return papers
