import os
import boto3
import datetime
from datetime import datetime


#Logs a S3
def upload_log_to_s3(log_text, filename_prefix="log"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename_prefix}_{timestamp}.txt"
    s3_key = f"logs/{filename}" 

    #Archivo temporal
    with open(filename, "w") as file:
        file.write(log_text)
    try:
        s3 = boto3.client("s3")
        bucket_name = "s3nsei"
        s3.upload_file(filename, bucket_name, s3_key)
        print(f"✅ Log subido a S3: {s3_key}")
    except Exception as e:
        print(f"❌ Error al subir log a S3: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)  #Eliminando archivo temporal