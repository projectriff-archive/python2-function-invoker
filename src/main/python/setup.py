import distutils.cmd
import distutils.log
import setuptools
import subprocess
import os


class GrpcCommand(distutils.cmd.Command):
    """A custom command to generate grpc modules"""
    user_options = []
    description = 'download proto file run grpctools'

    def initialize_options(self):
        self.clean('proto')
        self.clean('grpc_function')
        file = open("grpc_function/__init__.py","w")
        file.close()

    def clean(self,dir):
        if not os.path.exists(dir):
            os.mkdir(dir, 0777)
        else:
            for file in os.listdir(dir):
                file_path = os.path.join(dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)

    def finalize_options(self):
        pass

    def run(self):
        """Run command."""

        command = ["wget", "https://raw.githubusercontent.com/projectriff/function-proto/master/function.proto", "-P",
                   "proto"]
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)
        subprocess.check_call(command)

        command = ["python", "-m", "grpc_tools.protoc", "-I./proto", "--python_out=./grpc_function", "--grpc_python_out=./grpc_function",
                   "./proto/function.proto"]
        self.announce(
            'Running command: %s' % str(command),
            level=distutils.log.INFO)

        subprocess.check_call(command)


setuptools.setup(
    install_requires=['grpcio_tools','protobuf==3.4.0'],
    extras_require={
        ':python_version == "2.7"': ['futures']
    },
    cmdclass={
        'grpc': GrpcCommand,
    },
)
