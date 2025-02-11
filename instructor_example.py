import os
import instructor
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Optional


# Step 1: Define the models
class ColumnModel(BaseModel):
    column_name: str
    data_type: str
    is_primary_key: bool
    is_nullable: bool
    default_value: Optional[str] = None
    is_foreign_key: bool

class MeasureModel(BaseModel):
    measure_name: str
    measure_formula: str
    measure_type: str
    related_columns: List[ColumnModel]
    is_aggregated: bool

class RelationshipModel(BaseModel):
    relationship_name: str
    from_table: str
    to_table: str
    from_column: str
    to_column: str
    relationship_type: str

class MetadataModel(BaseModel):
    connection_type: str
    source_name: str
    last_updated: str
    created_by: str
    refresh_schedule: str

class TableModel(BaseModel):
    table_name: str
    columns: List[ColumnModel]
    measures: List[MeasureModel]
    relationships: List[RelationshipModel]
    metadata: MetadataModel


# Step 2: Initialize the OpenAI client with Instructor
client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_KEY")))

# Define hook functions for logging
def log_kwargs(**kwargs):
    print(f"Function called with kwargs: {kwargs}")

def log_exception(exception: Exception):
    print(f"An exception occurred: {str(exception)}")

# Set up the hooks for logging
client.on("completion:kwargs", log_kwargs)
client.on("completion:error", log_exception)

# Step 3: Define the prompt for semantic model generation
user_input = """
Generate a semantic model for a Power BI report that includes the following elements:
- Table: 'Sales'
- Columns: 'ProductID' (integer), 'SalesAmount' (decimal), 'Date' (datetime)
- Measure: 'Total Sales' (sum of SalesAmount)
- Relationships: Sales table has a relationship with the 'Product' table on ProductID
- Metadata: Source from BigQuery, last updated on '2025-01-15', created by 'Admin', refresh schedule: 'daily'
"""

# Step 4: Use Instructor to request the semantic model
response = client.chat.completions.create(
    model="gpt-4",  # Use the appropriate GPT model
    response_model=TableModel,
    messages=[
        {"role": "user", "content": user_input}
    ]
)

# Step 5: Print the generated semantic model
generated_table = response
print(generated_table)
