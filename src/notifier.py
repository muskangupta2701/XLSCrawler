import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL

def send_alert(anomaly_report, business_summary):
    """
    Sends an email alert (or prints to console if not configured).
    """
    anomalies = anomaly_report.get("anomalies", {})
    date = anomaly_report.get("date")
    
    if not anomalies:
        return
        
    # Format the data for the email
    html_content = f"""
    <html>
      <body>
        <h2>🚨 AI Anomaly Alert: {date}</h2>
        <p><strong>Business Summary:</strong></p>
        <p><em>{business_summary}</em></p>
        <hr>
        <h3>Metric Deviations</h3>
        <ul>
    """
    
    for metric, details in anomalies.items():
        html_content += f"<li><b>{metric}</b>: {details['direction']} by {abs(details['pct_change']):.1%} (Current: {details['current']:.2f} | 7-Day Avg: {details['baseline']:.2f})</li>"
        
    html_content += """
        </ul>
      </body>
    </html>
    """

    if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
        print("\n" + "="*50)
        print("MOCK EMAIL SENT TO CONSOLE (Configure SMTP in .env to send real emails)")
        print("="*50)
        print(html_content)
        print("="*50 + "\n")
        return

    # Actually send the email
    try:
        print("Sending email alert...")
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"🚨 Metric Anomaly Detected: {date}"
        
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
