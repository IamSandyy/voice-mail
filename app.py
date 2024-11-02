import tkinter as tk
from tkinter import scrolledtext
from voice_utils import SpeakText, speech_to_text
from email_utils import composeMail, getMailBoxStatus, getLatestMails, findMail

class VoiceEmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice-Controlled Email App")
        self.root.geometry("500x400")

        # Title label
        tk.Label(root, text="Voice-Controlled Email App", font=("Arial", 16)).pack(pady=10)

        # Output area for displaying results
        self.output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 10))
        self.output_text.pack(pady=10)

        # Initial announcement and voice command prompt
        root.after(1000, self.announce_and_listen_for_command)

    def announce_and_listen_for_command(self):
        # Announce available options and start listening for a command
        SpeakText("Choose an option by saying Send Email, Check Mailbox Status, or Get Last 3 Emails.")
        self.listen_for_command()

    def listen_for_command(self):
        command = speech_to_text()
        if command:
            self.handle_command(command.lower())
        else:
            SpeakText("Sorry, I didn't catch that. Please say it again.")
            self.listen_for_command()

    def handle_command(self, command):
        self.clear_output()

        if "send email" in command or "send" in command or "send mail" in command:
            self.send_email()

        elif "check mailbox status" in command or "check inbox" in command or "check" in command:
            self.check_mailbox_status()

        elif "get last 3 emails" in command or "get last three emails" in command or "last 3 emails" in command or "latest emails" in command or "latest" in command:
            self.get_latest_emails()

        elif "find email" in command or "find mail" in command:
            self.find_email()

        else:
            SpeakText("Invalid command. Please say Send Email, Check Mailbox Status, Get Last 3 Emails, or Find Email.")
            self.listen_for_command()  # Retry listening for a valid command

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    def display_message(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)  # Scroll to the end of the text

    def send_email(self):
        SpeakText("Please follow the instructions for sending the email.")
        result = composeMail()
        if result:
            self.display_message("Email sent successfully.")
        else:
            self.display_message("Email sending failed.")

    def check_mailbox_status(self):
        SpeakText("Checking mailbox status.")
        status = getMailBoxStatus()
        self.display_message(f"Mailbox Status:\n{status}")

    def get_latest_emails(self):
        SpeakText("Fetching last 3 emails.")
        emails = getLatestMails()
        if emails:
            self.display_message("Latest emails:")
            for email in emails:
                email_info = f"From: {email['from']}\nSubject: {email['subject']}\n---"
                self.display_message(email_info)
                # Speak the email details
                SpeakText(f"Email from {email['from']}, subject {email['subject']}")
        else:
            self.display_message("No emails found.")



    def find_email(self):
        SpeakText("Please say the search query, such as a name or subject.")
        search_query = speech_to_text()

        if search_query and search_query.strip():
            SpeakText(f"Searching for emails with {search_query}.")
            emails = findMail(search_query)
            if emails:
                self.display_message("Found emails:")
                for email in emails:
                    result = f"From: {email['from']}\nSubject: {email['subject']}\n---"
                    self.display_message(result)
                    # Speak the email details
                    SpeakText(f"Email from {email['from']}, subject {email['subject']}")
            else:
                self.display_message("No emails found.")
                SpeakText("No emails found.")
        else:
            SpeakText("No search query provided.")
while True:
    if __name__ == "__main__":
        root = tk.Tk()
        app = VoiceEmailApp(root)
        root.mainloop()
