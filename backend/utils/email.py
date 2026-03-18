import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)


async def send_email(
    to_email: str,
    subject: str,
    html_body: str,
    text_body: Optional[str] = None,
) -> bool:
    """
    Send an email using SMTP. Returns True on success, False on failure.
    Fails silently if SMTP is not configured.
    """
    if not settings.SMTP_USERNAME or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured. Email not sent to %s", to_email)
        return False

    try:
        import aiosmtplib

        message = MIMEMultipart("alternative")
        message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = to_email
        message["Subject"] = subject

        if text_body:
            message.attach(MIMEText(text_body, "plain"))
        message.attach(MIMEText(html_body, "html"))

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        logger.info("Email sent to %s", to_email)
        return True
    except Exception as e:
        logger.error("Failed to send email to %s: %s", to_email, str(e))
        return False


async def send_password_reset_email(to_email: str, reset_token: str) -> bool:
    """Send password reset email."""
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    subject = "MICE Travel Mate - Password Reset"
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2563eb;">Password Reset Request</h2>
        <p>You have requested to reset your password for MICE Travel Mate.</p>
        <p>Click the button below to reset your password:</p>
        <a href="{reset_url}"
           style="display: inline-block; padding: 12px 24px; background-color: #2563eb;
                  color: white; text-decoration: none; border-radius: 6px; margin: 16px 0;">
            Reset Password
        </a>
        <p>Or copy and paste this link: <br><a href="{reset_url}">{reset_url}</a></p>
        <p style="color: #666; font-size: 14px;">This link expires in 1 hour. If you did not request this, please ignore this email.</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
        <p style="color: #999; font-size: 12px;">MICE Travel Mate</p>
    </body>
    </html>
    """
    return await send_email(to_email, subject, html_body)


async def send_booking_confirmation_email(
    to_email: str,
    booking_number: str,
    booking_type: str,
    booking_date: str,
    total_amount: float,
    guest_name: str,
    item_name: str = "",
) -> bool:
    """Send booking confirmation email."""
    subject = f"MICE Travel Mate - Booking Confirmed ({booking_number})"
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #2563eb;">Booking Confirmed!</h2>
        <p>Dear {guest_name},</p>
        <p>Your booking has been confirmed. Here are the details:</p>
        <div style="background: #f8fafc; padding: 20px; border-radius: 8px; margin: 16px 0;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px 0; color: #666;">Booking Number:</td>
                    <td style="padding: 8px 0; font-weight: bold;">{booking_number}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;">Type:</td>
                    <td style="padding: 8px 0;">{booking_type.title()}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;">Item:</td>
                    <td style="padding: 8px 0;">{item_name}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;">Date:</td>
                    <td style="padding: 8px 0;">{booking_date}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;">Total Amount:</td>
                    <td style="padding: 8px 0; font-weight: bold;">${total_amount:.2f} USD</td>
                </tr>
            </table>
        </div>
        <p>You can view your booking at any time by visiting our website.</p>
        <p>Thank you for choosing MICE Travel Mate!</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
        <p style="color: #999; font-size: 12px;">MICE Travel Mate</p>
    </body>
    </html>
    """
    return await send_email(to_email, subject, html_body)


async def send_booking_cancellation_email(
    to_email: str,
    booking_number: str,
    guest_name: str,
    reason: str = "",
) -> bool:
    """Send booking cancellation email."""
    subject = f"MICE Travel Mate - Booking Cancelled ({booking_number})"
    reason_text = f"<p>Reason: {reason}</p>" if reason else ""
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #dc2626;">Booking Cancelled</h2>
        <p>Dear {guest_name},</p>
        <p>Your booking <strong>{booking_number}</strong> has been cancelled.</p>
        {reason_text}
        <p>If you have any questions, please contact our support team.</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
        <p style="color: #999; font-size: 12px;">MICE Travel Mate</p>
    </body>
    </html>
    """
    return await send_email(to_email, subject, html_body)
