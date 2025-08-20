# %%
import pandas as pd



# %%
csv_path = "../data/raw/NigeriaHousingDataset.csv"


# %%
# Load CSV
df = pd.read_csv(csv_path)


# Show first 5 rows
print(df.head())

# %%
df.info()

# %%
display(df)

# %%
df.isnull().sum()

# %%
df["Toilets"]

# %%
missing_percent = df.isnull().sum()/len(df)*100 #check proportion of missingness

# %%
missing_percent

# %%
##Insight:
##Bedrooms has very few missing → can fill with median or mode.
#Bathrooms and Toilets have moderate missing → median imputation works.
#Parking Spaces is missing almost half → maybe fill with 0 if absence of parking is plausible, or leave as null and let LLM handle missing info.


# %%
usd_rows = df['Currency'].str.contains('\$', regex=True)
df[usd_rows].head()

# %%
# Remove commas and $ sign
df['Price_clean'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)


# %%
USD_TO_NGN = 1532.34

# Create a new column in Naira
df.loc[usd_rows, 'Price_clean'] = df.loc[usd_rows, 'Price_clean'] * USD_TO_NGN

# %%
naira_rows = ~usd_rows
df.loc[naira_rows, 'Price_clean'] = df.loc[naira_rows, 'Price'].replace(',', '', regex=True).astype(float)

# %%
df['Price'] = df['Price_clean']
df.drop(columns=['Price_clean'], inplace=True)


# %%
df.head(10)

# %%
df['Currency'] = "₦"

# %%
df.head(10)

# %%
# ---------- Step 3: Handle missing numeric values ----------
numeric_cols = ['Bedrooms', 'Bathrooms', 'Parking Spaces', 'Toilets']

# Bedrooms, Bathrooms, Toilets → fill with median
df['Bedrooms'] = df['Bedrooms'].fillna(df['Bedrooms'].median())
df['Bathrooms'] = df['Bathrooms'].fillna(df['Bathrooms'].median())
df['Toilets'] = df['Toilets'].fillna(df['Toilets'].median())

# Parking Spaces → fill missing with 0
df['Parking Spaces'] = df['Parking Spaces'].fillna(0)

# %%
df.isnull().sum()

# %%
# Simple scoring: give weight to Bedrooms, Bathrooms, Toilets, Parking Spaces
df['Score'] = (
    df['Bedrooms'] * 2 +
    df['Bathrooms'] * 1 +
    df['Toilets'] * 0.5 +
    df['Parking Spaces'] * 0.5
)


