###
# Multi-stage build to produce a smaller runtime image
###

# --- Builder stage: install deps and compile pyfiles ---
FROM python:3.9-slim as builder
WORKDIR /build

# Install build requirements
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install into a custom prefix to avoid site-wide install
COPY requirements.txt /build/requirements.txt
RUN pip install --prefix=/install --no-cache-dir -r /build/requirements.txt

# Copy source and compile to bytecode to avoid shipping .py where possible
COPY src /build/src
RUN python -m compileall -q /build/src


# --- Final stage: minimal runtime image ---
FROM python:3.9-slim as runtime
WORKDIR /app

# Copy installed packages from builder into runtime image's site-packages
# Locate the site-packages path under /usr/local in the runtime image by using pip's default prefix layout
COPY --from=builder /install /usr/local

# Copy only the compiled bytecode (pyc) and any non-compiled resources we need
# Keep source .py files out of the final image to reduce size; copy .py only if present in runtime
COPY --from=builder /build/src /app/src

# Ensure pip and runtime tools are available but avoid dev packages
RUN python -c "import sys, pkgutil; print('Python', sys.version)"

# Expose the port the Flask app uses (index.py runs on 5000 by default)
EXPOSE 5000

# Use unbuffered output for log friendliness
CMD ["python", "-u", "src/index.py"]