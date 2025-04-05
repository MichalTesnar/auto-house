.PHONY: me-have-a-house example

me-have-a-house:
	python main.py

example:
	cp -r secret/michal secret/example && \
	rm secret/example/data/wgzimmer.ch/* && \
	rm secret/example/data/flatfox.ch/* && \
	rm secret/example/data/wohnen.ethz.ch/* && \
	find secret/example -type f -name "*.json" -exec sed -i 's/: "[^"]*"/: ""/g' {} +