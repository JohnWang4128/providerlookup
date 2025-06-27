import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from app import create_app
from models import db, Provider

def import_csv_data(csv_path):
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        print(f"Starting import from {csv_path}...")
        start_time = time.time()
        
        chunk_size = 10000
        chunk_num = 1
        
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            print(f"Processing chunk {chunk_num}...")
            
            chunk = chunk.dropna(subset=['NPI'])
            chunk = chunk.drop_duplicates(subset=['NPI'])
            
            for _, row in chunk.iterrows():
                existing_provider = Provider.query.filter_by(npi=row['NPI']).first()
                
                if existing_provider:
                    existing_provider.endpoint_type = row.get('Endpoint Type')
                    existing_provider.endpoint_type_description = row.get('Endpoint Type Description')
                    existing_provider.endpoint = row.get('Endpoint')
                    existing_provider.affiliation = row.get('Affiliation')
                    existing_provider.endpoint_description = row.get('Endpoint Description')
                    existing_provider.affiliation_legal_business_name = row.get('Affiliation Legal Business Name')
                    existing_provider.use_code = row.get('Use Code')
                    existing_provider.use_description = row.get('Use Description')
                    existing_provider.other_use_description = row.get('Other Use Description')
                    existing_provider.content_type = row.get('Content Type')
                    existing_provider.content_description = row.get('Content Description')
                    existing_provider.other_content_description = row.get('Other Content Description')
                    existing_provider.affiliation_address_line_one = row.get('Affiliation Address Line One')
                    existing_provider.affiliation_address_line_two = row.get('Affiliation Address Line Two')
                    existing_provider.affiliation_address_city = row.get('Affiliation Address City')
                    existing_provider.affiliation_address_state = row.get('Affiliation Address State')
                    existing_provider.affiliation_address_country = row.get('Affiliation Address Country')
                    existing_provider.affiliation_address_postal_code = row.get('Affiliation Address Postal Code')
                else:
                    new_provider = Provider(
                        npi=row['NPI'],
                        endpoint_type=row.get('Endpoint Type'),
                        endpoint_type_description=row.get('Endpoint Type Description'),
                        endpoint=row.get('Endpoint'),
                        affiliation=row.get('Affiliation'),
                        endpoint_description=row.get('Endpoint Description'),
                        affiliation_legal_business_name=row.get('Affiliation Legal Business Name'),
                        use_code=row.get('Use Code'),
                        use_description=row.get('Use Description'),
                        other_use_description=row.get('Other Use Description'),
                        content_type=row.get('Content Type'),
                        content_description=row.get('Content Description'),
                        other_content_description=row.get('Other Content Description'),
                        affiliation_address_line_one=row.get('Affiliation Address Line One'),
                        affiliation_address_line_two=row.get('Affiliation Address Line Two'),
                        affiliation_address_city=row.get('Affiliation Address City'),
                        affiliation_address_state=row.get('Affiliation Address State'),
                        affiliation_address_country=row.get('Affiliation Address Country'),
                        affiliation_address_postal_code=row.get('Affiliation Address Postal Code')
                    )
                    db.session.add(new_provider)
                
            # Commit the changes for this chunk
            db.session.commit()
            print(f"Chunk {chunk_num} committed to database")
            chunk_num += 1
        
        end_time = time.time()
        print(f"Import completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python import_data.py <path_to_csv_file>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"Error: File not found at {csv_path}")
        sys.exit(1)
    
    import_csv_data(csv_path)