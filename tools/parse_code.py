import os

def split_file(file_path, chunk_size):
    with open(file_path, 'r') as file:
        content = file.read()

    file_name = os.path.basename(file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    extension = os.path.splitext(file_name)[1]

    # Calculate the number of chunks
    num_chunks = (len(content) + chunk_size - 1) // chunk_size

    # Create a directory to store the file chunks
    output_dir = f"{file_name_without_extension}_chunks"
    os.makedirs(output_dir, exist_ok=True)

    # Split the content into chunks and write to separate files
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk_content = content[start:end]

        chunk_file_name = f"{file_name_without_extension}_chunk_{i}{extension}"
        chunk_file_path = os.path.join(output_dir, chunk_file_name)

        with open(chunk_file_path, 'w') as chunk_file:
            chunk_file.write(chunk_content)

        print(f"Chunk {i+1}/{num_chunks} written to {chunk_file_path}")

    print("File splitting completed.")

# Example usage
file_path = "Flask/app.py"
chunk_size = 5000  # Adjust this value according to your needs

split_file(file_path, chunk_size)
