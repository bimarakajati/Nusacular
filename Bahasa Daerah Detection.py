import pickle

# Load the pickled model
with open('lrmodel.pckl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Prepare your input data
input_text = input("Enter your text: ")

# Make predictions using the loaded model
predicted_class = loaded_model.predict([input_text])

# The variable 'predicted_class' now contains the predicted class or value
print("Predicted class:", predicted_class)