import os

import extract_msg


def extract_msg_file(file_path, attachment_dir="attachments"):
    """
    Extracts data from a .msg file and saves attachments.

    Parameters:
        file_path (str): Path to the .msg file.
        attachment_dir (str): Directory where attachments will be saved.
    """
    # Create the attachment directory if it doesn't exist
    if not os.path.exists(attachment_dir):
        os.makedirs(attachment_dir)

    # Load the .msg file
    msg = extract_msg.Message(file_path)

    # Extract email details
    subject = msg.subject
    sender = msg.sender
    recipients = msg.to
    cc = msg.cc
    date = msg.date
    body = msg.body
    # html_body = msg.htmlBody  # Optional: if HTML content is available

    # Print extracted information
    print("Subject:", subject)
    print("Sender:", sender)
    print("Recipients:", recipients)
    print("CC:", cc)
    print("Date:", date)
    print("Body:\n", body)
    # Uncomment the next line if you want to see the HTML version of the body
    # print("HTML Body:\n", html_body)

    # Save attachments, if any
    if msg.attachments:
        print("\nSaving attachments:")
        for attachment in msg.attachments:
            # Save the attachment in the specified directory
            attachment.save(customPath=attachment_dir)
            print(f" - Saved '{attachment.longFilename}' to '{attachment_dir}'")
    else:
        print("\nNo attachments found.")


if __name__ == "__main__":
    import argparse

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Extract contents from a .msg file.")
    parser.add_argument("msg_file", help="Path to the .msg file")
    parser.add_argument("--attachment_dir", default="attachments", help="Directory to save attachments (default: 'attachments')")
    args = parser.parse_args()

    extract_msg_file(args.msg_file, args.attachment_dir)
