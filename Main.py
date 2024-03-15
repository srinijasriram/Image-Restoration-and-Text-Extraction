import cv2
import pytesseract

# Function to display the image
def display_image(image):
    cv2.imshow("Restored Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Function to restore image using OpenCV
def restore_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Apply image restoration techniques (e.g., denoising, deblurring, etc.)
    # Example:
    restored_img = cv2.fastNlMeansDenoisingColored(img, None, 5, 5, 7, 21)
    
    return restored_img

# Function to extract text using Tesseract OCR
def extract_text(image):
    # Convert image to grayscale
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to enhance text
    _, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Perform OCR using Tesseract
    extracted_text = pytesseract.image_to_string(thresh_img)
    
    return extracted_text

def main(image_path):
    # Restore the image
    restored_image = restore_image(image_path)
    # Display the restored image
    #display_image(restored_image)   
    # Extract text from the restored image
    extracted_text = extract_text(restored_image)
    return extracted_text

# Example usage
if __name__ == "__main__":
    # Path to the degraded image
    image_path = "burnt.jpg"
    
    # Restore the image
    restored_image = restore_image(image_path)
    # Display the restored image
    display_image(restored_image)   
    # Extract text from the restored image
    extracted_text = extract_text(restored_image)
    
    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)
