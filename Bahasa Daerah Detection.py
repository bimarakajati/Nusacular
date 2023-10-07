import pickle

# Model list
model = ['lrmodel', 'mnbmodel', 'dtmodel']

# Load the pickled model
with open(f'model/{model[0]}.pckl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

while True:
    # Prepare your input data
    input_text = input("Enter your text: ")

    # Make predictions using the loaded model
    predicted_language = loaded_model.predict([input_text])

    # The variable 'predicted_language' now contains the predicted language or value
    print("Predicted language:", predicted_language[0])

    # Get the class probabilities as confidence scores
    class_probabilities = loaded_model.predict_proba([input_text])

    # The variable 'class_probabilities' contains the class probabilities
    print("Class Probabilities:", class_probabilities[0])

    # If you want to get the confidence score for the predicted class (the max probability)
    confidence_score = max(class_probabilities[0])
    print("Confidence Score:", confidence_score, '\n')