# ALGORITHMS_USED

## 1. Department Classification Algorithms

### 1.1 Rule-Based Keyword Matching
- **Type:** Deterministic rule engine
- **Purpose:** Quickly route complaints to departments when known keywords are present
- **How it works:**
  - Normalize text (lowercase, trim, whitespace cleanup)
  - Check complaint text against department-wise keyword dictionaries
  - Return the first/best matching department with high confidence
- **Used in:**
  - `backend/services/routing_service.py`
  - `backend/utils/routing_service.py`
  - `backend/services/keyword_routing.py`

### 1.2 ML Text Classification (TF-IDF + Logistic Regression)
- **Type:** Supervised machine learning classifier
- **Purpose:** Predict department when rule-based match is not found
- **How it works:**
  - Convert complaint text into TF-IDF vectors (word + bigram features)
  - Classify with Logistic Regression
  - Use class probabilities (`predict_proba`) to compute confidence
- **Used in:**
  - Training: `backend/ai/train_model.py`
  - Inference: `backend/ai/predict.py`

### 1.3 Exact-Match Priority Over ML
- **Type:** Lookup optimization
- **Purpose:** Improve accuracy for known training sentences
- **How it works:**
  - Precompute map: normalized training text -> department
  - If exact text found, return mapped label immediately (confidence 1.0)
- **Used in:** `backend/ai/predict.py`

### 1.4 Confidence Threshold Gating
- **Type:** Decision thresholding
- **Purpose:** Prevent low-confidence auto-routing errors
- **How it works:**
  - Accept ML label only if confidence >= threshold
  - Otherwise route to fallback (`Unclassified`)
  - Threshold is configurable in system settings
- **Used in:**
  - `backend/ai/predict.py`
  - `backend/utils/routing_service.py`

### 1.5 Hybrid Routing Pipeline
- **Type:** Multi-stage decision pipeline
- **Purpose:** Combine explainability + coverage + safety
- **How it works (ordered):**
  1. Rule-based routing
  2. ML routing
  3. Fallback routing (`Unclassified`)
- **Used in:**
  - `backend/services/routing_service.py`
  - `backend/utils/routing_service.py`

---

## 2. Priority and Severity Algorithms

### 2.1 Rule-Based Severity Layering
- **Type:** Weighted rule scoring
- **Purpose:** Estimate issue severity (Critical/High/Medium/Low)
- **How it works:**
  - Match risk terms (critical/high/medium/low buckets)
  - Apply deterministic weighted scoring
  - Map final score/category to priority
- **Used in:** `backend/ai/predict_priority.py`

### 2.2 Department-Aware Priority Escalation
- **Type:** Rule override/escalation
- **Purpose:** Increase safety for high-risk departments/events
- **How it works:**
  - Escalate priority if department-risk and complaint-risk combinations are detected
  - Example: dangerous electricity incidents -> escalate to high
- **Used in:** `backend/ai/predict_priority.py`

### 2.3 Regex-Based Risk Pattern Detection
- **Type:** Pattern matching
- **Purpose:** Catch semantic risk phrases not covered by plain term lists
- **How it works:**
  - Run predefined regex patterns for critical/high-risk events
  - Use matches in priority decision logic
- **Used in:** `backend/ai/predict_priority.py`

---

## 3. Multilingual Processing Algorithms

### 3.1 Script-Based Language Detection
- **Type:** Unicode-range heuristic
- **Purpose:** Identify Malayalam vs English input
- **How it works:**
  - Detect Malayalam Unicode block (`\u0D00-\u0D7F`)
- **Used in:** `backend/utils/language_utils.py`

### 3.2 Translation-Based Normalization
- **Type:** API-assisted preprocessing
- **Purpose:** Standardize multilingual complaints into English for classification
- **How it works:**
  - Malayalam input is translated to English
  - Classification runs on translated text
- **Used in:**
  - `backend/utils/language_utils.py`
  - `backend/services/routing_service.py`
  - `backend/utils/routing_service.py`
  - `backend/chatbot/intent_handler.py`

---

## 4. Chatbot Algorithms

### 4.1 Rule-Based Intent Detection with Priority Ordering
- **Type:** Deterministic intent classifier
- **Purpose:** Detect user intent (greeting, complaint, status check, etc.)
- **How it works:**
  - Maintain keyword lists per intent
  - Check intents in strict priority order
  - First matched intent is selected
