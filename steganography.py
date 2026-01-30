from PIL import Image

def encode_text_file():
    print("=== Encode a Message into an Image ===")
    image_path = input("Enter the path of the input image (e.g., input.png, input.jpg): ")
    input_text_file = input("Enter the path of the text file to hide (e.g., message.txt): ")
    output_image_path = input("Enter the path for the output image (e.g., output.png, output.jpg): ")

    with open(input_text_file, 'r') as file:
        message = file.read()

    img = Image.open(image_path)
    if img.mode != 'RGB' and img.mode != 'RGBA':
        img = img.convert('RGB')  # Convert to RGB if not already

    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Delimiter

    if len(binary_message) > (img.width * img.height * 3):
        print("Error: Message too long to hide in the image!")
        return

    data_index = 0
    for x in range(img.width):
        for y in range(img.height):
            pixel = list(img.getpixel((x, y)))
            for color in range(min(3, len(pixel))):  # Handle both RGB and RGBA
                if data_index < len(binary_message):
                    pixel[color] = pixel[color] & ~1 | int(binary_message[data_index])
                    data_index += 1
            img.putpixel((x, y), tuple(pixel))

    img.save(output_image_path)
    print(f"Message encoded and saved to {output_image_path}")

def decode_to_text_file():
    print("=== Decode a Message from an Image ===")
    image_path = input("Enter the path of the image to decode (e.g., output.png, output.jpg): ")
    output_text_file = input("Enter the path for the decoded text file (e.g., decoded_message.txt): ")

    img = Image.open(image_path)
    if img.mode != 'RGB' and img.mode != 'RGBA':
        img = img.convert('RGB')  # Convert to RGB if not already

    binary_message = ""
    for x in range(img.width):
        for y in range(img.height):
            pixel = img.getpixel((x, y))
            for color in range(min(3, len(pixel))):  # Handle both RGB and RGBA
                binary_message += str(pixel[color] & 1)

    delimiter = '1111111111111110'
    delimiter_index = binary_message.find(delimiter)
    if delimiter_index != -1:
        binary_message = binary_message[:delimiter_index]

    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:  # Ensure we have a full byte
            message += chr(int(byte, 2))

    with open(output_text_file, 'w') as file:
        file.write(message)

    print(f"Decoded message saved to {output_text_file}")

def main():
    print("Welcome to Steganography Tool!")
    print("1. Encode a message into an image")
    print("2. Decode a message from an image")
    choice = input("Enter your choice (1/2): ")

    if choice == '1':
        encode_text_file()
    elif choice == '2':
        decode_to_text_file()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
