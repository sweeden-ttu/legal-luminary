# Central Texas Legal Resource - Jekyll Site
# Based on jekyll/jekyll with project-specific additions

FROM docker.io/jekyll/jekyll:latest

# Set labels for container metadata
LABEL maintainer="Scott Weeden"
LABEL description="Jekyll build environment for Central Texas Legal Resource"
LABEL org.opencontainers.image.source="https://github.com/sweeden-ttu/legal-luminary"

# Install additional system packages for attribution scripts and RSS parsing
USER root
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-pillow \
    poppler-utils \
    imagemagick

# Install Python packages for attribution processing
RUN pip3 install --break-system-packages \
    pdf2image>=1.16.0 \
    PyPDF2>=3.0.0

USER jekyll

# Set working directory
WORKDIR /srv/jekyll

# Copy Gemfile first for layer caching
COPY --chown=jekyll:jekyll Gemfile Gemfile.lock ./

# Install project-specific gems (feedjira, faraday for RSS feeds)
RUN bundle install --jobs 4 --retry 3

# Copy the rest of the site files
COPY --chown=jekyll:jekyll . .

# Expose Jekyll server port
EXPOSE 4000

# Default command: build the site
CMD ["jekyll", "build"]
