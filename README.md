# SLAB-Protocol

## SLAB™ 1.0 – Standardized Labeling and Attribution Benchmark

### A Trading Card Data Standard Powered by AI

[Visit SLAB Protocol Website](https://slabprotocol.streamlit.app)

---

SLAB™ is an open data standard designed to bring structure and consistency to the trading card industry. It leverages AI-powered data extraction to transform unstructured card descriptions into machine-readable data.

---

## Why SLAB™?

- The trading card market lacks a universal data standard.
- Descriptions vary across platforms, making it hard to search, verify, price, and manage cards.
- SLAB™ introduces a standardized format to simplify inventory management, marketplace listings, and data sharing.

---

## SLAB™ AI Builder

The SLAB™ front-end app helps users:

- Upload raw card data (e.g., descriptions).
- Automatically extract structured fields (Year, Player, Set, Parallel, etc.) using AI.
- Review, refine, and export SLAB™-compliant data (including XML).
- Contribute validated data to improve the AI models.

---

## Hybrid AI Model: Why ChatGPT + Custom Model?

After extensive testing of different approaches, SLAB™ found that combining ChatGPT's natural language understanding with a custom-trained extraction model is the most effective solution for parsing trading card descriptions. Here's why:

### Key Benefits:
- **Flexibility:** ChatGPT excels at interpreting new and varied descriptions, handling edge cases better than rigid rule-based systems.
- **Domain-Specific Precision:** The custom model is trained specifically on trading card data, allowing it to accurately identify structured fields like Player Name, Set, and Parallel.
- **Iterative Improvement:** The hybrid approach allows SLAB™ to leverage GPT's reasoning capabilities when the custom model encounters uncertainty, improving overall accuracy.
- **Scalability:** This approach scales well as the dataset is continuously expanded and the model is refined with community contributions.

### Why Not Other Methods?
Other methods explored—like regex-only parsing, rule-based systems, and standalone machine learning models—proved to be:

- **Too brittle:** They often failed when descriptions deviated from expected patterns.
- **Maintenance-heavy:** Required constant updates as new sets and parallels were released.
- **Lacking adaptability:** Struggled to handle the diverse and evolving nature of trading card descriptions.

Combining GPT’s language understanding with the specialized extraction model delivers the best balance of **accuracy**, **adaptability**, and **scalability**.

---

## Version 1.0 Notes

- This is an early test version built with Streamlit; some quirks are expected.
- Focused on establishing the foundation for standardization, continually improving the model and learning AI along the way!

---

## Contact

Feedback is welcome! Reach out at:  
[slabprotocolfeedback@gmail.com](mailto:slabprotocolfeedback@gmail.com)
