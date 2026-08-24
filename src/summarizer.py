from google import genai
from .config import GEMINI_API_KEY

def generate_summary(anomaly_report):
    """
    Uses the Gemini API to generate a business-friendly summary of the anomalies.
    """
    anomalies = anomaly_report.get("anomalies", {})
    date = anomaly_report.get("date")
    
    if not anomalies:
        return "No anomalies detected."
        
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        print("WARNING: Gemini API key not set. Skipping AI summary generation.")
        return _generate_fallback_summary(anomalies)

    print("Generating AI summary using Gemini...")
    
    # Initialize the client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Format the anomalies for the prompt
    anomalies_str = ""
    for metric, details in anomalies.items():
        anomalies_str += f"- {metric} {details['direction']} by {abs(details['pct_change']):.1%}. (Current: {details['current']:.2f}, Normal: {details['baseline']:.2f})\n"

    prompt = f"""
    You are a senior business analyst. Review the following metrics that showed anomalous behavior on {date}:
    
    {anomalies_str}
    
    Write a 3-sentence executive summary explaining what changed and hypothesize one realistic business reason why this might have happened (e.g., if traffic spiked but conversion dropped, maybe low-quality bot traffic occurred).
    Keep it professional, clear, and action-oriented. Do not use technical jargon.
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return _generate_fallback_summary(anomalies)

def _generate_fallback_summary(anomalies):
    """Fallback if API is unavailable."""
    summary = "System Alert: The following metrics require attention due to significant deviations from the baseline:\n"
    for metric, details in anomalies.items():
        summary += f"- {metric} {details['direction']} by {abs(details['pct_change']):.1%}.\n"
    summary += "Please review the data dashboard for further insights."
    return summary
