from fastapi import FastAPI, BackgroundTasks
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi.responses import JSONResponse

# פונקציה לשליחת חדשות למספר משתמשים
async def send_news_to_users(user_news: list[dict], background_tasks: BackgroundTasks) -> list[str]:
    statuses = []

    for user in user_news:
        email = user["email"]
        news = user["news"]  # רשימה של מחרוזות בלבד

        if news:
            subject = "Your personalized news updates"
            body = "\n".join(news)  # ממיר רשימת מחרוזות לטקסט
            background_tasks.add_task(send_email, email, subject, body)
            statuses.append(f"Email for {email} scheduled successfully.")
        else:
            subject = "No News Available"
            body = "There are no news updates for your selected categories today. Please check back tomorrow."
            background_tasks.add_task(send_email, email, subject, body)
            statuses.append(f"Email for {email} scheduled (no news).")

    return statuses



# הפונקציה לשליחת המייל
# הפונקציה לשליחת המייל
import smtplib

# הפונקציה לשליחת המייל
import smtplib

# הפונקציה לשליחת המייל
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# הפונקציה לשליחת המייל
def send_email(to_email: str, subject: str, body: str):
    try:
        from_email = "nwh506616@gmail.com"
        from_password = "fzvb hwar xxrh tauf"

        # יצירת הודעת מייל עם MIMEText לקידוד UTF-8
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # יצירת גוף המייל עם הטקסט הנוסף בתחילת המייל
        body_with_intro = "Your news updates for today:\n\n" + body  # הוספת הטקסט בתחילת הגוף
        
        # יצירת גוף המייל והקידוד
        body_text = MIMEText(body_with_intro, 'plain', _charset='utf-8')  # קידוד UTF-8
        msg.attach(body_text)

        # חיבור לשרת ושליחה
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
       # body="This is a test email from my Python application."
  #  )
   # print("Test email sent successfully!")
    
  