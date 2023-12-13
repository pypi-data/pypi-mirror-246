from setuptools import setup, find_packages, findall

print("packages: " + str(find_packages()))

setup(
    name='bayserver',
    version='2.3.4',
    packages=find_packages(),
    author='Michisuke-P',
    author_email='michisukep@gmail.com',
    description='BayServer for Python',
    license='MIT',
    python_requires=">=3.7",
    url='https://baykit.yokohama/',
    package_data={
    },
    install_requires=[
      "bayserver-core==2.3.4",
      "bayserver-docker-cgi==2.3.4",
      "bayserver-docker-http3==2.3.4",
      "bayserver-docker-fcgi==2.3.4",
      "bayserver-docker-maccaferri==2.3.4",
      "bayserver-docker-ajp==2.3.4",
      "bayserver-docker-http==2.3.4",
      "bayserver-docker-wordpress==2.3.4",
    ],
    scripts=['bayserver_py'],
    include_package_data = True,
)

