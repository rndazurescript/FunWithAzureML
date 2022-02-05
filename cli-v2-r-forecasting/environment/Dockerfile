FROM rocker/tidyverse:4.1
# Get later versions if needed from https://hub.docker.com/r/rocker/tidyverse/tags

# user root is required for installing packages
USER root

# Install python (this is still required by AzureML, but this requirement will soon be removed )
RUN apt-get update -qq && \
 apt-get install -y python3-pip curl
RUN ln -f /usr/bin/python3 /usr/bin/python
RUN ln -f /usr/bin/pip3 /usr/bin/pip
RUN pip install -U pip

# install azureml-base and libfuse (this is required for data access in local execution -- this requirement will also be removed soon)
RUN apt-get install -y libfuse-dev
RUN pip install azureml-dataprep azureml-core
RUN apt-get update && apt-get install -y fuse

# Install SQL Server ODBS driver
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#debian17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN export ACCEPT_EULA=Y;apt-get install -y msodbcsql17


# Install CRAN packages needed for your scripts
# We will use a single docker environment for all jobs but you can use multiple environments if you want
RUN R -e "install.packages('devtools', repos='https://cran.rstudio.com')"
RUN R -e "devtools::install_version('forecast', version = '8.16', repos = 'http://cran.us.r-project.org')"
RUN R -e "devtools::install_version('optparse', version = '1.7.1', repos = 'http://cran.us.r-project.org')"
RUN R -e "devtools::install_version('RODBC', version = '1.3', repos = 'http://cran.us.r-project.org')"
RUN R -e "devtools::install_version('AzureAuth', version = '1.3.3', repos = 'http://cran.us.r-project.org')"
RUN R -e "devtools::install_version('AzureKeyVault', version = '1.0.5', repos = 'http://cran.us.r-project.org')"

# return to previous non-root user
USER 1001