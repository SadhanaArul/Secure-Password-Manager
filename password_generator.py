import random
import string

class PasswordGenerator:
    @staticmethod
    def generate_password(length=14):
        if length < 12:
            length = 12
        if length > 16:
            length = 16
        
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(special_chars)
        ]
        
        all_chars = lowercase + uppercase + digits + special_chars
        password.extend(random.choice(all_chars) for _ in range(length - 4))
        random.shuffle(password)
        
        return ''.join(password)
    
    @staticmethod
    def check_strength(password):
        score = 0
        feedback = []
        
        if len(password) >= 12:
            score += 1
        elif len(password) >= 8:
            feedback.append("Consider using at least 12 characters")
        else:
            feedback.append("Password is too short")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            score += 1
        else:
            feedback.append("Add special characters")
        
        if score >= 4:
            strength = "Very Strong"
        elif score >= 3:
            strength = "Strong"
        elif score >= 2:
            strength = "Medium"
        else:
            strength = "Weak"
        
        return strength, feedback