FROM python:3.11.15-slim-bookworm@sha256:d29f48a31a8b408ed19272ca1e7b10ebae13b240a27e862d3d4217c528e2e0c3
WORKDIR /workspace
COPY workspace/ /workspace/
USER 65534:65534
CMD ["python", "-c", "print(open('/workspace/instruction.md').read())"]
