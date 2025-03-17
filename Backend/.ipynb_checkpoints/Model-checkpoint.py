import pickle

try:
    with open(r'C:/Users/skand/Desktop/Major project/Backend/malware_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print(type(model))
except Exception as e:
    print(f"Error: {e}")
