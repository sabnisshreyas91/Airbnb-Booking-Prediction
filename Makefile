.PHONY: all

features:
	python src/generate_features_labels.py

train_test_split:
	python src/generate_train_test_split.py

train_model:
	python src/train_model.py

evaluate_model:
	python src/evaluate_model.py

run_app:
	python app.py
	
all: features train_test_split train_model evaluate_model run_app