import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
pumpkins_df = pd.read_csv("pumpkins_7.csv")

# Function to convert weight from lbs to kg
def convert_to_kg(weight_lbs):
    return weight_lbs * 0.453592

# Apply function to create a new column
pumpkins_df["weight_kg"] = pumpkins_df["weight_lbs"].apply(convert_to_kg)

# Function to classify weight
def classify_weight(weight_kg):
    if weight_kg < 500:
        return "light"
    elif 500 <= weight_kg < 1000:
        return "medium"
    else:
        return "heavy"

# Apply classification function
pumpkins_df["weight_class"] = pumpkins_df["weight_kg"].apply(classify_weight)

# Identify the heaviest pumpkin
heaviest_pumpkin = pumpkins_df.loc[pumpkins_df["weight_lbs"].idxmax()]
heaviest_weight = heaviest_pumpkin["weight_lbs"]
heaviest_variety = heaviest_pumpkin["variety"]
heaviest_location = f"{heaviest_pumpkin['city']}, {heaviest_pumpkin['state_prov']}, {heaviest_pumpkin['country']}"
heaviest_year = heaviest_pumpkin["gpc_site"]

# Scatter plot of estimated weight vs actual weight
plt.figure(figsize=(8,6))
scatter = plt.scatter(pumpkins_df["est_weight"], pumpkins_df["weight_kg"], c=pumpkins_df["weight_kg"], cmap="coolwarm", alpha=0.7)
plt.xlabel("Estimated Weight (lbs)")
plt.ylabel("Actual Weight (kg)")
plt.title("Estimated vs. Actual Weight of Pumpkins")
plt.colorbar(scatter, label="Weight (kg)")
plt.show()

# Filter data for three countries
selected_countries = ["USA", "UK", "China"]
filtered_pumpkins = pumpkins_df[pumpkins_df["country"].isin(selected_countries)]
filtered_pumpkins.to_csv("/Pumpkins//filtered_pumpkins.csv", index=False)

# Calculate mean weight by country
mean_weight_by_country = filtered_pumpkins.groupby("country")["weight_kg"].mean()
highest_mean_country = mean_weight_by_country.idxmax()

# Calculate mean weight by variety per country
mean_weight_by_variety = filtered_pumpkins.groupby(["country", "variety"])["weight_kg"].mean()
lowest_mean_variety = mean_weight_by_variety.idxmin()

# Boxplot for weight distribution by country
plt.figure(figsize=(8,6))
pumpkins_df.boxplot(column=["weight_kg"], by="country", grid=False)
plt.xlabel("Country")
plt.ylabel("Weight (kg)")
plt.title("Pumpkin Weight Distribution by Country")
plt.show()

# Facet plot showing data from each variety separately
import seaborn as sns
plt.figure(figsize=(10,8))
sns.catplot(x="country", y="weight_kg", hue="variety", data=filtered_pumpkins, kind="box")
plt.title("Pumpkin Weight Distribution by Variety and Country")
plt.show()