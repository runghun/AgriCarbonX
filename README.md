# AgriCarbonX
**AgriCarbonX – Carbon Credit Marketplace for Farmers**

AgriCarbonX is a web-based platform that helps farmers earn **carbon credits** for adopting eco-friendly farming practices such as soil conservation, organic farming, tree planting, and low-carbon agriculture.

Farmers can easily **track emissions**, **generate credits**, and **sell credits** to buyers through a simple marketplace.

---

### 👨‍🌾 **Farmer Panel**

* Farmer registration & login
* Dashboard showing carbon credits earned
* Upload farming practices (trees planted, organic proof, soil score)
* View carbon credit value in ₹
* Payment/withdrawal screen

### 🛒 **Carbon Credit Marketplace**

* Buyers can purchase verified farmer carbon credits
* Real-time credit rates
* Secure checkout

### 📊 **Admin (optional)**

* Verify farmer submissions
* Approve carbon credits

---

## 🛠️ **Tech Stack**

| Component | Technology                        |
| --------- | --------------------------------- |
| Backend   | Flask (Python)                    |
| Frontend  | HTML, Tailwind CSS, JavaScript, Bootstrap             |
| Templates | Jinja2                            |
| Database  | MySQL                             |
| Hosting   | Local / GitHub deployment support |

---

## 📂 **Project Structure**

```
AgriCarbonX/
│── app.py                  # Main Flask file
│── static/
│     ├── css/style.css
│     ├── images/
│           ├── co2.jpg
│           ├── home_banner.jpeg
│           ├── how can we help.jpg
│           └── no dp.jpg
│
│── templates/
│     ├── about.html
│     ├── dashboard.html
│     ├── farmer_form.html
│     ├── home.html
│     ├── login.html
│     ├── marketplace.html
│     ├── password.html
│     ├── payment.html
│     ├── peer_to_peer.html
│     ├── reset_request_sent.html
│     └── result.html
│
└── README.md
```

---

### 2️⃣ Install dependencies

```
pip install flask mysql-connector-python
```

### 3️⃣ Update MySQL credentials in `app.py`

### 4️⃣ Run the server

```
python app.py
```

### 5️⃣ Open in browser

```
http://127.0.0.1:5000
```

---

## 🎯 **Problem Solved**

The Problem It Solves

Farmers perform climate-positive actions like soil conservation, tree planting, crop rotation, and organic farming, but they do not earn any carbon credit income because:
The carbon credit certification process is too expensive
Verification requires specialized auditors and heavy paperwork
Farmers lack technical knowledge and digital access
Middlemen take a major share of the profit
Existing systems are slow, opaque, and non-farmer-friendly
This creates a huge income gap, even though farmers contribute significantly to carbon reduction and environmental protection.
Our platform solves this by providing a simple, affordable, and transparent carbon credit system designed specifically for farmers.

## Challenges ##

1. ifficulty in Accurate Carbon Calculation

Estimating soil and tree carbon without expensive tools was challenging.

2. No Access to Real Farmer Data

Lack of real-world datasets made testing and validation harder.

3. Complex Carbon Credit Rules

Understanding carbon registry guidelines and converting them into a simple digital workflow was tough.

4. Integrating Multiple Technologies

Connecting AI, satellite data, backend APIs, and blockchain caused several integration issues.

5. Designing Farmer-Friendly UI

Creating a simple interface for rural users with low digital literacy required careful UI planning.

6. Slow Verification Process

Initial verification workflows were slow and required backend optimization.

7. Ensuring Transparency & Avoiding Fraud

We had to prevent duplicate or fake carbon claims in the system.