- **Used in:** `backend/chatbot/intent_handler.py`

### 4.2 Fallback Intent Heuristic for Issue-Like Text
- **Type:** Heuristic classification
- **Purpose:** Treat unstructured problem descriptions as complaint intent
- **How it works:**
  - If no direct intent match but issue hints exist -> classify as `file_complaint`
- **Used in:** `backend/chatbot/intent_handler.py`

### 4.3 Stateful Conversation Flow (Finite State Machine)
- **Type:** FSM/dialogue state management
- **Purpose:** Guided complaint drafting in steps
- **States:** `IDLE -> COLLECT_WHAT -> COLLECT_WHERE -> COLLECT_WHEN -> CONFIRM`
- **Used in:** `backend/chatbot/chatbot.py`

### 4.4 Deterministic Variant Selection for Responses
- **Type:** Hash-like deterministic variant picker
- **Purpose:** Return varied but reproducible response phrasing
- **How it works:**
  - Picks response variant index using character-code sum of message
- **Used in:** `backend/chatbot/response_generator.py`

---

## 5. Complaint Assignment Algorithms

### 5.1 Least-Workload Staff Assignment
- **Type:** Greedy minimization
- **Purpose:** Auto-assign complaint to least-loaded staff in a department
- **How it works:**
  - Count assigned complaints per active staff
  - Pick staff with minimum count (`min`)
- **Used in:** `backend/services/assignment_service.py`

### 5.2 Round-Robin Style Bulk Assignment (Seeding Utility)
- **Type:** Cyclic distribution
- **Purpose:** Evenly distribute unassigned complaints during seed/maintenance operations
- **How it works:**
  - Iterate complaints, assign staff using index modulo staff-count
- **Used in:** `backend/routes/admin.py` (`seed_staff_and_assign`)

---

## 6. Analytics and Reporting Algorithms

### 6.1 Aggregation Pipelines (MongoDB)
- **Type:** Group-by aggregation
- **Purpose:** Build admin report metrics
- **How it works:**
  - Use `$match` + `$group` to compute counts by status/department
- **Used in:** `backend/routes/admin.py`

### 6.2 Derived KPI Computation
- **Type:** Deterministic metric formulas
- **Purpose:** Compute totals, pending/resolved stats, staff workload metrics
- **Used in:** `backend/routes/admin.py`, `backend/routes/staff.py`

---

## 7. Security-Related Algorithms

### 7.1 Password Hashing and Verification
- **Type:** One-way cryptographic hashing (Werkzeug / bcrypt compatibility paths)
- **Purpose:** Store passwords securely and verify login attempts
- **Used in:**
  - `backend/utils/security.py`
  - `backend/routes/citizen_auth.py`

### 7.2 JWT Token Signing and Validation
- **Type:** HMAC SHA-256 (`HS256`)
- **Purpose:** Stateless auth token generation/verification
- **Used in:**
  - `backend/utils/jwt_utils.py`
  - `backend/middleware/jwt_required.py`

---

## 8. ID Generation Algorithm

### 8.1 Human-Friendly Complaint ID Generator
- **Type:** Prefix + year + random token generation
- **Format:** `SG-YY-XXXXX`
- **Purpose:** Short, readable unique complaint IDs
- **How it works:**
  - Prefix `SG`
  - Current year suffix (2 digits)
  - Random token from custom safe alphabet
- **Used in:** `backend/utils/id_generator.py`

---

## 9. Training/Feature Engineering Summary

- Text normalization: lowercase + punctuation removal + whitespace normalization
- Vectorization: TF-IDF (unigram + bigram for department model)
- Classification model: Logistic Regression
- Confidence use: `predict_proba` for threshold-gated decisions

Files:
- `backend/ai/preprocess.py`
- `backend/ai/train_model.py`
- `backend/ai/train_priority_model.py`
- `backend/ai/predict.py`

---

## 10. End-to-End Decision Flow (At Runtime)

1. Complaint text received
2. Language detection and translation (if Malayalam)
3. Rule-based department routing
4. ML fallback department prediction (TF-IDF + Logistic Regression)
5. Confidence threshold check
6. Fallback to `Unclassified` if needed
7. Priority/severity prediction
8. Least-workload staff assignment (if eligible)
9. Persist complaint with routing metadata
