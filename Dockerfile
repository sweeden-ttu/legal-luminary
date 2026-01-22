# Central Texas Legal Resource - Jekyll Site
# Comprehensive Dockerfile matching GitHub Actions workflow

# Use official Ruby image matching .ruby-version
FROM docker.io/library/ruby:3.3-slim-bookworm

# Set labels for container metadata
LABEL maintainer="Scott Weeden"
LABEL description="Jekyll build environment for Central Texas Legal Resource"
LABEL org.opencontainers.image.source="https://github.com/sweeden-ttu/legal-luminary"

# Set environment variables
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    LANGUAGE=C.UTF-8 \
    JEKYLL_ENV=production \
    BUNDLE_PATH=/usr/local/bundle \
    BUNDLE_APP_CONFIG=/usr/local/bundle \
    GEM_HOME=/usr/local/bundle

# Install system dependencies required for Jekyll and native gem extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory
WORKDIR /srv/jekyll

# Copy Gemfile and Gemfile.lock first (for Docker layer caching)
COPY Gemfile Gemfile.lock ./

# Install bundler and gems
RUN gem update --system && \
    gem install bundler && \
    bundle config set --local deployment 'false' && \
    bundle config set --local path '/usr/local/bundle' && \
    bundle install --jobs 4 --retry 3

# Copy the rest of the site files
COPY . .

# Expose Jekyll server port
EXPOSE 4000

# Default command: build the site
# Override with 'serve' for local development
CMD ["bundle", "exec", "jekyll", "build"]

# Alternative commands:
# Development server with live reload:
#   docker run -p 4000:4000 -v $(pwd):/srv/jekyll legal-luminary \
#     bundle exec jekyll serve --host 0.0.0.0 --livereload --incremental
#
# Production build only:
#   docker run -v $(pwd):/srv/jekyll legal-luminary \
#     bundle exec jekyll build --destination /srv/jekyll/_site
