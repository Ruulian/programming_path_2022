FROM python:latest

# Install package dependences
RUN apt -y -qq update; \
    apt -y -qq install socat bc;

# Install python packages
RUN pip install Flask;

WORKDIR /var/databases
RUN echo > programming_path.sqlite

# Copy flask files
WORKDIR /app
ADD ./infra .

# Copy challenges files
WORKDIR /challenges
ADD ./challenges .


# Start the challenge
CMD /app/start.sh