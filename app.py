from flask import Flask, request
import random
import os, sys

# Generate random port
prt = int(random.randint(5000, 9000))

# Clear terminal
os.system('cls' if sys.platform.startswith('win') else 'clear')

# Terminal UI
print("""[~]=========================================[~]
[~]       Cloudflare Captcha Token Grabber         [~]
[~]       Telegram Channel: @sabbirmolla036        [~]
[~]=========================================       [~]
""".strip())
print(f'Web url : \033[0;32mhttp://localhost:{prt}\033[0m')
print("=============================================")
print(" Note:\033[0;32m Open the URL in your browser and solve the CAPTCHAs.\n More widgets = more tokens!\033[0m")
print("=============================================")

# Flask app
app = Flask(__name__)
tokens = []

# HTML with auto-reload after token received
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloudflare CAPTCHA</title>
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .captcha-box {
            margin: 20px auto;
            width: fit-content;
        }
        #status {
            font-weight: bold;
            color: green;
        }
    </style>
</head>
<body>
    <h2>Captcha Token Collector</h2>
    <h3>Telegram: @sabbirmolla036</h3>
    <div id="status">Solve any CAPTCHA below to generate tokens.</div>

    <!-- Multiple CAPTCHA widgets -->
    <div class="captcha-box cf-turnstile" data-sitekey="0x4AAAAAAA4PZrjDa5PcluqN" data-callback="onCaptchaVerified"></div>
    <div class="captcha-box cf-turnstile" data-sitekey="0x4AAAAAAA4PZrjDa5PcluqN" data-callback="onCaptchaVerified"></div>
    <div class="captcha-box cf-turnstile" data-sitekey="0x4AAAAAAA4PZrjDa5PcluqN" data-callback="onCaptchaVerified"></div>
    <div class="captcha-box cf-turnstile" data-sitekey="0x4AAAAAAA4PZrjDa5PcluqN" data-callback="onCaptchaVerified"></div>
    <div class="captcha-box cf-turnstile" data-sitekey="0x4AAAAAAA4PZrjDa5PcluqN" data-callback="onCaptchaVerified"></div>

    <script>
        async function onCaptchaVerified(token) {
            document.getElementById("status").textContent = "Token received, sending...";
            try {
                const response = await fetch(`/reserve_token?token=${token}`);
                if (response.ok) {
                    document.getElementById("status").textContent = "Token stored! Reloading...";
                    setTimeout(() => location.reload(), 1000); // Auto reload after 1 second
                } else {
                    document.getElementById("status").textContent = "Failed to store token.";
                }
            } catch {
                document.getElementById("status").textContent = "Error sending token.";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return template

@app.route('/reserve_token')
def reserve_token():
    token = request.args.get('token')
    if token:
        tokens.append(token)
        with open("tokens.txt", "a") as f:
            f.write(token + "\n")
    return 'ok'

@app.route('/get')
def get_token():
    try:
        return tokens.pop()
    except IndexError:
        return 'No tokens available'

# Run app
app.run(port=prt)
