import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Select the database
db = client["piccipher"]

# Select the collection where the data is stored
image_data_collection = db["imagedata"]

# Query the collection to retrieve the stored data
stored_data = image_data_collection.find()

# Print the retrieved data
for data in stored_data:
    print("Image URL:", data["image_url"])
    print("OCR Text:", data["ocr_text"])
    print()

# Close the MongoDB connection
client.close()
