import pickle
with open('EMBEDDINGS.pkl', 'rb') as f:
  triplet_df = pickle.load(f)

print(len(triplet_df))
