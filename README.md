# 📧 Bulk Email Sender Tool

A powerful Python tool for sending personalized, professional bulk emails to multiple recipients using SMTP. Ideal for developers, marketers, and businesses who want to automate email campaigns securely.

---

## 🔥 Features

- ✅ Send emails to multiple recipients at once  
- ✅ Read recipient email addresses from a CSV file  
- ✅ Send 100+ emails in one batch  
- ✅ Customize each email individually (name, links, etc.)  
- ✅ Use professional email templates (HTML or plain text)  
- ✅ Supports dynamic content injection  
- ✅ Fully responsive email design  
- ✅ Secure SMTP communication with TLS/SSL  
- ✅ Works with Gmail, Yahoo, or custom SMTP servers  
- ✅ App password-based authentication supported  

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/bulk-email-sender.git
```

### 2. Install Required Dependencies
Make sure you have Python installed. Then install the required packages:
```bash
pip install -r requirements.txt
```

### 3. Prepare Your CSV File with Recipient Data
Create a CSV file like recipients.csv with the following format:
```bash
name, email, link
John Doe,john@example.com,https://example.com/john
Jane Smith,jane@example.com,https://example.com/jane
```

### 4. Set Up SMTP Configuration
You can set your SMTP credentials either in a config.json file or using environment variables.
Example config.json:
```bash
{
  "smtp_server": "smtp.gmail.com",
  "port": 587,
  "sender_email": "youremail@gmail.com",
  "app_password": "your_app_password"
}
```

# 🤝Contributing <br>
Found a bug? Want to improve the tool? Fork this repo and submit a Pull Request.<br>
We welcome all kinds of contributions — bug fixes, improvements, new features, or template enhancements.<br>
<br>
<h1 align="center">DevCode Journey</h1>
<br>
