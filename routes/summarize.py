from services.ia_client_factory import get_ia_client

client = get_ia_client(form_data)
result = client(prompt)
