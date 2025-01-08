from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
from fake_useragent import UserAgent

# Initialize lists to store data
Product_names = []
Prices = []
Description = []
Reviews = []

# Create a UserAgent object
ua = UserAgent()

# Loop through the pages
for i in range(1, 45):
    url = f"https://www.flipkart.com/search?q=Mobile+under+50000&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}"
    
    # Generate a random user agent
    headers = {'User-Agent': ua.random}
    
    # Make the request with the fake user agent
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    # Find the container holding the products
    box = soup.find("div", class_="DOjaWF gdgoEp")
    if not box:
        print(f"No products found on page {i}")
        continue

    # Extract product names
    names = box.find_all("div", class_="KzDlHZ")
    for name in names:
        Product_names.append(name.text)
    
    # Extract prices
    prices = box.find_all("div", class_="Nx9bqj _4b5DiR")
    for price in prices:
        Prices.append(price.text)
    
    # Extract descriptions
    desc = box.find_all("ul", class_="G4BRas")
    for d in desc:
        Description.append(d.text)
    
    # Extract reviews
    reviews = box.find_all("div", class_="XQDdHH")
    for review in reviews:
        Reviews.append(review.text)

# Check lengths of lists and print them
print("Lengths of lists before adjusting:")
print(f"Product_names: {len(Product_names)}")
print(f"Prices: {len(Prices)}")
print(f"Description: {len(Description)}")
print(f"Reviews: {len(Reviews)}")

# Find the minimum length among all lists
min_length = min(len(Product_names), len(Prices), len(Description), len(Reviews))

# Adjust lists to the same length
Product_names = Product_names[:min_length]
Prices = Prices[:min_length]
Description = Description[:min_length]
Reviews = Reviews[:min_length]

# Create the DataFrame
df = pd.DataFrame({
    "Product Name": Product_names,
    "Price": Prices,
    "Description": Description,
    "Reviews": Reviews
})

# Print the lengths of lists after adjusting
print("Lengths of lists after adjusting:")
print(f"Product_names: {len(Product_names)}")
print(f"Prices: {len(Prices)}")
print(f"Description: {len(Description)}")
print(f"Reviews: {len(Reviews)}")

# Save DataFrame to CSV
output_dir = "C:/Web_scrapping"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

df.to_csv(os.path.join(output_dir, "Flipkart_mobiles_under_50000.csv"), index=False)

print("Data has been saved to Flipkart_mobiles_under_50000.csv")
