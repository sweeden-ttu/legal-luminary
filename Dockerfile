# Create a Jekyll container from a Ruby Alpine image

# At a minimum, use Ruby 2.5 or later
FROM ruby:2.7-alpine3.15

WORKDIR /srv/jekyll
COPY /Users/sdw/.codex* $HOME

# Add Jekyll dependencies to Alpine
RUN apk update
RUN apk add --no-cache build-base gcc cmake git
RUN npm install $HOME/.codex-sdk

COPY ./Gemfile* /srv/jekyll

# Update the Ruby bundler and install Jekyll
RUN gem update bundler && bundle install
