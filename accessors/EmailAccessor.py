from fastapi import FastAPI, BackgroundTasks
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.responses import JSONResponse

# The function for sending news
async def send_news_to_users(user_news: list[dict], background_tasks: BackgroundTasks) -> list[str]:
    """
    The function accepts 2 parameters
1. A list of dictionaries, each containing the email and the personalized news
2. An object that manages background tasks to send an email asynchronously

The function returns a list of states for each email
whether it was sent with news or with a no news message
    """
    statuses = []

    for user in user_news:
        email = user["email"]
        news = user["news"]  

        if news:
            subject = "Your personalized news updates"
            body = "\n".join(news)  # Convert the news list into a single string to be sent to the user
            background_tasks.add_task(send_email, email, subject, body)
            statuses.append(f"Email for {email} scheduled successfully.")
        else:
            subject = "No News Available"
            body = "There are no news updates for your selected categories today. Please check back tomorrow."
            background_tasks.add_task(send_email, email, subject, body)
            statuses.append(f"Email for {email} scheduled (no news).")

    return statuses


# The function for sending an email
def send_email(to_email: str, subject: str, body: str):
    """
This function sends an email via an SMTP server
It receives the recipient's address, header, and body of the email
It runs inside the task that is added to the background by the send_news_to_users function
and is therefore executed asynchronously, so we don't wait for each email to be sent 
before starting to send the next one
    """
    try:
        from_email = "nwh506616@gmail.com"
        from_password = "fzvb hwar xxrh tauf"

       
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        
        body_with_intro = "Your news updates for today:\n\n" + body  
        body_text = MIMEText(body_with_intro, 'plain', _charset='utf-8')  
        msg.attach(body_text)

       # Connecting to the server and sending
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)

        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")
        raise Exception(f"Failed to send email: {e}")

#if __name__ == "__main__":
   # test_email = "deniss4293@gmail.com"  
    
   # send_email(
        #to_email=test_email,
      #  subject="Test Email",
       # body="This is a test email from my Python application"
  #  )
   # print("Test email sent successfully!")
    
  