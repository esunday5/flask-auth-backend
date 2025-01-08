import pg8000  # Use pg8000 instead of psycopg2

try:
    # Use the correct argument names for pg8000
    connection = pg8000.connect(
        user="admin",
        password="aZ2ryQ9DACsQNFDY1tQouCigbOO8N2ib",
        host="dpg-ctpbp40gph6c73dcjppg-a.oregon-postgres.render.com",
        port=5432,
        database="ekondo"
    )
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Error: {e}")
