import cv2
import pytesseract
import numpy as np
# Function to display the image
'''def display_image(image):
    cv2.imshow("Restored Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
def update_output_image(dst_patch, output_image, x, y):
    # Copy the denoised patch into the corresponding region of the output image
    output_image[y:y+dst_patch.shape[0], x:x+dst_patch.shape[1]] = dst_patch

def adaptiveFastNlMeansDenoisingColored(src, max_h, min_h, templateWindowSize, searchWindowSize, patch_size):
    # Convert the input image to Lab color space
    #src_lab = cv2.cvtColor(src, cv2.COLOR_BGR2Lab)
    output_image = np.zeros_like(src)
    # Iterate over patches or regions of the image
    for x,y,patch in iterate_patches(src, patch_size):
        # Compute local statistics for the current patch
        patch_variance = compute_variance(patch)

        # Adjust the filter strength 'h' based on local variance
        h = adjust_h(patch_variance, max_h, min_h)

        # Apply fastNlMeansDenoisingColored with adaptive parameters
        dst_patch = cv2.fastNlMeansDenoisingColored(patch, None, h, h, templateWindowSize, searchWindowSize)

        # Update the denoised patch in the output image
        update_output_image(dst_patch, output_image, x, y)

    return output_image

# function to iterate over patches
def iterate_patches(image, patch_size):
    for y in range(0, image.shape[0], patch_size):
        for x in range(0, image.shape[1], patch_size):
            yield x,y,image[y:y+patch_size, x:x+patch_size]


def compute_variance(patch):
    return np.var(patch)

# function to adjust filter strength 'h' based on local variance
def adjust_h(patch_variance, max_h, min_h):
    h = max_h - 0.1 * patch_variance
    return min(max_h, max(min_h, h))

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
    #restored_image = restore_image(image_path)
    
    img = cv2.imread(image_path)
    restored_image =adaptiveFastNlMeansDenoisingColored(img, max_h=0, min_h=0, templateWindowSize=7, searchWindowSize=21, patch_size=16)
    #Display the restored image
    #display_image(restored_image)  
    name="restored_image.jpg" 
    cv2.imwrite(name,restored_image) 
    # Extract text from the restored image
    extracted_text = extract_text(restored_image)
    with open("filename.txt", "w") as file:
        # Write the string to the file
        file.write(extracted_text)

        # Close the file
        file.close()
    return extracted_text

# Example usage
if __name__ == "__main__":
    # Path to the degraded image
    image_path = "burnt.jpg"
    img = cv2.imread(image_path)
    # Restore the image
    #restored_image = restore_image(image_path)
    restored_image =adaptiveFastNlMeansDenoisingColored(img, max_h=0, min_h=0, templateWindowSize=7, searchWindowSize=21, patch_size=16)
    # Display the restored image
    #display_image(restored_image)   
    # Extract text from the restored image
    extracted_text = extract_text(restored_image)
    
    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)
