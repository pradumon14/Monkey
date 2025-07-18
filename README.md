# Monkey CLI Password Generator

[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🐒 Deterministic, Local, Secure Password Generation

Monkey CLI is a command-line tool that implements a unique, deterministic password generation algorithm. It allows you to create complex and secure passwords on-demand, without ever storing them. All processing happens locally on your machine, ensuring your privacy and security.

### ✨ Features

* **Deterministic Generation:** The same "Simple Password" and "Unique Key" will always produce the same complex password. This means you don't need to store the generated password.
* **Local Processing:** All password generation, hashing, and transformations occur entirely on your local machine. No data is ever sent to a server.
* **SHA-256 Hashing:** Utilizes the strong SHA-256 cryptographic hash function as the foundation for password derivation.
* **Guaranteed Character Diversity:** Ensures the generated password includes a mix of uppercase letters, lowercase letters, numbers, and symbols (configurable).
* **Flexible Length Control:** Generate passwords of any desired length.
* **Customizable Character Sets:** Choose which character types to include/exclude, and even provide your own set of symbols.
* **Clipboard Integration:** Optionally copy the generated password directly to your system's clipboard for convenience.
* **Basic Strength Estimation:** Provides a local, rule-based assessment of the generated password's strength with actionable feedback.
* **User-Friendly CLI:** Built with `rich` for a clean, colored, and interactive terminal experience (with a fallback for basic terminals).

### 🚀 Installation

1.  **Prerequisites:**
    * Python 3.x (recommended 3.8+) installed on your system.

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/pradumon14/monkey
    cd monkey
    ```

3.  **Install Dependencies (Optional but Recommended):**
    For a rich, colored, and interactive terminal experience, install the `rich` library:
    ```bash
    pip install -r requirements.txt
    ```
    If you choose not to install `rich`, the script will still run, but with basic plain text output.

### 💡 Usage

Run the script from your terminal. You can either provide the length as an argument or be prompted for it.

**Basic Interactive Usage:**

```bash
python monkey.py
```
The tool will then guide you through entering the desired length, your Simple Password, and Unique Key.

**Examples with Options:**

* **Generate a 16-character password:**
    ```bash
    python monkey.py --length 16
    ```

* **Generate 3 passwords of length 12, excluding numbers:**
    ```bash
    python monkey.py -l 12 --count 3 --no-numbers
    ```

* **Generate a 24-character password, using custom symbols and copy to clipboard:**
    ```bash
    python monkey.py --length 24 --symbols-set "!@#$" --copy
    ```

* **Generate a password with verbose output (shows intermediate hash):**
    ```bash
    python monkey.py -l 10 -v
    ```

### 🔒 Security Considerations

* **Your Inputs are Key:** The security of the generated password *directly depends* on the strength and secrecy of your "Simple Password" and the uniqueness/unpredictability of your "Unique Key".
    * **Simple Password:** Treat this as your master key. It should be long, complex, and unique to you. Never share it or write it down in an insecure place.
    * **Unique Key:** While less critical than the Simple Password, using predictable keys (e.g., "google" for Google) can make your generated passwords easier to guess if your Simple Password is ever compromised. Aim for unique, less obvious keys for different services.
* **Local Processing:** Emphasized repeatedly because it's a core security feature. Your sensitive inputs and generated passwords never leave your machine.
* **Deterministic Algorithm:** The algorithm is public and deterministic. Its security does not rely on obscurity. An attacker would need your exact "Simple Password" and "Unique Key" to reproduce your passwords.

### 🆚 Key Differentiators: "Monkey" vs. Traditional Password Solutions

Your "Monkey" tool offers a unique approach to password management that differentiates it significantly from traditional password managers and even simple password generators.

1.  **No Password Storage 🛡️**
    * **Traditional Password Managers:** These tools fundamentally operate by storing your encrypted passwords (and often other sensitive data) in a digital vault, either locally on your device or in the cloud. You access this vault with a single master password.
    * **"Monkey":** Never stores any passwords or keys. It's a pure generation algorithm. This eliminates the largest attack surface common to all password managers: the risk of their central database being breached or the master password being compromised. Your passwords exist only in the moment they are generated.

2.  **On-Demand Generation via Deterministic Algorithm 💡**
    * **Traditional Password Managers:** While many include built-in generators, their primary function is retrieval from storage. Users often rely on them to autofill stored credentials.
    * **"Monkey":** Generates the complex password deterministically on the fly using your simple password and unique key. This means you don't retrieve a stored password; you re-create it using a consistent mathematical process. As long as you remember your simple password and unique key, you can generate the correct complex password anywhere.

3.  **Device & Account Independence 🌍**
    * **Traditional Password Managers:** Often require you to install their application or browser extension on each device, and you typically need to be logged into your password manager account (which is tied to a master password).
    * **"Monkey":** Offers unparalleled flexibility. Since it's a CLI tool (and could be adapted to web-based or extension), you only need your remembered simple inputs. You're not tied to a specific device, installed software, or a centralized service account.

4.  **Enhanced Privacy & Reduced Trust Burden ✅**
    * **Traditional Password Managers:** Users must trust the password manager company with their encrypted vault, their infrastructure security, and their privacy policies. While many are reputable, this trust is still a prerequisite.
    * **"Monkey":** Drastically reduces the trust burden. Since your simple password and unique key are processed locally (in-terminal) and never leave your device or reach any server, there's no third party to trust with your core credentials. This significantly enhances privacy.

5.  **Focus on Algorithm over Storage Management 🛠️**
    * **Traditional Password Managers:** Their complexity lies in secure storage, synchronization across devices, autofill capabilities, and potentially auditing password health.
    * **"Monkey":** Its core strength and innovation lie in its deterministic cryptographic algorithm that transforms simple, memorable inputs into highly complex and unique outputs, tailored to a desired length and character set.

### ⚙️ How It Works (Briefly)

1.  **Combine Inputs:** Your "Simple Password" and "Unique Key" are concatenated.
2.  **SHA-256 Hash:** This combined string is hashed using SHA-256, producing a 64-character hexadecimal string.
3.  **Length Adjustment:** The hash is either truncated or extended (by repeating itself) to match your desired password length.
4.  **Deterministic Transformation:** The extended hash is then used to deterministically select character types (uppercase, lowercase, numbers, symbols) and specific characters for each position in the final password. This process ensures diversity without true randomness.
5.  **Diversity Guarantee:** A final pass ensures that all enabled character types are present in the password, injecting them deterministically if missing.

### ❤️ Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or find any bugs.

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Created with ❤️ by [Pradumon Sahani](https://github.com/pradumon14)

